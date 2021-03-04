import requests
import os
import json

PATH = os.path.dirname(__file__)

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
BEARER_TOKEN = os.environ.get("TWITTER_BEARER")
HEADERS = {"Authorization": "Bearer {}".format(BEARER_TOKEN)}
COUNT = 5000
BASE_URL = "https://api.twitter.com/1.1/followers/ids.json?count=" + str(COUNT) + "&screen_name="

def get_url(party_name):
    url = BASE_URL + party_name
    return url

def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def save_followers(party_name, json_response):
    ids = json_response["ids"]
    print("Size of ids:", len(ids))
    with open("%s/data/parties/%s.txt" % (PATH, party_name), "a") as file:
        for id in ids:
            file.write(str(id) + "\n")

def get_cursor(party_name):
    with open(PATH + "/data/parties/cursors.json") as file:
        cursors = json.load(file)
        return cursors[party_name]


def save_cursor(party_name, new_cursor):
    with open(PATH + "/data/parties/cursors.json") as file:
        cursors = json.load(file)

    cursors[party_name] = new_cursor

    with open(PATH + "/data/parties/cursors.json", "w") as file:
        json.dump(cursors, file, indent=4, sort_keys=True)


def main():
    iterations = 0
    for party_name in SCREEN_NAMES:
        next_cursor = get_cursor(party_name)
        if next_cursor == 0 or next_cursor == "0":
            continue
        
        url = get_url(party_name)
        if next_cursor:
            url += "&cursor=" + next_cursor

        json_response = connect_to_endpoint(url, HEADERS)
        next_cursor = json_response["next_cursor_str"]

        save_followers(party_name, json_response)

        print("#################################")
        print("Followers for %s saved successfully" % party_name, COUNT)
        print("")
        
        # Save next_cursor
        save_cursor(party_name, next_cursor)


if __name__ == "__main__":
    main()
