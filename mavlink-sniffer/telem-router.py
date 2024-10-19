#import subprocess
#import re

ip_address = '127.0.0.1'
port_1 = 14450
port_2 = 14451

def start_mavproxy(baud,udp_ip_address,udp_port_1,udp_port_2):
    # Start running MAVProxy MAVLink router (UDP)
    import subprocess
    command = (f'mavproxy.py --master={get_port_number()} --baudrate {baud} --out {udp_ip_address}:{udp_port_1} --out {udp_ip_address}:{udp_port_2}')
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Command failed with error: {e}')


def get_port_number():
    # Gets port number of most recent USB device
    # NOTE: May require password
    import subprocess
    import re
    print('Detecting ground radio..')
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

def get_gps_data(udp_ip_address, udp_port):
    # Extract state estimates from MAVLink stream in parallel to GCS instance
    import socket
    import time
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((udp_ip_address, udp_port))
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            printf(f'Received data from {addr}: {data}')
        except KeyboardInterrupt:
            print('Terminated by user')
            break
        except Exception as e:
            print(f'Error: {e}')
        time.sleep(1)


if __name__ == '__main__':
    start_mavproxy(57600, ip_address,port_1,port_2)
    #get_gps_data(ip_address, port_1)
   