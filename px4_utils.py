import json
from shapely.geometry import MultiPoint
from shapely.geometry.polygon import Polygon

# DEPENDENCIES
# shapely

def parsePX4Plan(plan_file):
    with open(plan_file, 'r') as file:
        mission_data = json.load(file)

    # GEOFENCE
    geofence = mission_data.get('geoFence', {}).get('polygons', [])
    if geofence:
        polygon = geofence[0].get('polygon', [])
        # Format coordinates into the desired string format
        formatted_polygon = '[' + ','.join(f"[{coord[1]},{coord[0]}]" for coord in polygon) + ']'
        geofence = f'geofence_polygon = \'{formatted_polygon}\''
    else:
        geofence = "geofence_polygon = '[]'"
    #print(geofence)

    # WAYPOINTS - BOUNDING BOX
    waypoints = mission_data.get('mission', {}).get('items', [])
    if waypoints:
        # Extract all latitudes and longitudes
        points = [(wp.get('params', [None])[5], wp.get('params', [None])[4]) for wp in waypoints]
        points = [point for point in points if point != (0, 0)]

        # Create a shapely MultiPoint object and compute the convex hull
        multi_point = MultiPoint(points)
        convex_hull = multi_point.convex_hull

        # Get coordinates of the convex hull
        if convex_hull.geom_type == 'Polygon':
            coords = list(convex_hull.exterior.coords)
        elif convex_hull.geom_type == 'MultiPolygon':
            coords = list(convex_hull[0].exterior.coords)
        else:
            coords = []

        # Format the coordinates into the required string format
        formatted_hull = '[' + ','.join(f"[{coord[0]},{coord[1]}]" for coord in coords) + ']'
        wp_bounding_box = f'convex_hull = \'{formatted_hull}\''
    else:
        wp_bounding_box = "convex_hull = '[]'"
    #print(wp_bounding_box)

    # WAYPOINTS (ROUTE)

    # RALLY POINTS

    return geofence, wp_bounding_box, rally_points
