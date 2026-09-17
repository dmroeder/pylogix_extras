import pylogix
import struct

print(pylogix.__version__)
chassis_size = struct.pack("<I", 2)
with pylogix.PLC("192.168.1.188") as comm:
    ret = comm.Message(0x10, 0x300, 0x01, 0x01, chassis_size)
    print(ret)