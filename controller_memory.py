import pylogix
import struct


def get_memory(plc):
    """
    This will apparently not work for 5380/5580 controllers
    """
    free_memory_io = 0
    free_memory_dt = 0
    free_memory_gen = 0
    free_memory = 0
    total_memory_io = 0
    total_memory_dt = 0
    total_memory_gen = 0
    total_memory = 0

    ret = plc.Message(0x03, 0x72, 0x01, [0x01, 0x02, 0x05, 0x06, 0x07])

    if ret.Status == "Success":
        data = ret.Value[50:]
        free_memory_io = struct.unpack_from("<I", data, 0)[0] * 4
        free_memory_dt = struct.unpack_from("<I", data, 4)[0] * 4
        free_memory_gen = struct.unpack_from("<I", data, 8)[0] * 4
        free_memory = free_memory_io + free_memory_dt + free_memory_gen
        total_memory_io = struct.unpack_from("<I", data, 16)[0] * 4
        total_memory_dt = struct.unpack_from("<I", data, 20)[0] * 4
        total_memory_gen = struct.unpack_from("<I", data, 24)[0] * 4
        total_memory = total_memory_io + total_memory_dt + total_memory_gen

    value = [free_memory_io, free_memory_dt, free_memory_gen, free_memory,
            total_memory_io, total_memory_dt, total_memory_gen, total_memory]

    return value


with pylogix.PLC("192.168.1.10") as comm:

    response = get_memory(comm)
    print(response)
