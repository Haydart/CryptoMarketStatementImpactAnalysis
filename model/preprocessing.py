import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


def parse_date(df, column_date_name):
    df[column_date_name] = pd.to_datetime(df[column_date_name])
    return df


def normalize_dataset(df):
    scaler = MinMaxScaler(feature_range=(0, 1))
    return scaler.fit_transform(df)


# create new dataset with X and Y for prediction
# data - numpy array
# look_back - the number of previous time steps to use as input variables to predict the next time period
def create_dataset(data, look_back=1):
    x, y = [], []
    for i in range(len(data) - look_back):
        x.append(data[i])
        y.append(data[i + look_back])
    return np.array(x), np.array(y)
