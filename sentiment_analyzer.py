from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
import pandas as pd
from datetime import timedelta
from CryptoStatementImpactAnalysis.model.utils import get_data_from_to


def get_avg_sentiments(sentences):
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
    dataset = pd.DataFrame(columns=["sentiment_avg", "date_time"])
    time_delta = timedelta(days=window_size)
    start_date_time = df[date_times_column][0].date()
    end_date_time = df[date_times_column][-1].date()

    while start_date_time <= end_date_time:
        avg_sentiment = get_avg_sentiments_in_time(df, texts_column, date_times_column, start_date_time, start_date_time + time_delta)
        dataset.loc[len(dataset)] = [avg_sentiment, start_date_time]
        start_date_time += time_delta

    return dataset


def get_avg_sentiments_in_time(df, text_column, date_column, start_date, end_date):
    df2 = get_data_from_to(df, date_column, start_date, end_date)
    if not df2.empty:
        return get_avg_sentiments(df2[text_column])
    else:
        return 0
