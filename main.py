from datetime import datetime, timedelta
from twitter.data_loader.loader import load_tweets
from crypto.data_loader.loader import load_crypto_data
from sentiment_analyzer import get_avg_sentiments
from utils import get_data_from_to
import pandas as pd
import numpy as np
from model.preprocessing import normalize_array, get_sentiments_prices, split
from model.model import create_model, train, test


df_twitter = load_tweets(".//twitter//data//tweets_all.json")
df_crypto = load_crypto_data(".//crypto//data//BTC-USD_2015-2018_1min")


def create_dataset(df_coin, df_twitter, df_reddit, window_width):
    dataset = pd.DataFrame(columns=["twitter_sentiments", "reddit_sentiments", "coin_price", "datetime"])

    df_coin["datetime"] = pd.to_datetime(df_coin["Date"])
    df_twitter["datetime"] = [datetime.strptime(row["date"] + " " + row["time"], "%Y-%m-%d %H:%M:%S") for _, row in df_twitter.iterrows()]
    df_reddit["datetime"] = pd.to_datetime(df_reddit["datetime"])

    df_coin = sort_by_date(df_coin)
    df_twitter = sort_by_date(df_twitter)
    df_reddit = sort_by_date(df_reddit)

    coin_idx, twitter_idx, reddit_idx, window_start = find_start_date_idxs(df_coin, df_twitter, df_reddit)
    window_time = timedelta(minutes=window_width)

    while coin_idx < len(df_coin) and twitter_idx < len(df_twitter) and reddit_idx < len(df_reddit):
        tweets = []
        reddits = []
        coins_prices = []

        while df_coin["datetime"].iloc[coin_idx] <= window_start + window_time:
            coins_prices.append(np.mean([df_coin["Open"].iloc[coin_idx], df_coin["Close"].iloc[coin_idx]]))
            coin_idx += 1

        while df_twitter["datetime"].iloc[twitter_idx] <= window_start + window_time:
            tweets.append(df_twitter["tweet"].iloc[twitter_idx])
            twitter_idx += 1

        while df_reddit["datetime"].iloc[reddit_idx] <= window_start + window_time:
            reddits.append(df_reddit["text"].iloc[reddit_idx])
            reddit_idx += 1

        coins_prices_avg = np.mean(coins_prices)
        tweets_sentiment_avg = get_avg_sentiments(tweets)
        reddits_sentiment_avg = get_avg_sentiments(reddits)

        dataset.loc[len(dataset)] = [tweets_sentiment_avg, reddits_sentiment_avg, coins_prices_avg, window_start]
        window_start += window_time

    dataset.to_csv("dataset.csv")
    print("Saved")
    print(dataset.head())
    return dataset


def find_start_date_idxs(df_coin, df_twitter, df_reddit):
    start_date_coins = df_coin["datetime"].iloc[0].replace(second=0)
    start_date_twitter = df_twitter["datetime"].iloc[0].replace(second=0)
    start_date_reddit = df_reddit["datetime"].iloc[0].replace(second=0)

    coin_idx = 0
    twitter_idx = 0
    reddit_idx = 0

    if max(start_date_coins, start_date_twitter, start_date_reddit) == start_date_coins:
        start_date = start_date_coins
        while df_twitter["datetime"].iloc[twitter_idx + 1] < start_date_coins:
            twitter_idx += 1
        while df_reddit["datetime"].iloc[reddit_idx + 1] < start_date_coins:
            reddit_idx += 1

    elif max(start_date_coins, start_date_twitter, start_date_reddit) == start_date_twitter:
        start_date = start_date_twitter
        while df_coin["datetime"].iloc[coin_idx + 1] < start_date_twitter:
            coin_idx += 1
        while df_reddit["datetime"].iloc[reddit_idx + 1] < start_date_twitter:
            reddit_idx += 1

    elif max(start_date_coins, start_date_twitter, start_date_reddit) == start_date_reddit:
        start_date = start_date_reddit
        while df_coin["datetime"].iloc[coin_idx + 1] < start_date_reddit:
            coin_idx += 1
        while df_twitter["datetime"].iloc[twitter_idx + 1] < start_date_reddit:
            twitter_idx += 1

    return coin_idx, twitter_idx, reddit_idx, start_date





def find_end_date(df_twitter, df_coin):
    end_date_coins = df_coin["datetime"].iloc[-1]
    end_date_sm = df_twitter["datetime"].iloc[-1]
#    start_date_sm = max(df_twitter["datetime"].iloc[-1], df_reddit["datetime"].iloc[-1])
    return min(end_date_coins, end_date_sm)


def sort_by_date(df):
    return df.sort_values(by='datetime')


def train_and_test(look_back, hidden_size, batch_size, epochs, dropout):
    dataset = create_dataset(df_crypto, df_twitter, None, 1)
    x, y = get_sentiments_prices(dataset['twitter_sentiments'], dataset["coin_price"], look_back)
    x = normalize_array(x)

    # split into train and test sets
    train_x, train_y = split(x)
    test_x, test_y = split(y)

    train_x = np.reshape(train_x, (train_x.shape[0], look_back, train_x.shape[1]))
    test_x = np.reshape(test_x, (test_x.shape[0], look_back, test_x.shape[1]))

    model = create_model(hidden_size=hidden_size, look_back=look_back, dropout=dropout)
    model = train(model, train_x, train_y, batch_size=batch_size, epochs=epochs)
    y_pred = test(model, test_x)


train_and_test(look_back=1, hidden_size=4, batch_size=50, epochs=100, dropout=0.2)

