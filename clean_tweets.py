import os
import pandas as pd


# import the csv file into a Pandas dataframe
tweet_df = pd.read_json("")
print(tweet_df)

tweet_df["tweet"] = tweet_df["tweet"].str.lower()
tweet_df["tweet"] = tweet_df["tweet"].str.replace("@", "")



pd.tweet_df.to_csv("clean_tweets.csv")
