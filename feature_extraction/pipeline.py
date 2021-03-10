import os
import pandas as pd
from sentiment import translate_and_analyze
from topic import TopicClassifier
import pickle
import numpy as np
import time


def add_sentiment(df):
    df["vader"] = df["text"].apply(translate_and_analyze)
    return df


def add_topic(df):
    # Finne ordboken som matcher best
    # Returnere key til ordboken som matcher best
    df["topic"] = df["text"].apply(topicclassifier.classify_topic)
    return df

# create map from user to parties
path = "data/testusers/"
files = os.listdir(path)
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

# read all texts from the nrk valgomat
path = "data/testtweets/"
files = os.listdir(path)
topicclassifier = TopicClassifier()
final_df = pd.DataFrame()
for file in files:
    df = pd.read_csv(os.path.join(path,file), delimiter=";")
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
features["target"] = targets

print(features.head(10))

if not os.path.exists('data/features/'):
    os.makedirs('data/features/')
with open('data/features/features.pickle', 'wb') as file:
    pickle.dump(features, file)
