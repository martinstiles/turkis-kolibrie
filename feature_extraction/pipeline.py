import os
import pandas as pd
from sentiment import analyze
from topic import TopicClassifier
import pickle
import numpy as np
import time
from tqdm import tqdm


def get_sentiment(df):
    return df["text"].apply(analyze)


def add_topic(df):
    # Finne ordboken som matcher best
    # Returnere key til ordboken som matcher best
    df["topic"] = df["text"].apply(topic_classifier.classify_topic)
    return df

# create map from user to parties
path = "../data_retrieval/data/parties/"
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
print(len(map_user_party.keys()))
exit()
# transform to binary representation
for key, value in map_user_party.items():
    map_user_party[key] = [0]*count
    for index in value:
        map_user_party[key][index] = 1


path = "../feature_extraction/clean/original/"
files = os.listdir(path)
path_translated = "../feature_extraction/clean/translated/"
files_translated = os.listdir(path_translated)

topic_classifier = TopicClassifier()
final_df = pd.DataFrame()


for file, file_translated in zip(files, files_translated):
    print(file)
    df = pd.read_csv(os.path.join(path, file), delimiter=",")
    df_translated = pd.read_csv(os.path.join(path_translated, file_translated), delimiter=",", index_col="Unnamed: 0")
    df = add_topic(df)
    df["vader"] = get_sentiment(df_translated)
    final_df = pd.concat([final_df, df], ignore_index=True)
final_df = final_df.drop_duplicates(subset=final_df.columns, keep="first")
final_df.to_csv('final_df.csv', index=True)
topics = final_df["topic"].unique()
ids = final_df["author_id"].unique()

features = pd.DataFrame(columns=["author_id"] + list(topics))
features["author_id"] = ids
for topic in topics:
    features[topic] = 0

features = features.set_index("author_id")
final_df = final_df.set_index("author_id")

for i, row in final_df.iterrows():  # loops through all the indices and rows
    features.loc[i, row["topic"]] += row["vader"]  # updates the topic feature for user i with the vader value in this row

targets = pd.Series(data=map_user_party)
print(targets)
features["target"] = targets


if not os.path.exists('feature_extraction/data/features/'):
    os.makedirs('feature_extraction/data/features/')

print(features)
features.to_csv('feature_extraction/data/features/features.csv', index=True)
