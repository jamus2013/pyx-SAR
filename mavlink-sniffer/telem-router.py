#import subprocess
#import re

def start_mavproxy(baud,udp_ip_address,udp_port):
    import subprocess
    command = (f'mavproxy.py --master={get_port_number()} --baudrate {baud} --out {udp_ip_address}:{udp_port}')
  
    print(command)

    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Command failed with error:{e}')


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


if __name__ == '__main__':
    start_mavproxy(57600, '127.0.0.1',14550)
   