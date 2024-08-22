import socket

piaware_IP  = '192.168.1.115'   # Manually set to piaware IP address
adsb_port   = 30005             # Manually update to match port
buffer_size = 4906              # Adjust as needed

def parse_adsb_data(data):
    # Example function to handle binary data
    print("Received data (hex):", data.hex())

def main():
    print("Test")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((piaware_IP, adsb_port))
        while True:
            data = s.recv(buffer_size)
            if not data:
                break
            parse_adsb_data(data)

if __name__ == '__main__':
    main()