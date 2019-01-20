from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
import pandas as pd
from datetime import timedelta
from utils import get_data_from_to


def get_avg_sentiments(sentences):
    if len(sentences) == 0:
        return 0
    return np.mean(analyze_sentiments(sentences))


def analyze_sentiments(sentences):
    analyzer = SentimentIntensityAnalyzer()
    sentiments = []
    [sentiments.append(analyzer.polarity_scores(s)['compound']) for s in sentences]
    return sentiments


def analyze_sentiment(sentence):
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(sentence)['compound']


def avg_sentiments_from_text_in_time(df, texts_column, date_times_column, window_size):
    dataset = pd.DataFrame(columns=["sentiment_avg", "datetime"])
    start_date_time = df[date_times_column].iloc[0].replace(minute=0,second=0)
    end_date_time = df[date_times_column].iloc[-1].replace(minute=0,second=0)
    time_window = timedelta(hours=2)

    start = start_date_time
    i = 0

    while i < len(df) and start_date_time <= end_date_time:
        texts = []
        end = start + time_window

        while i < len(df) and df[date_times_column].iloc[i].replace(minute=0, second=0) < end:
            texts.append(df[texts_column].iloc[i])
            i+=1

        start = start + time_window
        if len(texts) == 0:
            continue

        avg_sentiment = get_avg_sentiments(texts)
        dataset.loc[len(dataset)] = [avg_sentiment, start]
    return dataset


def get_avg_sentiments_in_time(df, text_column, date_column, start_date, end_date):
    df2 = get_data_from_to(df, date_column, start_date, end_date)
    if not df2.empty:
        return get_avg_sentiments(df2[text_column])
    else:
        return 0
