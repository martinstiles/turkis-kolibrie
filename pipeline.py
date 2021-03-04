import os
import pandas as pd
from sentiment import translate_and_analyze
from topic import TopicClassifier
import pickle


def add_sentiment(df):
    df["vader"] = df["text"].apply(translate_and_analyze)
    return df


def add_topic(df):
    # Finne ordboken som matcher best
    # Returnere key til ordboken som matcher best
    df["topic"] = df["text"].apply(topicclassifier.classify_topic)
    return df

# read all texts from the nrk valgomat
path = "data/test/"
files = os.listdir(path)
topicclassifier = TopicClassifier()
final_df = pd.DataFrame()
for file in files:
    df = pd.read_csv(os.path.join(path,file), delimiter=";")
    df = add_sentiment(df)
    df = add_topic(df)
    df["parti"] = file.split(".")[0] # add the target value
    final_df = pd.concat([final_df, df], ignore_index=True)

topics = final_df["topic"].unique()
ids = final_df["user"].unique()

features = pd.DataFrame(columns = ["user"] + list(topics))
features["user"] = ids
for topic in topics:
    features[topic] = 0

d_temp = final_df[["user", "parti"]]
d_temp = d_temp.drop_duplicates(subset='user', keep="first")
# inner join on userids to add the labels to the feature df
features = features.merge(d_temp, how='left', on='user')
features = features.set_index("user")
final_df = final_df.set_index("user")

for i, row in final_df.iterrows(): # loops through all the indices and rows
    features.loc[i, row["topic"]] += row["vader"] # updates the topic feature for user i with the vader value in this row

print(features.head(10))
if not os.path.exists('data/features/'):
    os.makedirs('data/features/')
with open('data/features/features.pickle', 'wb') as file:
    pickle.dump(features, file)
