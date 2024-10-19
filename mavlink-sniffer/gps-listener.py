from pymavlink import mavutil
import time

def connect_to_mavproxy(udp_ip_address, udp_port):
    # Extract state estimates from MAVLink stream in parallel to GCS instance
    connection = mavutil.mavlink_connection(f'udp:{udp_ip_address}:{udp_port}')
    print('Waiting for heartbeat...')
    connection.wait_heartbeat()
    print('Heartbeat received.')
    return connection

def get_gps_data(connection):
    # Get LLA from nav filter
    while True:
        try:
            msg = connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
            if msg:
                latitude = msg.lat / 1e7    # Deg N [WGS84]
                longitude = msg.lon / 1e7   # Deg E [WGS84]
                altitude = msg.alt / 1000   # double check units here...
                print(f'Latitude: {latitude}, Longitude: {longitude}')
        except KeyboardInterrupt:
            print('Stopped GPS collection')
            break
        except Exception as e:
            print(f'Error: {e}')


if __name__ == '__main__':
    mavproxy_connection = connect_to_mavproxy('127.0.0.1', 14450)
    get_gps_data(mavproxy_connection)