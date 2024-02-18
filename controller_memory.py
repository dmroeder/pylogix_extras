import pylogix
from pylogix.lgx_response import Response
from struct import pack, unpack_from

def get_memory(plc, service, cip_class, instance, attribute, data):
    """
    User configurable CIP command.  It is up to you to understand the
    data that will be returned
    
    returns Response class (.TagName, .Value, .Status
    """
    conn = plc.conn.connect(True)
    if not conn[0]:
        return Response(None, None, conn[1])

    free_memory_io = 0
    free_memory_dt = 0
    free_memory_gen = 0
    free_memory = 0
    total_memory_io = 0
    total_memory_dt = 0
    total_memory_gen = 0
    total_memory = 0

    AttributeService = service
    AttributeSize = 0x02
    AttributeClassType = 0x20
    AttributeClass = cip_class
    AttributeInstanceType = 0x24
    AttributeInstance = instance
    AttributeCount = 0x05

    request = pack('<BBBBBBHHHHHH',
                    AttributeService,
                    AttributeSize,
                    AttributeClassType,
                    AttributeClass,
                    AttributeInstanceType,
                    AttributeInstance,
                    AttributeCount,
                    1, 2, 5, 6, 7)

    status, ret_data = plc.conn.send(request, False)

    if status == 0:
        data = ret_data[50:]
        free_memory_io = unpack_from("<I", data, 0)[0] * 4
        free_memory_dt = unpack_from("<I", data, 4)[0] * 4
        free_memory_gen = unpack_from("<I", data, 8)[0] * 4
        free_memory = free_memory_io + free_memory_dt + free_memory_gen
        total_memory_io = unpack_from("<I", data, 16)[0] * 4
        total_memory_dt = unpack_from("<I", data, 20)[0] * 4
        total_memory_gen = unpack_from("<I", data, 24)[0] * 4
        total_memory = total_memory_io + total_memory_dt + total_memory_gen

    value = [free_memory_io, free_memory_dt, free_memory_gen, free_memory,
            total_memory_io, total_memory_dt, total_memory_gen, total_memory]

    return Response(None, value, status)


with pylogix.PLC("192.168.1.10") as comm:

    response = get_memory(comm, 0x03, 0x72, 0x01, 0x00, None)
    print(response)
