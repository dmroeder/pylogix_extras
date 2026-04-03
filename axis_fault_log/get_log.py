import axis_string_lookup
import datetime
import pylogix
import struct


def get_records(data, fault):
    """ Extract the fault records from the packet

    return [time stamp, state chagne, action, sub code, fault code, fault type]
    or
    return [time stamp, action, sub code, fault code, fault type]
    """
    return_values = []
    count = struct.unpack_from("<B", data, 51)[0]
    if not count:
        # no faults, return empty list
        return return_values
    
    data = data[52:]
    # break up the data into chunks (14 for faults, 13 for alarms)
    if fault:
        record_bytes = [data[i:i + 14] for i in range(0, len(data), 14)]
    else:
        record_bytes = [data[i:i + 13] for i in range(0, len(data), 13)]

    for record in record_bytes:
        # fault type, fault code, sub code, stop action,
        # state change, time stamp
        if fault:
            values = struct.unpack_from("<BBHBBQ", record, 0)
        else:
            values = struct.unpack_from("<BBHBQ", record, 0)
        # reverse order because later we'll sort by tiem stamp
        return_values.append(values[::-1])
    return return_values

def fault_record_to_string(values):
    """ Take the values returned from the PLC and look up
    the corresponding strings.
    """
    if 0 <= values[0] <= 12:
        type_string = axis_string_lookup.fault_type[values[0]]
    elif 13 <= values[0] <= 127:
        type_string = axis_string_lookup.fault_type[13]
    elif values[0] == 128:
        type_string = axis_string_lookup.fault_type[14]
    else:
        type_string = axis_string_lookup.fault_type[15]

    if values[1] > 63 and values[0] != 0:
        code_string = axis_string_lookup.undefined[0]
    elif values[0] != 0:
        if values[0] == 1:
            code_string = axis_string_lookup.fault_code_001[values[1]]
        elif values[0] == 2:
            code_string = axis_string_lookup.fault_code_002[values[1]]
        elif values[0] == 3:
            code_string = axis_string_lookup.fault_code_003[values[1]]
        elif values[0] == 4:
            code_string = axis_string_lookup.fault_code_004[values[1]]
        elif values[0] == 5:
            code_string = axis_string_lookup.fault_code_005[values[1]]
        elif values[0] == 6:
            code_string = axis_string_lookup.fault_code_006[values[1]]
        elif values[0] == 7:
            code_string = axis_string_lookup.fault_code_007[values[1]]
        elif values[0] == 8:
            code_string = axis_string_lookup.fault_code_008[values[1]]
        elif values[0] == 9:
            code_string = axis_string_lookup.fault_code_009[values[1]]
        elif values[0] == 10:
            code_string = axis_string_lookup.fault_code_010[values[1]]
        elif values[0] == 11:
            code_string = axis_string_lookup.fault_code_011[values[1]]
        elif values[0] == 12:
            code_string = axis_string_lookup.fault_code_012[values[1]]
        elif 13 <= values[0] <= 127:
            code_string = axis_string_lookup.undefined[0]
        elif values[0] == 128:
            code_string = axis_string_lookup.fault_code_128[values[1]]
        else:
            code_string = axis_string_lookup.undefined[0]
    else:
        if 0 <= values[1] <= 4:
            code_string = axis_string_lookup.fault_type_zero_message[values[1]]
        else:
            code_string = axis_string_lookup.fault_type_zero_message[5]
    if 0 <= values[3] <= 4:
        action = axis_string_lookup.stop_action[values[3]]
    else:
        action == axis_string_lookup.undefined[0]

    if 0 <= values[4] <= 3:
        state = axis_string_lookup.state_change[values[4]]
    else:
        state = axis_string_lookup.undefined[0]

    time_stamp = datetime.datetime(1970, 1, 1) + datetime.timedelta(microseconds=values[5])

    return f"{time_stamp} - {type_string} - {code_string} - {action} - {state}"

def alarm_record_to_string(values):
    """ Take the values returned from the PLC and look up
    the corresponding strings.
    """
    if 0 <= values[0] <= 7:
        type_string = axis_string_lookup.alarm_type[values[0]]
    else:
        type_string = axis_string_lookup.undefined[0]

    if values[1] > 63 and values[0] > 0:
        code_string = axis_string_lookup.undefined[0]
    elif values[0] != 0:
        if values[0] == 1:
            code_string = axis_string_lookup.alarm_code_001[values[1]]
        elif values[0] == 2:
            code_string = axis_string_lookup.alarm_code_002[values[1]]
        elif values[0] == 3:
            code_string = axis_string_lookup.alarm_code_003[values[1]]
        elif values[0] == 4:
            code_string = axis_string_lookup.alarm_code_004[values[1]]
        elif values[0] == 5:
            code_string = axis_string_lookup.alarm_code_005[values[1]]
        elif values[0] == 6:
            code_string = axis_string_lookup.alarm_code_006[values[1]]
        elif values[0] == 7:
            code_string = axis_string_lookup.alarm_code_007[values[1]]
    else:
        if values[1] == 255:
            code_string = axis_string_lookup.alarm_type_zero_messages[0]
        else:
            code_string = axis_string_lookup.undefined[0]

    if 0 <= values[3] <= 1:
        action = axis_string_lookup.alarm_action[values[3]]
    else:
        action = axis_string_lookup.undefined[0]

    time_stamp = datetime.datetime(1970, 1, 1) + datetime.timedelta(microseconds=values[4])

    return f"{time_stamp} - {type_string} - {code_string} - {action}"

with pylogix.PLC("192.168.1.10") as comm:

    output_file = "axis_log.txt"
    axis_instance = 0x01

    # get the fault log for the axis
    combined_records = []
    ret = comm.Message(0x03, 0xb1, axis_instance, [0x19])
    if ret.Status == "Success":
        combined_records.extend(get_records(ret.Value, True))

    # get the alarm log for the axis
    ret = comm.Message(0x03, 0xb1, axis_instance, [0x1a])
    if ret.Status == "Success":
        combined_records.extend(get_records(ret.Value, False))

    # sort by the time stamp.
    sorted_records = sorted(combined_records, key=lambda x: x[0])
    with open(output_file, "w") as f:
        for record in sorted_records:
            if len(record) == 6:
                # translate fault, reverse the order back to normal
                text = fault_record_to_string(record[::-1])
            else:
                # translate alarm, reverse the order back to normal
                text = alarm_record_to_string(record[::-1])

            print(text)
            f.write(f"{text}\n")
