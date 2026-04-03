import pylogix
import struct

with pylogix.PLC("192.168.1.10") as comm:
    ret = comm.Message(0x03, 0x69, 0x00, [0x09])

    # remove the overhead from the response packet
    response_value = ret.Value[44:]
    # get the force value
    force = struct.unpack_from("<H", response_value, 6)[0]
    
    if force == 0:
        print("forces disabled, no forces")
    elif force == 1:
        print("I/O forces present, forces disabled")
    elif force == 2:
        print("Forces enabled, no force present")
    elif force == 3:
        print("I/O forces present and forces are enabled")