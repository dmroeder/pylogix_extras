"""
Use this at your own risk.  It has only been tested against a 1769-L30ER
and it will change the IP address immediately.
"""


import pylogix
from pylogix.lgx_response import Response
from struct import pack, unpack_from

def change_ip_address(plc, ip_address, sn_mask, gw_address):
    """
    Change the IP address of a device.
    Requires 22 bytes, 12 bytes for IP/GW/SN.  I used 0 for
    the last 10 bytes, they  are for name servers, which I'm not
    using.
    """
    conn = plc.conn.connect(False)
    if not conn[0]:
        return Response(None, None, conn[1])

    cip_service = 0x10
    cip_service_size = 0x03
    cip_class_type = 0x20
    cip_class = 0xf5
    cip_instance_type = 0x24
    cip_instance = 0x01
    cip_attribute_type = 0x30
    cip_attribute = 0x05

    # convert the address to a list of ints, then reverse the order
    ip_address = ip_address.split(".")
    ip_address = [int(octet) for octet in ip_address]
    ip_address.reverse()

    sn_mask = sn_mask.split(".")
    sn_mask = [int(octet) for octet in sn_mask]
    sn_mask.reverse()

    gw_address = gw_address.split(".")
    gw_address = [int(octet) for octet in gw_address]
    gw_address.reverse()

    # add some pad bytes for nameserver
    pad = [0 for _ in range(10)]

    data = ip_address + sn_mask + gw_address + pad

    request = pack('<BBBBBBBB22B',
                    cip_service,
                    cip_service_size,
                    cip_class_type,
                    cip_class,
                    cip_instance_type,
                    cip_instance,
                    cip_attribute_type,
                    cip_attribute,
                    *data)

    status, ret_data = plc.conn.send(request, False)

    return Response(None, None, status)


with pylogix.PLC("192.168.1.10") as comm:
    print(pylogix.__version__)
    response = change_ip_address(comm, "192.168.100.10", "255.255.255.0", "0.0.0.0")
    print(response)
