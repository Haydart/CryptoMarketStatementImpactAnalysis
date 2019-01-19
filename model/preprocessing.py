import numpy as np
from sklearn.preprocessing import MinMaxScaler


def normalize_array(array):
    scaler = MinMaxScaler(feature_range=(0, 1))
    return scaler.fit_transform(array)


# create new dataset with X and Y for prediction
# data - numpy array
# look_back - the number of previous time steps to use as input variables to predict the next time period
def get_sentiments_prices(sentiments, prices, look_back=1):
    x, y = [], []
    for i in range(len(sentiments) - look_back):
        x.append(sentiments[i])
        y.append(prices[i + look_back])
    return np.array(x), np.array(y)


