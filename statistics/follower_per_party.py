import os
import json
import matplotlib.pyplot as plt
from pathlib import Path

PATH = Path(os.path.dirname(__file__))
PATH_TO_USERS = PATH.parent / "data_retrieval" / "data" / "parties"
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

x_parties = []
y_num_users = []

for party_file in PARTY_FILES:
    with open(PATH_TO_USERS / (party_file + ".txt"), "r") as file:
        users = file.readlines()
        num_users = len(users)

        x_parties.append(PARTY_FILE_TO_DISPLAY_NAME[party_file])  # Remove .json
        y_num_users.append(num_users)



plt.style.use('ggplot')
plt.bar(x_parties, y_num_users, color='green')
plt.xlabel("Party")
plt.ylabel("Users")
plt.title("Number of users per party")

#plt.xticks(x_pos, x)

plt.show()
