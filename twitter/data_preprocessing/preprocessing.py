import glob
import json
import pandas as pd
import re
from datetime import datetime
from sentiment_analyzer import avg_sentiments_from_text_in_time


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


def create_datetime_sentiment_for_file(file, date_format, window_size):
    with open(file, encoding='utf-8') as data_file:
        json_file = json.load(data_file)
        df = pd.DataFrame(json_file)
        df = get_unique_tweets(df)
        df = df.sort_values(by=["date", "time"])

        date_times = [datetime.strptime(date_and_time(row), date_format) for _, row in df.iterrows()]
        df["datetime"] = date_times
        return avg_sentiments_from_text_in_time(df, "tweet", "datetime", window_size)


# window_time - now in days
def create_datetime_sentiment_dataset(data_path, window_size):
    date_format = "%Y-%m-%d %H:%M:%S"
    files = glob.glob(data_path + "/*.json")
    for file in files:
        dataset = create_datetime_sentiment_for_file(file, date_format, window_size)
        dataset.to_csv(file + "_sentiments.csv")
        print("saved")
