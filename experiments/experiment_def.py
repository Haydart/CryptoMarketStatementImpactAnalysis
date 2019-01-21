from model.preprocessing import normalize_array, get_sentiments_prices, split
from model.model import create_model, train, test, evaluate
from main import create_dataset
from twitter.data_loader.loader import load_tweets
from crypto.data_loader.loader import load_crypto_data
from RedditWrapper.data_loader import load_reddit_data
import numpy as np


def load_datasets():
    df_twitter = load_tweets("..//twitter//data//tweets_all.json")
    df_reddit = load_reddit_data("..//RedditWrapper//prepared_reddit_data.csv")
    df_crypto = load_crypto_data("..//crypto//data//BTC-USD_2015-2018_1min")
    return df_crypto, df_twitter, df_reddit


def run_expreminent(look_back, hidden_size, batch_size, epochs, dropout):
    df_crypto, df_twitter, df_reddit = load_datasets()
    dataset = create_dataset(df_crypto, df_twitter, df_reddit, 1)
    x, y = get_sentiments_prices(dataset['twitter_sentiments'], dataset["reddit_sentiments"], dataset["coin_price"], look_back)
    for i in x.shape[0]:
        x[i] = normalize_array(x[i])

    # split into train and test sets
    train_x, test_x = split(x)
    train_y, test_y = split(y)

    train_x = np.reshape(train_x, (train_x.shape[0], look_back, train_x.shape[1]))
    test_x = np.reshape(test_x, (test_x.shape[0], look_back, test_x.shape[1]))

    model = create_model(hidden_size=hidden_size, look_back=look_back, dropout=dropout)
    model = train(model, train_x, train_y, batch_size=batch_size, epochs=epochs)
    y_pred = test(model, test_x)
    score = evaluate(test_y, y_pred)
    print('Test Score: %.2f RMSE' % (score))
    return score
