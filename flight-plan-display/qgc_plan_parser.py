import json

# Extract geofence vertices from mission file
def get_geofence_points(plan_data):
    geofence_vertices = []
    # Detect presence of polygon geofence(s)
    if "geoFence" in plan_data and "polygons" in plan_data["geoFence"]:
        print('Detecting geofence...')
        # Parse polygon points
        for polygon in plan_data["geoFence"]["polygons"]:
            geofence_vertices.extend([[point[1], point[0]] for point in polygon["polygon"]])
    return geofence_vertices

# Extract mission waypoints from mission file
def get_waypoints(plan_data):
    waypoints = []
    # Detect presence of valid waypoints
    if "mission" in plan_data and "items" in plan_data["mission"]:
        print('Detecting waypoints...')
        for item in plan_data["mission"]["items"]:
            # Filter to only get takeoff, landing, waypoint, or RTL points
            if "command" in item and item["command"] in [16, 21, 22, 30]:
                # Detect LLA and parse points
                if "params" in item and len(item["params"]) >= 6:
                    lat = item["params"][4]
                    lon = item["params"][5]
                    alt = item["params"][6]
                    waypoints.append([lon,lat])    # Add in alt if it were available
    return waypoints

# Extract rally points from mission file
def get_rally_points(plan_data):
    rally_points = []
    # Detect valid rally point(s) and parse points
    if "rallyPoints" in plan_data and "points" in plan_data["rallyPoints"]:
        print('Detecting rally point(s)...')
        for point in plan_data["rallyPoints"]["points"]:
            lat = point[0]
            lon = point[1]
            alt = point[2]
        rally_points.append((lat,lon))  # Add in alt if it were supported
    return rally_points

def main(plan_file):
    # Read QGC *.plan file
    print("Parsing mission file...")
    with open(plan_file, 'r') as f:
        plan_data = json.load(f)

    # Parse plan file
    geofence_vertices = get_geofence_points(plan_data)
    waypoints = get_waypoints(plan_data)
    rally_points = get_rally_points(plan_data)

    # Preview results
    print("\nGeofence vertices:")
    print(geofence_vertices)
    print("\nWaypoints:")
    print(waypoints)
    print("\nRally points:")
    print(rally_points)

if __name__ == "__main__":
    plan_file = '../example-data/maple-hill.plan'   # Replace with import tool!
    main(plan_file)