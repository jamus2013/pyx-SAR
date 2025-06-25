# Script for automatically updating PiAware receiver position using known lat/long
# How to run:
#    sudo python update-adsb-rx-pos.py 34.<lat> -86.<lon>

import argparse
import re
import subprocess

CONFIG_PATH = "/etc/default/dump1090-fa"

def update_config(lat, lon):
    try:
        with open(CONFIG_PATH, 'r') as file:
            lines = file.readlines()

        # Update or add the lines for lat/lon
        updated_lines = []
        lat_set, lon_set = False, False
        for line in lines:
            if line.startswith("RECEIVER_LAT="):
                updated_lines.append(f"RECEIVER_LAT={lat}\n")
                lat_set = True
            elif line.startswith("RECEIVER_LON="):
                updated_lines.append(f"RECEIVER_LON={lon}\n")
                lon_set = True
            else:
                updated_lines.append(line)

        if not lat_set:
            updated_lines.append(f"RECEIVER_LAT={lat}\n")
        if not lon_set:
            updated_lines.append(f"RECEIVER_LON={lon}\n")

        with open(CONFIG_PATH, 'w') as file:
            file.writelines(updated_lines)

        print(f"Updated receiver position to: {lat}, {lon}")

    except PermissionError:
        print("Permission denied — try running this script with sudo.")
        exit(1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

def restart_dump1090():
    try:
        subprocess.run(["sudo", "systemctl", "restart", "dump1090-fa"], check=True)
        print("dump1090-fa restarted successfully.")
    except subprocess.CalledProcessError:
        print("Failed to restart dump1090-fa.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update dump1090-fa receiver position.")
    parser.add_argument("latitude", type=float, help="Receiver latitude (e.g. 34.1234)")
    parser.add_argument("longitude", type=float, help="Receiver longitude (e.g. -86.5678)")

    args = parser.parse_args()

    # Validate lat/lon ranges
    if not (-90 <= args.latitude <= 90 and -180 <= args.longitude <= 180):
        print("Invalid latitude or longitude value.")
        exit(1)

    update_config(args.latitude, args.longitude)
    restart_dump1090()