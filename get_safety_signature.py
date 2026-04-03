import pylogix
import struct

with pylogix.PLC("192.168.1.110") as comm:

    ret = comm.Message(0x03, 0x334, 0x01, [0x04, 0x0c])
    data = ret.Value[44:]
    signature_present = struct.unpack_from("<B", data, 6)[0]
    
    if signature_present:
        data = data[12:]
        # convert each character to string
        characters = [str(hex(d))[2:].upper() for d in data]
        # pad with 0 if only a single character (ex: f > 0f)
        characters = [s if len(s) == 2 else "0" + s for s in characters]
        # convert to a string
        signature = "".join(c for c in characters)
        # format similar to Rockwell
        signature = " - ".join(signature[i:i+8] for i in range(0, len(signature), 8))
        print(signature)
    else:
        print("no siguature")