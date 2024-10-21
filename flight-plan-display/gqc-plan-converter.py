import json
from PyQt5.QtWidgets import QApplication, QFileDialog
from shape_utils import generateJSONfeature
import os

def main():
    plan_file_path, plan_data = import_plan_file()
    if plan_data:
        # Parse plan file
        geofence_vertices = get_geofence_points(plan_data)
        waypoints = get_waypoints(plan_data)
        #rally_points = get_rally_points(plan_data)

        generate_geoJSON(plan_file_path, geofence_vertices, waypoints, None)


# Import *.plan file and extract data
def import_plan_file():
    app = QApplication([])
    plan_file_path, _ = QFileDialog.getOpenFileName(None, "Select QGC mission file")

    # Read QGC *.plan file
    if not plan_file_path:
        print("No file selected")
    else:
        print("Parsing mission file...")
        with open(plan_file_path, 'r') as f:
            plan_data = json.load(f)
        return plan_file_path, plan_data


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


def generate_geoJSON(src, fence_points, waypoints, rally_points):
    # Put together main shape string for JSON
    if fence_points:
        geofence_string = generateJSONfeature('UAS Geofence','Polygon',fence_points,'OOOOFF',1,1,0.1,'KQ4VFH')
    if waypoints:
        waypoints_string = generateJSONfeature('UAS Flightpath','LineString',waypoints,'OOFF00',1,1,0.1,'KQ4VFH')
    if rally_points:
        print("Rally points not yet supported")
    json_string = (
        f'{{"features":['
        f'{geofence_string},'
        f'{waypoints_string}'
        f'],"type":"FeatureCollection"}}'
    )

    # Default to writing geoJSON in same location as source *.plan
    destination = os.path.dirname(src)
    output_filename = os.path.basename(src) # Match geoJSON filename with original *.plan filename
    output_filename, _ = os.path.splitext(output_filename)

    # Export geoJSON
    print('Writing CalTopo shape file..')
    data = json.loads(json_string)
    with open(f'{destination}/{output_filename}.json', 'w') as json_file:
        json.dump(data, json_file)
    print('Shape file saved')


if __name__ == "__main__":
    #plan_file = '../example-data/maple-hill.plan'   # Replace with import tool!
    main()