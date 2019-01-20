from keras.models import Sequential
from keras.layers import Dense, LSTM


def create_model(hidden_size, look_back, dropout):
    model = Sequential()
    model.add(LSTM(hidden_size, input_shape=(1, look_back), dropout=dropout))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model


def train(model, train_x, train_y, batch_size, epochs):
    model.fit(train_x, train_y, epochs=epochs, batch_size=batch_size)
    return model


def test(model, test_x):
    y_pred = model.predict(test_x)
    return y_pred


def evaluate(y_true, y_pred):
    pass





