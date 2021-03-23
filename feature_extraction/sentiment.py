from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


def analyze(string):
    return analyzer.polarity_scores(string)["compound"]