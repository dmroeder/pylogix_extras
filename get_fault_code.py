import pylogix
from pylogix.lgx_response import Response
from struct import pack, unpack_from

def get_controller_fault(plc):
    """
    User configurable CIP command.  It is up to you to understand the
    data that will be returned
    
    returns Response class (.TagName, .Value, .Status
    """
    conn = plc.conn.connect(True)
    if not conn[0]:
        return Response(None, None, conn[1])

    cip_service = 0x01
    cip_service_size = 0x02
    cip_class_type = 0x20
    cip_class = 0x73
    cip_instance_type = 0x24
    cip_instance = 0x01

    request = pack('<BBBBBB',
                    cip_service,
                    cip_service_size,
                    cip_class_type,
                    cip_class,
                    cip_instance_type,
                    cip_instance)

    status, ret_data = plc.conn.send(request, False)

    if status == 0:
        data = ret_data[44:]
        major = unpack_from("<H", data, 20)[0]
        minor = unpack_from("<H", data, 22)[0]
    else:
        major = None
        minor = None

    return Response(None, (major, minor), status)


with pylogix.PLC("192.168.1.10") as comm:
    response = get_controller_fault(comm)
    print(response)
