import os
import json
import matplotlib.pyplot as plt
from pathlib import Path

PATH = Path(os.path.dirname(__file__))
PATH_TO_TWEETS = PATH.parent / "data_retrieval" / "data" / "tweets"
PARTY_FILES = [
    "Arbeiderpartiet",
    "frp_no",
    "Hoyre",
    "KrFNorge",
    "Partiet",
    "Raudt",
    "Senterpartiet",
    "SVparti",
    "Venstre",
]
PARTY_FILE_TO_DISPLAY_NAME = {
    "Arbeiderpartiet": "AP",
    "frp_no": "FRP",
    "Hoyre": "Høyre",
    "KrFNorge": "KRF",
    "Partiet": "MDG",
    "Raudt": "Rødt",
    "Senterpartiet": "SP",
    "SVparti": "SV",
    "Venstre": "Venstre",
}


total_tweet_count = 0
total_retweet_count = 0
x_parties = []
y_retweet_percentage = []

for party_file in PARTY_FILES:
    with open(PATH_TO_TWEETS / (party_file + ".json"), "r") as file:
        tweets = json.load(file)
        num_tweets = len(tweets.keys())
        total_tweet_count += num_tweets

        num_retweets = 0
        for tweet_id, tweet_ob in tweets.items():
            try:
                if tweet_ob["referenced_tweets"][0]["type"] == "retweeted":
                    total_retweet_count += 1
                    num_retweets += 1
            except:
                pass

        x_parties.append(PARTY_FILE_TO_DISPLAY_NAME[party_file])  # Remove .json
        y_retweet_percentage.append(num_retweets / num_tweets)

print("Total retweet percentage:", total_retweet_count / total_tweet_count)

plt.style.use('ggplot')
plt.bar(x_parties, y_retweet_percentage, color='green')
plt.xlabel("Party")
plt.ylabel("Users")
plt.title("Number of users per party")

plt.show()
