from keras.models import Sequential
from keras.layers import Dense, LSTM
from utils import create_dataset, split_dataset, normalize_dataset
import numpy as np


hidden_size = 4
batch_size = 50

# normalize the dataset
dataset = normalize_dataset(dataset)

# split into train and test sets
train, test = split_dataset(dataset, 0.2)

# reshape into X=t and Y=t+1
look_back = 1
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)

# reshape input to be [samples, time steps, features]
trainX = np.reshape(trainX, (trainX.shape[0], look_back, trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0], look_back, testX.shape[1]))

# create and fit the LSTM network
model = Sequential()
model.add(LSTM(hidden_size, input_shape=(1, look_back), dropout=0.2))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(trainX, trainY, epochs=100, batch_size=batch_size)

y_pred = model.predict(testX)
