import os
from google.cloud import translate_v2 as translate
from multiprocessing import Pool
import pandas as pd
import time

t0 = time.time()

os.environ['GOOGLE_APPLICATION_CREDENTIALS']=os.path.expanduser("~/googletrans_api_key.json")

translate_client = translate.Client()


def translate(text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language='en', source_language='no')
    return result["translatedText"]


def f(row):
    date, author_id, tweet, i, l = row
    print(i,"/",l, time.time()-t0)
    translated_tweet = translate(tweet)
    return date, author_id, translated_tweet


def main(filename):
    df = pd.read_csv("clean/" + filename)
    arr = df.to_numpy()
    l = len(arr)
    with Pool(32) as p:
        translated_arr = p.map(f, [[*row, i, l] for i, row in enumerate(arr)])
    df = pd.DataFrame(translated_arr, columns=df.columns)
    df.to_csv("clean/translated/" + filename)


if __name__ == '__main__':

    main("Hoyre.csv")
