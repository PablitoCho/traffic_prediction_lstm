# merge data file (from Pandas) with shapefiles to create shapefiles (.shp)
# with mapnik xml files (.mml)
import json

import pandas
import shapefile
import pyproj
import geojson


INPUT_SHAPE_FILE = '../data/shapefiles/900913.shp'
INPUT_TREND_FILE = '../data/speed/trend.h5'
OUTPUT_FILE = '../data/links.geojson'


def convert_to_latlng(coordinate):
    return pyproj.transform(epsg900931, epsg3857, *coordinate)


trends = pandas.read_hdf(INPUT_TREND_FILE, 'series')
sf = shapefile.Reader(INPUT_SHAPE_FILE)

epsg900931 = pyproj.Proj('+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs')
epsg3857 = pyproj.Proj(init='EPSG:4326')

features = []
for shape_rec in sf.iterShapeRecords():
    link_id = shape_rec.record[0]
    if link_id not in trends.columns:
        continue

    geom = shape_rec.shape.__geo_interface__
    coordinates = geom.get('coordinates', ())
    if geom['type'] is 'MultiLineString':
        coordinates = map(lambda x: list(map(convert_to_latlng, x)),
                          coordinates)
    else:
        coordinates = map(convert_to_latlng, coordinates)
    geom['coordinates'] = list(coordinates)

    feature = {
        'type': 'Feature',
        'properties': {
            'id': link_id
        },
        'geometry': geom
    }

    features.append(feature)

with open(OUTPUT_FILE, 'w') as f:
    json.dump({'type': 'FeatureCollection', 'features': features}, f)

with open(OUTPUT_FILE, 'r') as f:
    # validate
    dumps = f.read()
    obj = geojson.loads(dumps)
    print(obj.is_valid)
