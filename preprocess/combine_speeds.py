# combine speed data files into one big file
import glob

import pandas


INPUT_FILE_GLOB = '../data/speed/20*.h5'
OUTPUT_FILE = '../data/speed/combined.h5'

# process the traffic files
data = pandas.DataFrame()
for input_file_path in sorted(glob.glob(INPUT_FILE_GLOB)):
    _data = pandas.read_hdf(input_file_path, 'series')
    data = pandas.concat([data, _data], axis=0)

# remove ids with NA values
data = data.dropna(axis=1, how='any')
print(data.shape)
data.to_hdf(OUTPUT_FILE, 'series')
