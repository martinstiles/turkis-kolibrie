import os
import json


PATH = os.path.dirname(__file__)
SCREEN_NAMES = [
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

def get_num_spaces(party):
    return len("Arbeiderpartiet") - len(party)

sum_tweets = 0
for party in SCREEN_NAMES:
    with open(PATH + "/data/tweets/" + party + ".json", "r") as file:
        tweets = json.load(file)
        num_tweets = len(tweets.keys())
        num_spaces = get_num_spaces(party)
        sum_tweets += num_tweets
        print(party + ": " + " " * num_spaces +  str(num_tweets))

print("\nTotal number of tweets:", sum_tweets)