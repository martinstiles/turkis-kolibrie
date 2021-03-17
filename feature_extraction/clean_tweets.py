import os
import pandas as pd
import re

def clean_rt(text):
    text = str(text)
    text = re.sub(' \w+…', '', text)
    text = re.sub('https\S+', '', text)
    text = re.sub(r"([\w/'+$\s-]+|[^\w/'+$\s-]+)\s*", r"\1 ", text)
    text = re.sub('^rt ', '', text)
    return text

# import the csv file into a Pandas dataframe
tweet_df = pd.read_json("/Users/akjen/Documents/NTNU/EiT/turkis-kolibrie/data_retrieval/data/tweets/Venstre.json")
tweet_df = tweet_df.T
tweet_df = tweet_df[["author_id", "text"]]

tweet_df["text"] = tweet_df["text"].str.lower()
tweet_df["text"] = tweet_df["text"].str.replace("@", "")
tweet_df['text'] = tweet_df['text'].apply(clean_rt)


tweet_df.to_csv("/Users/akjen/Documents/NTNU/EiT/turkis-kolibrie/feature_extraction/clean/Venstre.csv")
