from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def analyze_sentiments(sentences):
    analyzer = SentimentIntensityAnalyzer()
    sentiments = []
    [sentiments.append(analyzer.polarity_scores(s)['compound']) for s in sentences]
    return sentiments


def analyze_sentiment(sentence):
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(sentence)['compound']
