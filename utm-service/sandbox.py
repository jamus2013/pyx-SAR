from px4_utils import connect_to_mavproxy
from pymavlink import mavutil

# Define flag bits
VALID_COORDINATES = 1      # 0b0001 (bit 0)
VALID_HEADING = 2         # 0b0010 (bit 1)

# Combine flags using bitwise OR


# Example ADS-B vehicle data
icao = int(1234567)          # Example ICAO address (unique identifier)
lat = int(34.7295 * 1e7)   # Latitude in 1E-7 degrees (example: San Francisco)
lon = int(-86.5852 * 1e7) # Longitude in 1E-7 degrees
alt = int(500 * 1000)      # Altitude in millimeters (example: 500m = 500,000mm)
course = int(9000)             # Heading in centi-degrees (90.00° = 9000)
gnd_spd = int(300)              # Horizontal velocity in cm/s
climb_rate = int(0)                # Vertical velocity in cm/s
callsign = ("ABCD1234" + "\0")[:9]            # Callsign (up to 8 characters, pad if shorter)
callsign = callsign.encode("ascii", errors="replace")
emitter_type = int(0)                # Emitter type (default: No info)
tslc = int(0)                        # Time since last communication in seconds
flags = bin(3)                   # Flags: position, altitude, and heading are valid
squawk = int(0)

master = connect_to_mavproxy('127.0.0.1', 14552)

# Send the ADSB_VEHICLE message
print('Sending ADS-B message')
master.mav.adsb_vehicle_send(
    icao,
    lat,
    lon,
    alt,
    0,
    course,
    gnd_spd,
    climb_rate,
    callsign,
    emitter_type,
    tslc,
    flags,
    squawk
)

print('Message sent.')
