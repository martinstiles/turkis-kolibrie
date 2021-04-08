import os
import json
from pathlib import Path
import matplotlib.pyplot as plt


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


def find_occurrences(included=[], excluded=[], min_follows=0, max_follows=9):
    tot = 0
    for distribution in distributions:
        if not(min_follows <= len(distribution[0]) <= max_follows):
            continue
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
for party1 in SCREEN_NAMES:
    followers_party1 = find_occurrences([party1])
    data = {}
    partier = []
    for party2 in SCREEN_NAMES:
        if party1 != party2:
            partier.append(party2)
            data[party2] = find_occurrences([party1, party2])/followers_party1
    plt.style.use('ggplot')
    plt.bar(data.keys(), [data[key] for key in partier], color='green')
    plt.xlabel("Party")
    plt.ylabel("Users")
    plt.title(party1)
    #plt.show()

data = {}
for party in SCREEN_NAMES:
    data[party]  = find_occurrences([party], max_follows=1)
plt.style.use('ggplot')
plt.bar(data.keys(), [data[key] for key in SCREEN_NAMES], color='green')
plt.xlabel("Party")
plt.ylabel("Users")
plt.title("Brukere som kun følger ett parti")
#plt.show()

print(sum([data[key] for key in SCREEN_NAMES]))