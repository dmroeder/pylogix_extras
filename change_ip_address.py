"""
Use this at your own risk.  It has only been tested against a 1769-L30ER
and it will change the IP address immediately.
"""


import pylogix
import struct


NEW_IP = "192.168.1.40"
NEW_SUBNET = "255.255.255.0"
NEW_GATEWAY = "0.0.0.0"


with pylogix.PLC("192.168.1.43") as comm:
    print(pylogix.__version__)
    comm.ProcessorSlot = None

    # convert the address to a list of ints, then reverse the order
    ip_address = NEW_IP.split(".")
    ip_address = [int(octet) for octet in ip_address]
    ip_address.reverse()

    sn_mask = NEW_SUBNET.split(".")
    sn_mask = [int(octet) for octet in sn_mask]
    sn_mask.reverse()

    gw_address = NEW_GATEWAY.split(".")
    gw_address = [int(octet) for octet in gw_address]
    gw_address.reverse()

    # add some pad bytes for nameserver
    pad = [0 for _ in range(10)]

    data = ip_address + sn_mask + gw_address + pad
    data = struct.pack("<22B", *data)
    
    ret = comm.Message(0x10, 0xf5, 0x01, 0x05, data)
    print(ret.Status)
