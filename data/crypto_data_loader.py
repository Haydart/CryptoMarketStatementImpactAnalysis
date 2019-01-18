import csv
import pandas as pd

FILE_PATH = "crypto dataset/BTC-USD_2015-2018_1min/gemini_BTCUSD_2018_1min.csv"


def load_data():
    with open(FILE_PATH, newline='') as data_file:
        reader = csv.reader(data_file, delimiter=',')

        headers = next(reader)
        print(headers)

        coin_data = pd.DataFrame(columns=headers)
        coin_data.set_index('Unix Timestamp', inplace=True)
        print(coin_data)

        for row in reader:
            coin_data.loc[row[0]] = row[1:]
