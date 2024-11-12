import socket

accumulate_tracks = False   # Enable to store tracks in a dictionary
max_alt = 90000 # ft MSL Altitude filter
if accumulate_tracks:
    aircraft_database = {}  # Initialize dictionary to store tracks


def main():
    adsb_socket = connect_to_piaware("192.168.1.115", 30003, 10)    # Connect to PiAware over LAN
    while True:
        parse_adsb_data(adsb_socket)


def connect_to_piaware(ip_address, port, timeout):
    # Connect to local dump1090 server
    print('Connecting to PiAware...')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)   # Timeout [seconds]
        s.connect((ip_address, port))
        print("Connected to PiAware")
        return s
    except (socket.error, socket.timeout) as e:
        print(f'PiAware connection failed: {e}')
        

def parse_adsb_data(sock):
    # Decode ADS-B tracks into desired data
    raw_data = sock.recv(4096).decode("utf-8").strip().split("\n")  # Decode incoming tracks
    for message in raw_data:    # Each individual message
        fields = message.split(',')
        if len(fields) < 16:
            return None  # Not enough fields

        # Extract fields based on expected positions
        msg_type = fields[0]
        if msg_type != "MSG":
            return None  # Only process MSG types

        # Extract LLA if present        
        lat_str = fields[14]    # Latitude (string)
        lon_str = fields[15]    # Longitude (string)
        alt_str = fields[11]    # Altitude (string)

        # Filter by valid LLA
        if lat_str and lon_str and alt_str:
            if float(alt_str) <= max_alt:
                latitude = float(lat_str)   # ADD GEO FILTER HERE?
                longitude = float(lon_str)
                altitude = float(alt_str)
                timestamp = f"{fields[6]} {fields[7]}" # Extract date and time
                id_number = fields[4]  # Extract ID (hex code)
                lla = (latitude, longitude, altitude)
                print(f"MSG Received: Date/Time: {timestamp}, ID: {id_number}, LLA: {lla}")   # Uncomment for debug
                #publish_location(id_number, lla[0], lla[1], key)
        
                if accumulate_tracks:
                    store_adsb_data(timestamp, id_number, lla)


def store_adsb_data(id_number, timestamp, lla):
    # Generate dictionary sorted by aircraft ID
    if id_number not in aircraft_database:
        aircraft_database[id_number] = []
    aircraft_database[id_number].append((timestamp, lla))


if __name__ == "__main__":
    main()