import pylogix

"""
Set 1734-OB8E properties.  We like no-load-detection turned off
and auto-reset turned on.  The default is opposite
Byte 0 = Fault State
Byte 1 = Fault Value
Byte 2 = Idle State
Byte 3 = Idle Value
Byte 4 = Enable No Load
Byte 5 = Reset Mode
Byte 6 = Enable Latched Alarms
Byte 7 = Pad
"""

fault_state = 0x00
fault_value = 0x00
idle_state = 0x00
idle_value = 0x00
no_load_detection = 0x00
reset_mode = 0xff
latched_alarms = 0x00
pad = 0x00

point_io_address = "192.168.1.188"
module_slot = 1

with pylogix.PLC(point_io_address) as comm:
    comm.Route = [(1, module_slot)]
    data = [fault_state, fault_value, idle_state, idle_value, no_load_detection, reset_mode, latched_alarms, pad]
    ret = comm.Message(0x10, 0x04, 123, 0x03, bytes(data))
