
import pylogix
import struct

with pylogix.PLC("192.168.1.10") as comm:
    ret = comm.Message(0x0e, 0xf6, 0x01, 0x04)
    if ret.Status == "Success":
        data = ret.Value[44:]
        interface_counters = [struct.unpack_from("<I", data, i*4)[0] for i in range(11)]
        print(interface_counters)
    else:
        print(ret.Status)