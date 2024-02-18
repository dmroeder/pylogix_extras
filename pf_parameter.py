import pylogix
from pylogix.lgx_response import Response
from struct import pack, unpack_from

def get_parameter(plc, parameter):
    """
    User configurable CIP command.  It is up to you to understand the
    data that will be returned
    
    returns Response class (.TagName, .Value, .Status
    """
    conn = plc.conn.connect(True)
    if not conn[0]:
        return Response(None, None, conn[1])

    cip_service = 0x0e
    cip_service_size = 0x03
    cip_class_type = 0x20
    cip_class = 0x93
    cip_instance_type = 0x24
    cip_instance = parameter
    cip_attribute_type = 0x30
    cip_attribute = 0x09

    request = pack('<BBBBBBBB',
                    cip_service,
                    cip_service_size,
                    cip_class_type,
                    cip_class,
                    cip_instance_type,
                    cip_instance,
                    cip_attribute_type,
                    cip_attribute)

    status, ret_data = plc.conn.send(request, False)

    if status == 0:
        data = ret_data[44:]
        value = unpack_from("<H", data, 0)[0]
    else:
        value = None

    return Response(None, value, status)


with pylogix.PLC("192.168.1.101") as comm:
    response = get_parameter(comm, 69)
    print(response)
