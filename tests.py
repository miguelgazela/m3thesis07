from statistics import mean
import matplotlib.pyplot as plt

import numpy as np

# df = quandl.get('WIKI/GOOGL')
# df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']]
#
# df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100.0
# df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0
#
# df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]
#
# forecast_col = 'Adj. Close'
# df.fillna(-99999, inplace=True)
#
# forecast_out = int(math.ceil(0.01 * len(df)))
#
# df['label'] = df[forecast_col].shift(-forecast_out)
# df.dropna(inplace=True)
#
# X = np.array(df.drop(['label'], 1))
#
# print X
xs = np.array([1, 2, 3, 4, 5, 6], dtype=np.float64)
ys = np.array([5, 4, 6, 5, 6, 7], dtype=np.float64)



print "Foo Bar"
