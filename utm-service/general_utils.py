def get_system_time():
    # CREATE TIME STAMP BASED ON LOCAL SYSTEM TIME
    import datetime
    sys_time = datetime.datetime.now()
    return sys_time.strftime("%Y-%m-%d %H:%M:%S")

def dist_between_points(lat_lon1, lat_lon2):
    # Measure distance [km] between two points [WGS84]
    from geopy.distance import geodesic
    distance_km = geodesic(lat_lon1, lat_lon2).kilometers
    return distance_km
