import pylogix
import struct

# PowerFlex IP Address
with pylogix.PLC("172.17.120.250") as comm:
    parameter_number = 39
    new_value = 1
    new_value = struct.pack("<H", new_value)
    ret = comm.Message(0x10, 0x0f, parameter_number, 0x01, new_value)
    print(ret.Status)