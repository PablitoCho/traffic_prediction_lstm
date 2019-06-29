# parse raw csv files to create Pandas-compatiable speed files
from glob import glob
import pandas
import numpy

RAW_DATA_GLOB = '../data/raw/*.csv'
HEADERS = ['time', 'id', 'spd', 'traffic', *['_'] * 6]


def parse_csv_file(csv_file):
    df = pandas.read_csv(csv_file, header=None, names=HEADERS,
                         usecols=['time', 'id', 'spd', 'traffic'],
                         dtype={'id': str, 'spd': numpy.int32, 'traffic': numpy.int32},
                         parse_dates=['time'])

    # grouped = df.groupby('id')['spd']

    # remove duplicate time, id combinations
    filtered = df.drop_duplicates(subset=['time', 'id'], keep='last')

    # pivot to time / id table
    data = filtered.pivot(index='time', columns='id', values='traffic')

    # filter out wrong id
    data = data.drop([c for c in data.columns
                      if len(c) < 10 or c.startswith('Tmp')], axis=1)

    n_row = data.shape[0]

    # remove more than 30% are NA
    #data = data.drop([c for c in data.columns
    #                  if data[c].isnull().sum() > n_row * 0.3], axis=1)

    ## fill in NA with forward and backward fill
    #data = data.fillna(method='ffill').fillna(method='bfill')

    # period = 30  # minutes
    # reshape into traffic might improve or disimprove 30% given period

    # filter out little change ids

    # filter out low traffic ids

    # combine connected links and similar pattern

    return data


if __name__ == '__main__':
    # csv_file = '../data/raw/20160824_5m.csv'
    # print(type(parse_csv_file(csv_file)))

    # data = pandas.DataFrame()
    count = 1
    for csv_file in sorted(glob(RAW_DATA_GLOB)):
        parse_csv_file(csv_file).to_hdf('traffic_%s.h5' % (count), 'series')
        count += 1

    # save files
    # data.to_hdf('speed.h5', 'series')
