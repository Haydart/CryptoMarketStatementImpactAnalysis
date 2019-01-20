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


def create_dataset(df_twitter, df_reddit, df_coin, time_window_min):
    dataset = pd.DataFrame(columns=["twitter_sentiments", "coin_price", "datetime"])

    df_twitter["datetime"] = [datetime.strptime(row["date"] + " " + row["time"], "%Y-%m-%d %H:%M:%S") for _, row in df_twitter.iterrows()]
 #   df_reddit["datetime"] = pd.to_datetime(df_reddit["datetime"])
    df_coin["datetime"] = pd.to_datetime(df_coin["Date"])

    df_twitter = sort_by_date(df_twitter)
#    df_reddit = sort_by_date(df_reddit)
    df_coin = sort_by_date(df_coin)

    window_time = timedelta(minutes=time_window_min)
    start_date = find_start_date(df_twitter, df_coin).replace(second=0)
    end_date = find_end_date(df_twitter, df_coin).replace(second=0)

    df_twitter = get_data_from_to(df_twitter, "datetime", start_date, end_date)
    df_coin = get_data_from_to(df_coin, "datetime", start_date, end_date)

    start_date2 = find_start_date(df_twitter, df_coin).replace(second=0)
    while start_date2 != start_date:
        df_twitter = get_data_from_to(df_twitter, "datetime", start_date2, end_date)
        df_coin = get_data_from_to(df_coin, "datetime", start_date2, end_date)
        start_date = start_date2
        start_date2 = find_start_date(df_twitter, df_coin).replace(second=0)


    while start_date <= end_date:
        start = start_date
        tweets = []
        reddits = []
        coins_prices = []

        end = start + window_time
        while start < end:
            for _, tweet in df_twitter.iterrows():
                if tweet["datetime"] < end:
                    tweets.append(tweet["tweet"])
                else:
                    break

            for _, coin in df_coin.iterrows():
                if coin["datetime"] < end:
                    coins_prices.append(np.mean([coin["Open"], coin["Close"]]))
                else:
                    start += window_time
                    break

        tweets_sentiment_avg = get_avg_sentiments(tweets)
 #       reddits_sentiment_avg = get_avg_sentiments(reddits)
        coins_prices_avg = np.mean(coins_prices)

        dataset.loc[len(dataset)] = [tweets_sentiment_avg, coins_prices_avg, start_date]
        start_date += window_time

    dataset.to_csv("dataset.csv")
    print("Saved")
    print(dataset.head())
    return dataset


def find_start_date(df_twitter, df_coin):
    start_date_coins = df_coin["datetime"].iloc[0]
    start_date_sm = df_twitter["datetime"].iloc[0]
#    start_date_sm = min(df_twitter["datetime"].iloc[0], df_reddit["datetime"].iloc[0])
    return max(start_date_coins, start_date_sm)


def find_end_date(df_twitter, df_coin):
    end_date_coins = df_coin["datetime"].iloc[-1]
    end_date_sm = df_twitter["datetime"].iloc[-1]
#    start_date_sm = max(df_twitter["datetime"].iloc[-1], df_reddit["datetime"].iloc[-1])
    return min(end_date_coins, end_date_sm)


def sort_by_date(df):
    return df.sort_values(by='datetime')


def train_and_test(look_back, hidden_size, batch_size, epochs, dropout):
    dataset = create_dataset(df_twitter, None, df_crypto, 1)
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

