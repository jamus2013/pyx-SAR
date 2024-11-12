def publish_location(device_id, lat, lon, connect_key, timestamp):
    # STREAM POSITION TO CALTOPO API
    # Enable debug_true to display data being broadcasted
    import requests

    endpoint = f'https://caltopo.com/api/v1/position/report/{connect_key}?id={device_id}&lat={lat}&lng={lon}'
    #print(endpoint)    # Uncomment to debug URL
    r = requests.get(url=endpoint)
    if r.status_code == 200:
        # print(f'Updated location to {lat}, {lon}') # Uncomment to display lat/long
        print(f'{device_id} position updated {timestamp}')
    else:
        print(f'Upload failed, error code {r.status_code}')
    return r.status_code

