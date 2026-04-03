import pylogix


def get_startup_mer(plc):
    """
    Reads the registry entry on the PanelView Plus that contains the application that is
    configured to run at startup.  This assumes that there is one configured to load at
    startup and someone hasn't switched applications after it booted.
    """

    data = "HKEY_LOCAL_MACHINE\\Software\\Rockwell Software\\RSViewME\\Startup Options\\CurrentApp\0"
    ret = plc.Message(0x51, 0x04fe, 0x00, data=data)

    if ret.Status == "Success":
        temp = ret.Value.split(b"\\")
        try:
            name = temp[-1].decode("utf-8").strip()
        except (Exception,):
            name = None
    else:
        name = None

    return ret.Status, name


with pylogix.PLC("192.168.1.11", None) as comm:

    response = get_startup_mer(comm)
    print(response)
