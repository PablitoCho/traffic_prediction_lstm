import csv
import shapefile
# import geojson

csvfilename = '../data/20160824_5Min.01.csv'
sf = shapefile.Reader('../data/shapefiles/5181.shp')
outputfilename = '../data/shapefiles/5181_filtered.shp'

# fields = sf.fields
# 0: 'LINK_ID', 'C', 10, 0
# 1: 'F_NODE', 'C', 10, 0
# 2: 'T_NODE', 'C', 10, 0
# 4: 'LANES', 'N', 19, 8
# 5: 'ROAD_RANK', 'C', 3, 0
# 9: 'MAX_SPD', 'N', 19, 8
shapes = sf.shapes()


# get all LINK_ID's from csv
link_speed_dict = {}
with open(csvfilename, 'r') as csvfile:
    for row in csv.reader(csvfile):
        link_id = row[1]
        link_speed_dict[link_id] = row[2]  # speed

w = shapefile.Writer(shapeType=shapefile.POLYLINE)
w.field('LINK_ID', 'C', 10, 0)
w.field('LANES', 'N', 2, 0)
w.field('ROAD_RANK', 'C', 3, 0)
w.field('MAX_SPD', 'N', 3, 0)

# filter out unused link id
for shape_rec in sf.iterShapeRecords():
    link_id = shape_rec.record[0]

    if link_id in link_speed_dict:
        lanes = shape_rec.record[4]
        road_rank = shape_rec.record[5]
        max_speed = shape_rec.record[9]
        w.record(link_id, int(lanes), road_rank, int(max_speed))
        w._shapes.append(shape_rec.shape)

w.save(outputfilename)
