import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import pandas as pd


# test_size: should be float [0.0, 1.0] - the proportion of the dataset to include in the test split.
# or int - the absolute number of test samples.
def split_dataset(df, test_size):
    train, test = train_test_split(df, test_size=test_size)
    return train, test


def get_data_from_to(df, column_date_name, time_from, time_to):
    df[column_date_name] = pd.to_datetime(df[column_date_name])
    mask = (df[column_date_name] > time_from) & (df[column_date_name] <= time_to)
    return df.loc[mask]


def plot_data(df, column_date_name, column_data_name):
    time = df[column_date_name]
    values = df[column_data_name]
    plt.plot(time, values)
    plt.show()
