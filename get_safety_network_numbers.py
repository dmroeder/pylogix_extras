import pylogix

"""
Example to get the SNN's from a controller.  In my case, this was a 5380
CompactLogix, configured for dual port mode, so there are 3.  The values
come in reverse order.
"""
with pylogix.PLC("192.168.1.10") as comm:

    ret = comm.Message(0x0e, 0x39, 0x01, 0x1e)

    # get the value from the packet, 6 bytes starting at 47
    value = ret.Value[47:53]
    # convert to list in reverse order
    value_list = [int(v) for v in value][::-1]
    # convert to string
    backplane_snn = ''.join(hex(v)[2:] for v in value_list)
    print(backplane_snn)

    # get the value from the packet, 6 bytes starting at 47
    value = ret.Value[59:65]
    # convert to list in reverse order
    value_list = [int(v) for v in value][::-1]
    # convert to string
    a1_snn = ''.join(hex(v)[2:] for v in value_list)
    print(a1_snn)

    # get the value from the packet, 6 bytes starting at 47
    value = ret.Value[71:77]
    # convert to list in reverse order
    value_list = [int(v) for v in value][::-1]
    # convert to string
    a2_snn = ''.join(hex(v)[2:] for v in value_list)
    print(a2_snn)
