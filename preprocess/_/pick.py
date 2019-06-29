import os
import glob
import csv

INPUT_GLOB = '../data/traffic_trend_sample/*.csv'
OUTPUT_DIR = '../data/traffic_trend_sample'
OUTPUT_FILE = '%s_%03d.csv'

N_SAMPLE = 300

def _get_output(csv_filename, counter):
    f = os.path.splitext(os.path.basename(csv_filename))[0]
    return os.path.join(OUTPUT_DIR, OUTPUT_FILE % (f, counter))


if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

for csv_filename in glob.glob(INPUT_GLOB):
    print(csv_filename)
    with open(csv_filename, 'rb') as csv_file:
        _currentrow = None
        _counter = 1
        _f = open(_get_output(csv_filename, _counter), 'wb')
        writer = csv.writer(_f)

        for row in csv.reader(csv_file):
            if not _currentrow:
                _currentrow = row[0]
            elif _currentrow != row[0]:
                _currentrow = row[0]
                if _currentrow.endswith('00:00'):
                    # start new row
                    _f.close()
                    _counter += 1
                    _f = open(_get_output(csv_filename, _counter), 'wb')
                    writer = csv.writer(_f)

            writer.writerow(row)
