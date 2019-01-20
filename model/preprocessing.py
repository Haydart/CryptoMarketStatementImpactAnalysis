import numpy as np


def normalize_array(array):
    normalized = (array - min(array)) / (max(array) - min(array))
    return normalized


# create new dataset with X and Y for prediction
# data - numpy array
# look_back - the number of previous time steps to use as input variables to predict the next time period
def get_sentiments_prices(sentiments1, prices, look_back=1):
    x, y = [], []
    for i in range(len(sentiments1) - look_back):
        x.append(sentiments1[i])
   #     x.append([sentiments1[i], sentiments2[i]])
        y.append(prices[i + look_back])
    return np.array(x), np.array(y)


def shuffle_data(x, y):
    s = np.arange(x.shape[0])
    np.random.shuffle(s)
    return x[s], y[s]


def split(x):
    train_size = int(len(x) * 0.8)
    train = x[0:train_size]
    test = x[train_size:]
    return train, test


