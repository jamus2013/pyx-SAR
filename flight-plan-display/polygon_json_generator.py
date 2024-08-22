from shape_utils import generateJSONPolygon
import json

vertices = '[[-86.56598703,34.72974881],[-86.57424748,34.72982136],[-86.57461321,34.73328307],[-86.57468888,34.73443349],[-86.57153603,34.73439203],[-86.56671849,34.73213264],[-86.56610052986903,34.73045360224115],[-86.56598703,34.72974881]]'


# Put together main shape string for JSON
json_string = generateJSONPolygon('MyPolygon','Polygon',vertices,'OOOOFF',1,1,0.1)

# print(json_string)
print('Writing shape file..')
data = json.loads(json_string)
with open('output.json', 'w') as json_file:
    json.dump(data, json_file)
print('Shape file saved')