import pylogix
import struct

def get_controller_fault(plc):
    """
    User configurable CIP command.  It is up to you to understand the
    data that will be returned
    
    returns Staus, major, minor
    """
    ret = plc.Message(0x01, 0x73, 0x01, 0x00)

    if ret.Status == "Success":
        data = ret.Value[44:]
        major = struct.unpack_from("<H", data, 20)[0]
        minor = struct.unpack_from("<H", data, 22)[0]
    else:
        major = None
        minor = None

    return ret.Status, major, minor


with pylogix.PLC("192.168.1.10") as comm:
    response = get_controller_fault(comm)
    print(response)
