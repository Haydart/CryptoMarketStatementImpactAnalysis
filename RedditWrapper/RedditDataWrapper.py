import pandas as pd
import numpy as np

def prepare_data():

    reddit_data = pd.read_csv("reddit_data", sep='\t')

    subreddits = reddit_data['subreddit'].unique()
    # ^^^ ['crypto' 'Bitcoin' 'litecoin' 'btc' 'CryptoCurrency' 'CryptoMarkets' 'ethereum']
    # removing subreddits realted to other coins than BTC

    subreddits = np.delete(subreddits, [2, 6])
    print("Removed unnecessary subreddits, remaining: ", subreddits)



    pass

prepare_data()




