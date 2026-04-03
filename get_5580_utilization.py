import pylogix
import struct

def get_io_utilization(plc):
    ret = plc.Message(0x58, 0x335, 0x01, 0x00)
    if ret.Status == "Success":
        data = ret.Value[44:]
        task_utilization = struct.unpack_from("<B", data, 5)[0]
        msg_utilization = struct.unpack_from("<B", data, 9)[0]
        io_utilization = struct.unpack_from("<B", data, 11)[0]
        return ret.Status, task_utilization, msg_utilization, io_utilization
    else:
        return ret.Status, None, None, None

with pylogix.PLC("192.168.1.10") as comm:
    stuff = get_io_utilization(comm)
    print(stuff)