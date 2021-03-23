import os
import pandas as pd
from sentiment import translate_and_analyze
from topic import TopicClassifier
import pickle
import numpy as np
import time
from tqdm import tqdm

def add_sentiment(df):
    for i in tqdm(range(df.shape[0])):
        index = df.index[i]
        vader = translate_and_analyze(df.at[index, "text"])
        df.at[index,'vader'] = vader
    return df


def add_topic(df):
    # Finne ordboken som matcher best
    # Returnere key til ordboken som matcher best
    df["topic"] = df["text"].apply(topicclassifier.classify_topic)
    return df

# create map from user to parties
path = "data_retrieval/data/parties/"
files = os.listdir(path)
files.remove("cursors.json")
map_user_party = {}
count = 0
for i, file in enumerate(files):
    count += 1
    f = open(path + file, "r")
    for line in f.readlines():
        user_id = int(line.replace('\n', ''))
        if user_id not in map_user_party.keys():
            map_user_party[user_id] = [i]
        else:
            map_user_party[user_id] += [i]

# transform to binary representation
for key, value in map_user_party.items():
    map_user_party[key] = [0]*count
    for index in value:
        map_user_party[key][index] = 1


path = "feature_extraction/clean/"
files = os.listdir(path)
topicclassifier = TopicClassifier()
final_df = pd.DataFrame()
for file in files:
    print(files)
    df = pd.read_csv(os.path.join(path,file), delimiter=",")
    df = add_sentiment(df)
    df = add_topic(df)
    final_df = pd.concat([final_df, df], ignore_index=True)
final_df = final_df.drop_duplicates(subset=final_df.columns, keep="first")

topics = final_df["topic"].unique()
ids = final_df["user"].unique()

features = pd.DataFrame(columns = ["user"] + list(topics))
features["user"] = ids
for topic in topics:
    features[topic] = 0

features = features.set_index("user")
final_df = final_df.set_index("user")

for i, row in final_df.iterrows(): # loops through all the indices and rows
    features.loc[i, row["topic"]] += row["vader"] # updates the topic feature for user i with the vader value in this row

targets = pd.Series(data=map_user_party)
print(targets)
features["target"] = targets


if not os.path.exists('feature_extraction/data/features/'):
    os.makedirs('feature_extraction/data/features/')

print(features)
features.to_csv('feature_extraction/data/features/features.csv', index=True)
