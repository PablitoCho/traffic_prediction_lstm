# create trend data
import pandas

INPUT_FILE = '../data/speed/slope.h5'
OUTPUT_FILE = '../data/speed/trend.%s'
GETTING_BETTER_THRESHOLD = 0.8
GETTING_WORSE_THRESHOLD = -0.5


def conditional_trend(slope):
    if slope > GETTING_BETTER_THRESHOLD:
        return 1
    elif slope < GETTING_WORSE_THRESHOLD:
        return -1
    else:
        return 0


def set_trends(slope_data):
    return slope_data.apply(conditional_trend)


if __name__ == '__main__':
    data = pandas.read_hdf(INPUT_FILE, 'series')

    trends = data.apply(set_trends, axis=0)
    trends.to_hdf(OUTPUT_FILE % ('h5'), 'series')
    trends.to_csv(OUTPUT_FILE % ('csv'))
