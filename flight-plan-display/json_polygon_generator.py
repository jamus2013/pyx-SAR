from shape_utils import generateJSONfeature
from qgc_plan_parser import get_geofence_points
from qgc_plan_parser import get_waypoints
import json

# Read in QGC mission file
plan_file = 'maple_hill.plan'
print('Importing QGC mission file...')
with open(plan_file, 'r') as f:
    plan_data = json.load(f)

# Extract geofence
print('Parsing mission file...')
geofence_vertices = get_geofence_points(plan_data)
mission_points = get_waypoints(plan_data)

# Put together main shape string for JSON
geofence_string = generateJSONfeature('UAS Geofence','Polygon',geofence_vertices,'OOOOFF',1,1,0.1,'KQ4VFH')
waypoints_string = generateJSONfeature('UAS Flightpath','LineString',mission_points,'OOFF00',1,1,0.1,'KQ4VFH')
json_string = (
    f'{{"features":['
    f'{geofence_string},'
    f'{waypoints_string}'
    f'],"type":"FeatureCollection"}}'
)

# print(json_string)
print('Writing CalTopo shape file..')
data = json.loads(json_string)
with open('uas_flight_plan.json', 'w') as json_file:
    json.dump(data, json_file)
print('Shape file saved')