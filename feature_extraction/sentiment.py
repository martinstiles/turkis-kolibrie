from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

translator = Translator(service_urls=['translate.googleapis.com'])
analyzer = SentimentIntensityAnalyzer()

def translate_and_analyze(string):
    translated = translator.translate(string).text
    vs = analyzer.polarity_scores(translated)
    return vs["compound"]
