def generateJSONPolygon(shape_title, shape_type, vertices, stroke_color_rgb, stroke_width, stroke_opacity, fill_opacity):
    fill_color_rgb = stroke_color_rgb   # Remove to enable separate edge and fill colors

    json_string = (f'{{"features":[{{"geometry":{{"coordinates":[{vertices}],"type":"{shape_type}"}},'
                   f'"id":"6953b20e-aca0-4739-8fab-e9f8f6051dd9","type":"Feature","properties":{{"stroke-opacity":{stroke_opacity},'
                   f'"creator":"PHL7MC","description":"","stroke-width":{stroke_width},"title":"{shape_title}",'
                   f'"fill":"#{fill_color_rgb}","stroke":"#{stroke_color_rgb}","fill-opacity":{fill_opacity},'
                   f'"class":"Shape","updated":1724165341574}}}}],"type":"FeatureCollection"}}')

    return json_string