# merge shape file and data file (from raw csv)
import os
import csv
import shapefile
import glob
import numpy


INPUT_SHAPE_FILE = '../data/shapefiles/900913.shp'
TRAFFIC_FILE_GLOB = '../data/traffic/20160824_30min_*.csv'
OUTPUT_PATH = '../data/traffic/'
N_CLASSIFICATION = 15

_range = [1.5, 0.05]
SPEED_CLASSIFICATION_THRESHOLD = numpy.tanh(
    numpy.linspace(_range[0], _range[1], N_CLASSIFICATION))

sf = shapefile.Reader(INPUT_SHAPE_FILE)

# process the traffic files
for traffic_file_path in glob.glob(TRAFFIC_FILE_GLOB):
    link_speed_dict = {}
    otput_file_path = os.path.join(OUTPUT_PATH, os.path.splitext(
                        os.path.split(traffic_file_path)[-1])[0] + '.shp')
    with open(traffic_file_path, 'r') as csv_file:
        for row in csv.reader(csv_file):
            link_id = row[0]
            link_speed_dict[link_id] = float(row[1])  # speed

    w = shapefile.Writer(shapeType=shapefile.POLYLINE)
    w.field('LINK_ID', 'C', 10, 0)
    # w.field('F_NODE', 'C', 10, 0)
    # w.field('T_NODE', 'C', 10, 0)
    w.field('LANES', 'N', 2, 0)
    w.field('ROAD_RANK', 'C', 3, 0)
    w.field('MAX_SPD', 'N', 3, 0)
    w.field('AVG_SPD', 'N', 3, 0)
    w.field('TRAFFIC_CL', 'N', 2, 0)

    # filter out unused link id
    for shape_rec in sf.iterShapeRecords():
        link_id = shape_rec.record[0]

        if link_id not in link_speed_dict:
            continue

        lanes = shape_rec.record[4]
        road_rank = shape_rec.record[5]
        max_speed = shape_rec.record[9]
        avg_speed = link_speed_dict[link_id]

        # calculate the speed classification
        if max_speed <= 0:
            classfication = -1
        else:
            classification = numpy.abs(SPEED_CLASSIFICATION_THRESHOLD -
                                       avg_speed / max_speed).argmin()
        w.record(link_id, int(lanes), road_rank, int(max_speed),
                 int(avg_speed), classification)
        w._shapes.append(shape_rec.shape)

    w.save(otput_file_path)
