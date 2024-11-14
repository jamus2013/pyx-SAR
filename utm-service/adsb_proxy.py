import socket

accumulate_tracks = False   # Enable to store tracks in a dictionary
broadcast_tracks = False    # Enable to stream ADS-B tracks to CalTopo
max_alt = 90000 # ft MSL Altitude filter
max_radius = 30 # km maximum radius around home_point to observe
home_point = (34.7308, -86.5994) # Reference point for air traffic center
pi_address = "192.168.1.231"    # IP address of PiAware RPi

if accumulate_tracks:
    aircraft_database = {}  # Initialize dictionary to store tracks
if broadcast_tracks:
    from caltopo_utils import publish_location
    import getpass
    key = getpass.getpass("Enter CalTopo Connect Key: ")    # User inputs CalTopo access URL connect key

def main():
    adsb_socket = connect_to_piaware(pi_address, 30003, 20)    # Connect to PiAware over LAN
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
            
            latitude = float(lat_str)   
            longitude = float(lon_str)
            altitude = float(alt_str)
            timestamp = f"{fields[6]} {fields[7]}" # Extract date and time
            id_number = fields[4]  # Extract ID (hex code)
            lla = (latitude, longitude, altitude)
            
            if float(alt_str) <= max_alt: # & is_inside_radius(home_point, (lla[0], lla[1]), max_radius):
                if is_inside_radius(home_point, (lla[0], lla[1]), max_radius):
                
                    print(f"MSG Received: Date/Time: {timestamp}, ID: {id_number}, LLA: {lla}")   # Uncomment for debug
                    if broadcast_tracks:
                        publish_location(id_number, lla[0], lla[1], key, timestamp)
                    if accumulate_tracks:
                        store_adsb_data(timestamp, id_number, lla)
            #if is_inside_radius(home_point, (lla[0], lla[1]), max_radius):
            #    print('Inside radius')
            #else:
            #    print('Outside radius')


def store_adsb_data(id_number, timestamp, lla):
    # Generate dictionary sorted by aircraft ID
    if id_number not in aircraft_database:
        aircraft_database[id_number] = []
    aircraft_database[id_number].append((timestamp, lla))


def is_inside_radius(ref, lat_lon, radius):
    # Determines if lat/long point is within predefined radius [km] of reference point
    from general_utils import dist_between_points

    d = dist_between_points(ref, lat_lon)
    if d <= radius:
        return True
    else:
        return False

if __name__ == "__main__":
    main()