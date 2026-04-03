import pylogix
import struct

# PowerFlex IP Address
with pylogix.PLC("172.17.120.250") as comm:
    parameter_number = 39
    ret = comm.Message(0x0e, 0x0f, parameter_number, 0x01)

    if ret.Status == "Success":
        value = ret.Value[44:]
        value = struct.unpack_from("<H", value)[0]
        print(value)
    else:
        print(ret.Status)