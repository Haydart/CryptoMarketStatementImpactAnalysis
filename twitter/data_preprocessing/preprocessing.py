import glob
import json
import pandas as pd
import re
import numpy as np
from datetime import datetime, timedelta
from CryptoStatementImpactAnalysis.model.utils import get_data_from_to


def file_to_dataframe(file_path):
    data = []
    with open(file_path, encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    print(file_path + ' loaded')
    return pd.DataFrame(data)


def join_files_to_dataframe(files):
    file_list = glob.glob(files + "/*.json")
    data = []
    for file in file_list:
        with open(file, encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line))
    return pd.DataFrame(data)


def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\ / \ / \S+)", " ", tweet).split())


def get_unique_tweets(dataframe):
    return dataframe.drop_duplicates(subset='id')


def sort_by(dataframe, sort_column):
    return dataframe.sort_values(by=sort_column, ascending=False)


def date_and_time(row):
    return row["date"] + " " + row["time"]


# window_time - now in days
def create_datetime_sentiment_dataset(data_path, window_time):
    dataset = pd.DataFrame(columns=["sentiment_avg", "date_time"])
    files = glob.glob(data_path + "/*.json")
    time_delta = timedelta(days=window_time)
    date_format = "%Y-%m-%d %H:%M:%S"

    for file in files:
        with open(file, encoding='utf-8') as data_file:
            json_file = json.load(data_file)
            #       df = pd.DataFrame.from_dict(json_file)
            df = pd.DataFrame(json_file)
            df = get_unique_tweets(df)
            df = df.sort_values(by=["date", "time"])

            date_times = [datetime.strptime(date_and_time(row), date_format) for _, row in df.iterrows()]
            df["datetime"] = date_times

            start_date_time = date_times[0].date()
            end_date_time = date_times[-1].date()

            while start_date_time <= end_date_time:
                df2 = get_data_from_to(df, "datetime", start_date_time, start_date_time + time_delta)
                if not df2.empty:
                    sentiment_avg = np.mean(df2["sentiment"])
                    dataset.loc[len(dataset)] = [sentiment_avg, start_date_time]
                start_date_time += time_delta

    return dataset


