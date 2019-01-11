from textblob import TextBlob
import glob
import os
import json
import pandas as pd
import re


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


# FINDING INFLUENCERS IN TWEETS
def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\ / \ / \S+)", " ", tweet).split())


def sort_by(dataframe, sort_column):
    return dataframe.sort_values(by=sort_column, ascending=False)


def group_by_username(dataframe):
    return dataframe.groupby(['username'], as_index=False)['retweets', 'likes', 'replies'].sum()


def filter_more_than_zero(dataframe):
    df = dataframe[dataframe['retweets'] > 0]
    return df[df['likes'] > 0]


def find_influencers_in_tweets(file_path, number):
    if os.path.isdir(file_path):
        df = join_files_to_dataframe(file_path)
    else:
        df = file_to_dataframe(file_path)
    df = group_by_username(df)
    df = filter_more_than_zero(df)
    df = sort_by(df, 'retweets')
    return df.head(number)


def find_influencers_in_stats(file_path, number):
    df = file_to_dataframe(file_path)
    df = sort_by(df, 'followers')
    df = sort_by(df, 'likes')
    df = sort_by(df, 'tweets')
    return df.head(number)
