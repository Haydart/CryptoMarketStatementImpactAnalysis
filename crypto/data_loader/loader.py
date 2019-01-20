import pandas as pd
import numpy as np
import glob
from datetime import timedelta


def load_crypto_data(file_path):
    files = glob.glob(file_path + "/*.csv")
    result = []

    for file in files:
        df = pd.read_csv(file, header=0)
        result.append(df)
    return pd.concat(result, axis=0)


def get_average(data):
    return np.mean(data)


def get_avg_open_close(df, date_column_name):
    dataset = pd.DataFrame(columns=["price_avg", "datetime"])
    df[date_column_name] = pd.to_datetime(df[date_column_name])
    df = df.sort_values(by=[date_column_name])

    start_date_time = df[date_column_name].iloc[0].replace(minute=0, second=0)
    end_date_time = df[date_column_name].iloc[-1].replace(minute=0, second=0)

    time_window = timedelta(hours=2)

    start = start_date_time
    i = 0

    while i < len(df) and start_date_time <= end_date_time:
        open = []
        close = []

        end = start + time_window
        while i < len(df) and df[date_column_name].iloc[i].replace(minute=0, second=0) < end:
            open.append(df["Open"].iloc[i])
            close.append(df["Close"].iloc[i])
            i += 1

        start = start + time_window
        if len(open) == 0:
            continue

        open_avg = get_average(open)
        close_avg = get_average(close)

        dataset.loc[len(dataset)] = [(open_avg + close_avg)/2, start_date_time]
    return dataset
