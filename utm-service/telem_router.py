import subprocess
import re

baud = 115200   # Baudrate for telemetry stream
ip_address = '127.0.0.1'    # IP address for MAVLink router
port_1 = 14550  # QGC port
port_2 = 14551  # gps_relay port
port_3 = 14552  # piaware port?


def start_mavproxy(baud,udp_ip_address,udp_port_1,udp_port_2,udp_port_3):
    # Start running MAVProxy MAVLink router (UDP)
    command = (f'mavproxy.py --master={get_port_number()} --baudrate {baud} --out {udp_ip_address}:{udp_port_1} --out {udp_ip_address}:{udp_port_2} --out {udp_ip_address}:{udp_port_3}')
    print(command)
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Command failed with error: {e}')


def get_port_number():
    # Gets port number of most recent USB device to help identify SiK radio or Cube
    # NOTE: May require password
    print('Detecting telemetry system..')
    try:
        # Get the dmesg output
        dmesg_output = subprocess.check_output(['sudo', 'dmesg'], universal_newlines=True)

        # Search for ttyACM or ttyUSB devices
        tty_devices = re.findall(r'(ttyACM\d+|ttyUSB\d+)', dmesg_output)

        if tty_devices:
            # Return the most recent tty device found
            print(f'Device found at /dev/{tty_devices[-1]}')
            return f"/dev/{tty_devices[-1]}"
        else:
            print("No tty devices found.")
            return None
        
    except subprocess.CalledProcessError as e:
        print(f"Error running dmesg: {e}")
        return None


if __name__ == '__main__':
    start_mavproxy(baud, ip_address, port_1, port_2, port_3)

   