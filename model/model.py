from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot
import math


def create_model(hidden_size, look_forward, dropout):
    model = Sequential()
    model.add(LSTM(hidden_size, input_shape=(look_forward, 3)))
 #   model.add(Dropout(dropout))
    model.add(Dense(1))
    return model


def train(model, train_x, train_y, test_x, test_y, batch_size, epochs):

    model.compile(loss='mae', optimizer='adam')
    history = model.fit(x=train_x, y=train_y, epochs=epochs, batch_size=batch_size, verbose=2, shuffle=False,
                        validation_data=(test_x, test_y))
    pyplot.plot(history.history['loss'], label='train')
    pyplot.plot(history.history['val_loss'], label='test')
    pyplot.legend()
    pyplot.show()
    return model


def test(model, test_x):
    y_pred = model.predict(test_x)
    return y_pred


def evaluate(y_true, y_pred):
    score = math.sqrt(mean_squared_error(y_true, y_pred))
    return score






