import pylogix
import struct

"""
Available attributes (thanks JeremyM)

    1	Total Connections Supported		    H
    2	Total Connections Open		        H
    3	Maximum Connections Opened		    H
    4	Reserved I/O Connections		    H
    5	Opened I/O Connections		        H
    6	Maximum Opened I/O Connections		H
    7	Reserved Produced Tag Connections	H
    8	Opened Produced Tag Connections		H
    9	Max Produced Tag Connections		H
    10	Reserved Consumed Tag Connections	H
    11	Opened Consumed Tag Connections		H
    12	Max Consumed Tag Connections		H
    13	Opened MSG/BT Connections		    H
    14	Maximum Opened MSG/BT Connections	H
    15	Opened Comm Connections		        H
    16	Maximum Opened Comm Connections		H
    17	Reserved Unconnected Buffers		I
    18	Maximum Unconnected Buffers		    I
    19	Unconnected Buffers Used		    I
    20	MSG/BT Connection Cache Size		H
    21	MSG/BT Cache Entries Used		    H
    22	Maximum MSG/BT Cache Entries Used	H
"""

def get_cip_connections(plc):
    # get attributes 1 > 16
    attributes = [i for i in range(1,17)]
    ret = plc.Message(0x03, 0x304, 0x01, attributes)
    values = []
    if ret.Status == "Success":
        data = ret.Value[44:]
        attribute_count = struct.unpack_from("<H", data, 0)[0]
        data = data[2:]
        values = {}
        for i in range(attribute_count):
            attr, value = struct.unpack_from("<IH", data, i*6)
            values[attr] = value
    
    return ret.Status, values

with pylogix.PLC("192.168.1.10") as comm:

    stuff = get_cip_connections(comm)
    print(stuff)