# create data file which contains slopes
# NOTICE: it takes long time to generate the output
# import numba
import numpy
import pandas

TRAFFIC_FILE = '../data/speed/combined.h5'
OUTPUT_FILE = '../data/speed/slope.h5'
N_TREND_SAMPLE = 6  # 5 minutes each


# @numba.jit
def get_slope(data):
    # return numpy.polyfit(numpy.arange(0, data.shape[0]), data, deg=1)[0]
    return numpy.polyfit(numpy.arange(0, data.values.shape[0]), data.values,
                         deg=1)[0]


# @numba.jit
def calculate_trend(speed_data):
    # return speed_data.resample('%dT' % 5 * N_TREND_SAMPLE).apply(
    #         lambda x: get_slope(x.values))
    return speed_data.resample('%dT' % 5 * N_TREND_SAMPLE).apply(get_slope)
    # 1. reshape
    # data = numpy.resize(speeds, (int(speeds.shape[0] / N_TREND_SAMPLE),
    #                              N_TREND_SAMPLE))
    # indices = speeds.Index.resize()
    # speeds.resize((int(speeds.shape[0] / N_TREND_SAMPLE), N_TREND_SAMPLE))
    # return numpy.apply_along_axis(get_slope, 1, data)


# @numba.jit
def get_trends(data):
    # process the traffic file
    return data.apply(calculate_trend, axis=0)


if __name__ == '__main__':
    data = pandas.read_hdf(TRAFFIC_FILE, 'series')
    data = data.sample(3000, axis=1)

    print('processing')
    trends = get_trends(data)
    trends.to_hdf(OUTPUT_FILE, 'series')
    # from timeit import timeit
    # print(timeit(lambda: get_trends(data), number=1))
