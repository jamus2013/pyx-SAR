from pymavlink import mavutil
import time
import requests
import getpass

device_id = input("Enter CalTopo device ID: ")  # User inputs CalTopo trackable device name
key = getpass.getpass("Enter CalTopo Connect Key: ")    # User inputs CalTopo access URL connect key
logging_enabled = False
refresh_rate = 0.5    # Broadcast period [s] for CalTopo position updates
udp_address = '127.0.0.1'   # IP address for UDP
udp_port = 14551    # UDP port for pyx-SAR; NOTE GCS will need a separate port number

def main():
    mavproxy_connection = connect_to_mavproxy(udp_address, udp_port)
    print('Broadcasting location to CalTopo...')
    #if logging_enabled == True:
    #    log_file        = generateLogFile()     # Create CSV file(name) using current system time
    while True:
        if mavproxy_connection is not None :
            lat, lon = get_gps_data(mavproxy_connection)         # Get global position and time
            #print(f'Latitude: {lat}, Longitude: {lon}') # Uncomment for position debug
            response = publish_location(device_id, lat, lon, key)  # Upload position updates to Caltopo
            #if logging_enabled == True:
            #    logDataStream(log_file,time_stamp, lat, lon, response)
            time.sleep(refresh_rate)    # Delay to stagger CalTopo upload
        else:
            break


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
                #time_local = get_system_time()  # Local time 
                #print(f'Latitude: {latitude}, Longitude: {longitude}') # Uncomment to debug
                return latitude, longitude
        except KeyboardInterrupt:
            print('Stopped GPS collection')
            break
        except Exception as e:
            print(f'Error: {e}')


def publish_location(device_id, lat, lon, connect_key):
    # STREAM POSITION TO CALTOPO API
    
    endpoint = f'https://caltopo.com/api/v1/position/report/{connect_key}?id={device_id}&lat={lat}&lng={lon}'
    #print(endpoint)    # Uncomment to debug URL
    r = requests.get(url=endpoint)
    if r.status_code == 200:
        print(f'Updated location to {lat}, {lon}')
    else:
        print(f'Upload failed, error code {r.status_code}')
    return r.status_code


def get_system_time():
    # CREATE TIME STAMP BASED ON LOCAL SYSTEM TIME
    import datetime
    sys_time = datetime.datetime.now()
    return sys_time.strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    main()