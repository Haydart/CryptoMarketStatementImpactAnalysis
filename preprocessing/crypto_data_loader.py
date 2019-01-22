import csv

import pandas as pd

FILE_PATH = "crypto dataset/BTC-USD_2015-2018_1min/gemini_BTCUSD_2018_1min.csv"


def load_data():
    with open(FILE_PATH) as data_file:
        reader = csv.reader(data_file, delimiter=',')
        headers = next(reader)

        crypto_data = pd.DataFrame(columns=headers)
        crypto_data.set_index(headers[0])

        for row in reader:
            crypto_data.loc[row[0]] = row[1:]
    return crypto_data
