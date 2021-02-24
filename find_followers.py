import requests
import os

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
COUNT = 10
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
    # TODO: Use next_cursor
    ids = json_response["ids"]
    print("Size of ids:", len(ids))
    with open("%s/data/parties/%s.txt" % (PATH, party_name), "a") as file:
        for id in ids:
            file.write(str(id) + "\n")

def main():
    for party_name in SCREEN_NAMES:
        url = get_url(party_name)
        json_response = connect_to_endpoint(url, HEADERS)
        save_followers(party_name, json_response)
        print("#################################")
        print("Followers for %s saved successfully" % party_name, COUNT)
        print("")

if __name__ == "__main__":
    main()

