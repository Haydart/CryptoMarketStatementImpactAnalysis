from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def analyze_sentiments(sentences):
    analyzer = SentimentIntensityAnalyzer()
    sentiments = []
    [sentiments.append(analyzer.polarity_scores(s)) for s in sentences]
    return sentiments
