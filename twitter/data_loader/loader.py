import pandas as pd


def load_sentiment_time_data(file_path):
    df = pd.read_csv(file_path, header=0, index_col=0)
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df
