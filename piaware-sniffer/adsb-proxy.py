import socket

def is_valid_lat_lon(lat, lon):
    """Check if latitude and longitude are valid."""
    return -90 <= lat <= 90 and -180 <= lon <= 180

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
    if lat_str and lon_str:
        print("debug")
        try:
            latitude = float(lat_str)
            longitude = float(lon_str)
            if alt_str:
                altitude = float(alt_str)
            else:
                altitude = None
            return (timestamp, id_number, (latitude, longitude, altitude))
        except ValueError:
            return None
    return None



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

if __name__ == "__main__":
    main()