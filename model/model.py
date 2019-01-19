from keras.models import Sequential
from keras.layers import Dense, LSTM
from utils import split, merge_datasets_by_date
from preprocessing import normalize_array, get_sentiments_prices
from crypto.data_loader.loader import load_crypto_data, get_avg_open_close
from twitter.data_loader.loader import load_sentiment_time_data
import numpy as np


hidden_size = 4
batch_size = 50
look_back = 1


twitter_data = load_sentiment_time_data("C:\\STUDIA\\Analiza-mediow-spolecznosciowych\\Crypto\\CryptoStatementImpactAnalysis\\twitter\\data\\BTC\\influencers\\BMouler.json_sentiments-2h.csv")
crypto_dataset = load_crypto_data("C:\STUDIA\Analiza-mediow-spolecznosciowych\Crypto\CryptoStatementImpactAnalysis\crypto\data\BTC-USD_2015-2018_1min\gemini_BTCUSD_2015_1min.csv")
crypto_dataset = get_avg_open_close(crypto_dataset, "Date")

dataset = merge_datasets_by_date(crypto_dataset, twitter_data, "datetime")

# normalize the dataset
dataset = get_sentiments_prices(dataset['sentiment_avg'], dataset['price_avg'], look_back)
#dataset2 = normalize_array(dataset)

sentiments = dataset[0]
prices = dataset[1]

# split into train and test sets
train_x, test_x = split(sentiments)
train_y, test_y = split(prices)

# reshape input to be [samples, time steps, features]
train_x = np.reshape(train_x, (train_x.shape[0], look_back, train_x.shape[1]))
test_x = np.reshape(test_x, (test_x.shape[0], look_back, test_x.shape[1]))

# create and fit the LSTM network
model = Sequential()
model.add(LSTM(hidden_size, input_shape=(1, look_back), dropout=0.2))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(train_x, train_y, epochs=100, batch_size=batch_size)

y_pred = model.predict(test_x)
