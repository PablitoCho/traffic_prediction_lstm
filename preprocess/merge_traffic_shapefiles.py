# merge data file (from Pandas) with shapefiles to create shapefiles (.shp)
# with mapnik xml files (.mml)
import os
import glob
from string import Template

import numpy
import pandas
import shapefile


INPUT_SHAPE_FILE = '../data/shapefiles/900913.shp'
TRAFFIC_FILE_GLOB = '../data/speed/*.h5'
OUTPUT_PATH = '../data/traffic/'
TEMPLATE_FILE = '../data/traffic/template.mml'

RESAMPLE_EVERY_MINIUTE = 30
OUTPUT_FILENAME = '%s_%dmin_%03d.shp'

N_CLASSIFICATION = 15
_range = [1.5, 0.5]
SPEED_CLASSIFICATION_THRESHOLD = numpy.tanh(
    numpy.linspace(_range[0], _range[1], N_CLASSIFICATION))

sf = shapefile.Reader(INPUT_SHAPE_FILE)

template_string = Template(open(TEMPLATE_FILE).read())

# process the traffic files
for traffic_file_path in glob.glob(TRAFFIC_FILE_GLOB):
    link_speed_dict = {}
    otput_file_path = os.path.join(OUTPUT_PATH, os.path.splitext(
                        os.path.split(traffic_file_path)[-1])[0] + '.shp')

    data = pandas.read_hdf(traffic_file_path, 'series')

    # change range from 5min to RESAMPLE_EVERY_MINIUTES
    data = data.resample('%dT' % (RESAMPLE_EVERY_MINIUTE)).mean()

    # for each time, create a seperate shape file
    for index, timestamp in enumerate(data.index):
        w = shapefile.Writer(shapeType=shapefile.POLYLINE)
        w.field('LINK_ID', 'C', 10, 0)
        # w.field('F_NODE', 'C', 10, 0)
        # w.field('T_NODE', 'C', 10, 0)
        w.field('LANES', 'N', 2, 0)
        w.field('ROAD_RANK', 'C', 3, 0)
        w.field('MAX_SPD', 'N', 3, 0)
        w.field('AVG_SPD', 'N', 3, 0)
        w.field('TRAFFIC_CL', 'N', 2, 0)

        for shape_rec in sf.iterShapeRecords():
            link_id = shape_rec.record[0]

            # filter out unused link id
            if link_id not in data:
                continue

            lanes = shape_rec.record[4]
            road_rank = shape_rec.record[5]
            max_speed = shape_rec.record[9]
            avg_speed = data[link_id][index]

            # calculate the speed classification
            if max_speed <= 0:
                classfication = -1
            else:
                classification = numpy.abs(SPEED_CLASSIFICATION_THRESHOLD -
                                           avg_speed / max_speed).argmin()
            w.record(link_id, int(lanes), road_rank, int(max_speed),
                     int(avg_speed), classification)
            w._shapes.append(shape_rec.shape)

        output_filename = OUTPUT_FILENAME % (
            timestamp.to_pydatetime().strftime('%Y%m%d'),
            RESAMPLE_EVERY_MINIUTE,
            index + 1
        )

        print(output_filename)
        w.save(os.path.join(OUTPUT_PATH, output_filename))

        # create the template file
        template_filename = os.path.join(
            OUTPUT_PATH, os.path.splitext(output_filename)[0] + '.mml')
        with open(template_filename, 'w') as f:
            f.write(template_string.substitute({'shapefile': output_filename}))
