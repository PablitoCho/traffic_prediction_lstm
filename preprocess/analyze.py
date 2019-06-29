from glob import glob
import pandas
from matplotlib import pyplot

DATA_GLOB = '../data/speed/20*.h5'
link_id = '1020001100'


def get_series(link_id):
    data = pandas.DataFrame()
    for hdf_file in sorted(glob(DATA_GLOB)):
        _data = pandas.read_hdf(hdf_file, 'series')
        print(_data.shape)
        data = pandas.concat([data, _data[link_id]])

    x = data.index.to_pydatetime()
    y = data.values
    return pandas.Series(y.transpose()[0], x)


series = get_series(link_id)

pyplot.subplot(211)
ts = series.resample('30T')
tsint = ts.interpolate(method='cubic')
tsint.plot()

pyplot.subplot(212)
pyplot.plot(series)

pyplot.show()
# x_ = numpy.arange(len(x))
# p = scipy.polyfit(x_, y, deg=80)
# y_ = scipy.polyval(p, x_)
# pyplot.plot(x, y_)
# pyplot.show()

# pyplot.plot(x, y)
# pyplot.show()
