from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

translator = Translator(service_urls=['translate.googleapis.com'])
analyzer = SentimentIntensityAnalyzer()


def translate(string):
    return translator.translate(string).text


def analyze(string):
    return analyzer.polarity_scores(string)["compound"]