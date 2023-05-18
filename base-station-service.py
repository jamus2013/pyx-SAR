def main():
    import time
    baud                = 57600
    refresh_rate        = 2                 # Position update period [s]
    key                 = "xxxxxxxx"        # Caltopo connect key
    device_id           = "xxxx-xxxx"      # Caltopo device ID

    link = connectUAS(baud)  # Open telemetry link
    while True:
        if link is not None :
            lat, lon = getUASPosition(link)         # Get global position
            # print('Latitude = %f \t\t Longitude = %f' % (lat, lon))   # Uncomment for position debug
            publishLocation(device_id, lat, lon, key)  # Upload position updates to Caltopo
            time.sleep(refresh_rate)    # Delay to stagger CalTopo upload
        else:
            break


def connectUAS(baudrate):
    # INITIALIZE SERIAL CONNECTION FROM GCS TO PIXHAWK
    from pymavlink import mavutil
    port = detectPort("usb")    # [Hook for future UDP connection]
    if port is not None:
        master = mavutil.mavlink_connection(port, baud=baudrate)
        print('Waiting for connection...')
        master.wait_heartbeat()  # Confirm connection
        print('Connection successful!')
        return master


def getUASPosition(master):
    # GET GEOSPATIAL DATA FROM PIXHAWK
    from pymavlink import mavutil
    master.mav.request_data_stream_send(  # Initialize MAVLink stream
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_DATA_STREAM_ALL,
        1, 1
    )
    while True:
        msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True, timeout=10)
        if msg is not None:
            break
    # print(msg)
    lat = msg.lat / 1e7  # Est. Latitude [deg N WGS-84]
    lon = msg.lon / 1e7  # Est. Longitude [deg E WGS-84]
    alt_msl = msg.alt  # Est. Altitude [m MSL]
    alt_rel = msg.relative_alt  # Est. Altitude relative to HOME [m AGL]
    return lat, lon


def publishLocation(device_id, lat, lon, connect_key):
    # STREAM POSITION TO CALTOPO API
    import requests
    endpoint = "https://caltopo.com/api/v1/position/report/%s?id=%s&lat=%f&lng=%f" % (connect_key, device_id, lat, lon)
    #print(endpoint)
    r = requests.get(url=endpoint)
    if r.status_code == 200:
        print("Updated location to \t %fN, \t%fE" % (lat, lon))
    else:
        print("Upload failed, error code %d" % r.status_code)


def detectPort(type):
    # IDENTIFY TELEMETRY LINK'S PORT
    print("Detecting port...")
    if type == 'usb':
        import serial.tools.list_ports
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "USB" in port.description:       # Telemetry modem
                com_port = port.device
                break
            elif "CUBE" in port.description:    # MicroUSB
                com_port = port.device
                break
            else:
                com_port = None
    if com_port is not None:
        print("Port found!")
        return com_port
    else:
        print("No device detected: Check USB connection")
        return None


if __name__ == '__main__':
    main()
