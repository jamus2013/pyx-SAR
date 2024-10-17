def generateJSONfeature(shape_title, shape_type, vertices, color_rgb, stroke_width, stroke_opacity, fill_opacity, owner):

    import time
    import uuid
    unix_time = int(time.time())
    random_id = str(uuid.uuid4())   # Workaround?

    # CalTopo GeoJSON format (feature only)
    if shape_type == 'Polygon':
        feature_string = (
            f'{{"geometry":{{"coordinates":[{vertices}],"type":"{shape_type}"}},'
            f'"id":"{random_id}","type":"Feature",'
            f'"properties":{{"stroke-opacity":{stroke_opacity},"creator":"{owner}",'
            f'"description":"","stroke-width":{stroke_width},"title":"{shape_title}",'
            f'"fill":"#{color_rgb}","stroke":"#{color_rgb}","fill-opacity":{fill_opacity},'
            f'"class":"Shape","updated":{unix_time}}}}}'
        )
    elif shape_type == 'LineString':
        feature_string = (
            f'{{"geometry":{{"coordinates":{vertices},"type":"{shape_type}"}},'
            f'"id":"{random_id}","type":"Feature",'
            f'"properties":{{"stroke-opacity":{stroke_opacity},"creator":"{owner}","pattern":"solid",'
            f'"description":"","stroke-width":{stroke_width},"title":"{shape_title}",'
            f'"fill":"#{color_rgb}","stroke":"#{color_rgb}",'
            f'"class":"Shape","updated":{unix_time}}}}}'
        )

    return feature_string