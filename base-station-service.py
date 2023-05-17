def main():
    import time

    refresh_rate    = 2                         # Position update period [s]
    link            = connectUAS(8, 57600)
    key             = "hcru1234"                # Caltopo connect key
    device_id       = "HCRU-TEST1"              # Caltopo device ID

    while True:
        lat, lon = getUASPosition(link)         # Get global position
        # print('Latitude = %f \t\t Longitude = %f' % (lat, lon))   # Uncomment for position debug
        publishLocation(device_id, lat, lon, key)  # Upload position updates to Caltopo
        time.sleep(refresh_rate)


def connectUAS(port_number, baudrate):
    # INITIALIZE SERIAL CONNECTION FROM GCS TO PIXHAWK
    from pymavlink import mavutil
    master = mavutil.mavlink_connection("com%d" % port_number, baud=baudrate)
    # NOTE: Might have to change tty* syntax if using GPIO
    master.wait_heartbeat()  # Confirm connection
    print('Connection successful')
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

if __name__ == '__main__':
    main()
