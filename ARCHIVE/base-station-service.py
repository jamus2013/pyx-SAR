import time
import getpass


def main():
    refresh_rate        = 2                 # Position update period [s]
    logging_enabled     = False
    
    device_id   = input("Enter CalTopo device ID: ")  # User inputs CalTopo trackable device name
    key         = getpass.getpass("Enter CalTopo Connect Key: ")    # User inputs CalTopo access URL connect key

    link = connectUAS(baud)  # Open telemetry link
    if logging_enabled == True:
        log_file        = generateLogFile()     # Create CSV file(name) using current system time
    while True:
        if link is not None :
            lat, lon, time_stamp = getUASPosition(link)         # Get global position and time
            # print('Latitude = %f \t\t Longitude = %f' % (lat, lon))   # Uncomment for position debug
            response = publishLocation(device_id, lat, lon, key)  # Upload position updates to Caltopo
            if logging_enabled == True:
                logDataStream(log_file,time_stamp, lat, lon, response)
            time.sleep(refresh_rate)    # Delay to stagger CalTopo upload
        else:
            break





def logDataStream(log_path, t, lat, lon, status):
    import csv
    # WRITE DATA STREAM TO CSV LOG FILE
    line = [t, lat, lon, status]
    with open(log_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(line)


def generateLogFile():
    # GENERATES NEW LOG FILENAME USING CURRENT TIME
    import datetime
    import csv
    current_time    = datetime.datetime.now()
    timestamp       = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    filename        = f"base-station-svc_{timestamp}.csv"   # Initialize CSV named using current time
    header = ["Local Time [Y-M-D_h:m:s]", "Latitude [°N WGS84]", "Longitude [°E WGS84]", "HTTP Status"]  # Column headers
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
    return filename


if __name__ == '__main__':
    main()
