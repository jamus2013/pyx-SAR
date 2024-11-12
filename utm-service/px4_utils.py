def connect_to_mavproxy(udp_ip_address, udp_port):
    # Establish connection to MAVLink router
    from pymavlink import mavutil

    connection = mavutil.mavlink_connection(f'udp:{udp_ip_address}:{udp_port}')
    print('Waiting for heartbeat...')
    connection.wait_heartbeat()
    print('Heartbeat received.')
    return connection

def get_gps_data(connection):
    # Get LLA from nav filter
    from general_utils import get_system_time

    while True:
        try:
            msg = connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
            if msg:
                latitude = msg.lat / 1e7    # Deg N [WGS84]
                longitude = msg.lon / 1e7   # Deg E [WGS84]
                altitude = msg.alt / 1000   # double check units here...
                time_local = get_system_time()  # Local time 
                #print(f'Latitude: {latitude}, Longitude: {longitude}') # Uncomment to debug
                return latitude, longitude, altitude, time_local
        except KeyboardInterrupt:
            print('Stopped GPS collection')
            break
        except Exception as e:
            print(f'Error: {e}')