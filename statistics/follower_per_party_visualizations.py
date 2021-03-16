import os
import json
from pathlib import Path


PATH = Path(os.path.dirname(__file__))
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


with open(PATH / "followers_per_party_combination.json") as file:
    distributions = json.load(file)


def parties_string_to_list(parties_string):
    party_list = []
    for party in SCREEN_NAMES:
        if party in parties_string:
            party_list.append(party)
    return party_list


distributions = [(parties_string_to_list(comb), distributions[comb]) for comb in distributions]


def find_occurrences(included=[], excluded=[]):
    tot = 0
    for distribution in distributions:
        for party in included:
            if party not in distribution[0]:
                break
        else:
            for party in excluded:
                if party in distribution[0]:
                    break
            else:
                tot += distribution[1]
    return tot


L = len(SCREEN_NAMES)
total_users = find_occurrences()
print("Total users:  {}".format(total_users))
print()
print("Percentage of users following...")
for party in SCREEN_NAMES:
    print("{:{width1}}:{:{width2}.1%}".format(party, find_occurrences([party])/total_users, width1=17, width2=6))
print()
print("Percentage of users following...")
for party1 in SCREEN_NAMES:
    print("{} also following...".format(party1))
    followers_party1 = find_occurrences([party1])
    for party2 in SCREEN_NAMES:
        if party1 != party2:
            print("{:{width1}}:{:{width2}.1%}".format(party2, find_occurrences([party1, party2])/followers_party1, width1=17, width2=6))
    print()
