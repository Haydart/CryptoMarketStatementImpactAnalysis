from CryptoStatementImpactAnalysis.twitter.data_preprocessing.preprocessing import join_files_to_dataframe, file_to_dataframe, sort_by
import os


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
