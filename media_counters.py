
import pylogix
import struct

with pylogix.PLC("192.168.1.10", slot=0) as comm:
    ret = comm.Message(0x0e, 0xf6, 0x01, 0x05)
    if ret.Status == "Success":
        data = ret.Value[44:]
        media_counters = [struct.unpack_from("<I", data, i*4)[0] for i in range(12)]
        print(media_counters)
    else:
        print(ret.Status)