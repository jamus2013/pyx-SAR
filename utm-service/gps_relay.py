from pymavlink import mavutil
import time
import getpass
from px4_utils import get_gps_data, connect_to_mavproxy
from caltopo_utils import publish_location

device_id = input("Enter CalTopo device ID: ")  # User inputs CalTopo trackable device name
key = getpass.getpass("Enter CalTopo Connect Key: ")    # User inputs CalTopo access URL connect key
logging_enabled = False
refresh_rate = 1    # Broadcast period [s] for CalTopo position updates
udp_address = '127.0.0.1'   # IP address for UDP
udp_port = 14551    # UDP port for pyx-SAR; NOTE GCS will need a separate port number

def main():
    mavproxy_connection = connect_to_mavproxy(udp_address, udp_port)
    print(f'Broadcasting {device_id} location to CalTopo...')
    #if logging_enabled == True:
    #    log_file        = generateLogFile()     # Create CSV file(name) using current system time
    while True:
        if mavproxy_connection is not None :
            lat, lon, alt, local_time = get_gps_data(mavproxy_connection)         # Get global position and time
            #print(f'Latitude: {lat}, Longitude: {lon}') # Uncomment for position debug
            response = publish_location(device_id, lat, lon, key, local_time)  # Upload position updates to Caltopo
            #if logging_enabled == True:
            #    logDataStream(log_file,time_stamp, lat, lon, response)
            time.sleep(refresh_rate)    # Delay to stagger CalTopo upload
        else:
            break


if __name__ == '__main__':
    main()