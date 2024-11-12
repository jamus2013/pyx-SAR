import socket
import sys
import os
import getpass
import requests

accumulate_tracks = False   # Enable to store tracks in a dictionary
max_alt = 90000 # ft MSL Altitude filter
piaware_address = "192.168.1.115" # PI address of piaware "192.168.56.168" for LTE hotspot
key = getpass.getpass("Enter CalTopo Connect Key: ")    # User inputs CalTopo access URL connect key
refresh_rate = 1    # Broadcast period [s] for CalTopo position updates


if accumulate_tracks:
    aircraft_database = {}

def main():
    # Connect to the dump1090 server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mavlink-sniffer")))
        
        s.connect((piaware_address, 30003))
        while True:
            raw_data = s.recv(4096).decode("utf-8").strip().split("\n")
            for message in raw_data:    # Each individual message
                parsed = parse_adsb_message(message)
                if parsed:
                    timestamp, id_number, lla = parsed  
                    print(f"MSG Received: Date/Time: {timestamp}, ID: {id_number}, LLA: {lla}")   # Uncomment for debug
                    publish_location(id_number, lla[0], lla[1], key)
                    
                    if accumulate_tracks:
                        store_adsb_data(timestamp, id_number, lla)


def parse_adsb_message(message):
    # Parse the ADS-B message and return relevant fields
    fields = message.split(',')
    if len(fields) < 16:
        return None  # Not enough fields

    # Extract fields based on expected positions
    msg_type = fields[0]
    if msg_type != "MSG":
        return None  # Only process MSG types

    # Extract date and time
    timestamp = f"{fields[6]} {fields[7]}"
    
    # Extract ID (hex code)
    id_number = fields[4]
    
    # Extract LLA if present
    lat_str = fields[14]    # Latitude (string)
    lon_str = fields[15]    # Longitude (string)
    alt_str = fields[11]    # Altitude (string)
    if lat_str and lon_str and alt_str:
        try:
            latitude = float(lat_str)
            longitude = float(lon_str)
            altitude = float(alt_str)
            if altitude <= max_alt: # Apply altitude lowpass filter
                return (timestamp, id_number, (latitude, longitude, altitude))
            else:
                return None
        except ValueError:
            return None
    return None


def store_adsb_data(id_number, timestamp, lla):
    # Generate dictionary sorted by aircraft ID
    if id_number not in aircraft_database:
        aircraft_database[id_number] = []
    aircraft_database[id_number].append((timestamp, lla))


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


if __name__ == "__main__":
    main()