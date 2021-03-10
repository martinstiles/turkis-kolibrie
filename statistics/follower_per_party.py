import os
import matplotlib.pyplot as plt
from pathlib import Path

PATH = Path(os.path.dirname(__file__))
PATH_TO_USERS = PATH.parent / "data_retrieval" / "data" / "parties"
PATH_TO_TWEETS = PATH.parent / "data_retrieval" / "data" / "tweets"

print(PATH_TO_TWEETS)



plt.style.use('ggplot')

x = ["AP", "SV"]
energy = [59000, 20000]

x_pos = [i for i, _ in enumerate(x)]

plt.bar(x, energy, color='green')
plt.xlabel("Party")
plt.ylabel("#Users")
plt.title("Number of user per party")

plt.xticks(x_pos, x)

plt.show()
