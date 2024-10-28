import socket

accumulate_tracks = True
max_alt = 10000 # ft MSL Altitude filter

if accumulate_tracks:
    aircraft_database = {}


def parse_adsb_message(message):
    """Parse the ADS-B message and return relevant fields."""
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
            if altitude <= max_alt:
                return (timestamp, id_number, (latitude, longitude, altitude))
            else:
                return None
        except ValueError:
            return None
    return None

def store_adsb_data(id_number, timestamp, lla):
    if id_number not in aircraft_database:
        aircraft_database[id_number] = []
    aircraft_database[id_number].append((timestamp, lla))

def main():
    # Connect to the dump1090 server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("192.168.56.168", 30003))
        while True:
            raw_data = s.recv(4096).decode("utf-8").strip().split("\n")
            for message in raw_data:
                parsed = parse_adsb_message(message)
                if parsed:
                    timestamp, id_number, lla = parsed
                    print(f"Date/Time: {timestamp}, ID: {id_number}, LLA: {lla}")
                    if accumulate_tracks:
                        store_adsb_data(timestamp, id_number, lla)
if __name__ == "__main__":
    main()