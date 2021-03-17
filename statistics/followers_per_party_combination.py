import os
# import matplotlib.pyplot as plt
from pathlib import Path

PATH = Path(os.path.dirname(__file__))
PATH_TO_USERS = PATH.parent / "data_retrieval" / "data" / "parties"
PATH_TO_TWEETS = PATH.parent / "data_retrieval" / "data" / "tweets"

SCREEN_NAMES = [
    "Arbeiderpartiet",
    "Hoyre",
    "SVparti",
    "Venstre",
    "Partiet",
    "Raudt",
    "frp_no",
    "KrFNorge",
    "Senterpartiet"
]

followers = {}
for party in SCREEN_NAMES:
    with open(PATH_TO_USERS / (party + ".txt")) as users_file:
        users_list = users_file.readlines()
        users_list = [user.strip() for user in users_list]
        users_list.sort()
        followers[party] = users_list

counts = {}
progress = 0
for party1 in followers:
    for user in followers[party1]:
        passed_party = False
        failed = False
        parties_string = ""
        for party2 in followers:
            progress += 1
            if not progress % 1000:
                print(progress)
            if party2 == party1:
                passed_party = True
            if user in followers[party2]:
                if passed_party:
                    parties_string += party2
                else:
                    failed = True
                    break
        if not failed:
            if parties_string in counts:
                counts[parties_string] += 1
            else:
                counts[parties_string] = 1


print(counts)
