"""
\u00e5 = å
\u00f8 = ø
erna: 16432083
"""


import requests
import os
import json

path = os.path.dirname(__file__)

screen_names = [
    # "erna_solberg",
    # "jonasgahrstore",
    # "Siv_Jensen_FrP",
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

def auth():
    return os.environ.get("TWITTER_BEARER")


def create_url():
    # url = "https://api.twitter.com/2/users/by?usernames=erna_solberg&expansions=pinned_tweet_id"
    url = "https://api.twitter.com/2/tweets/search/recent?user.fields=id&max_results=11&query=lang%3Ano%20from%3A16432083"
    return url

def user_url(screen_names):
    url = "https://api.twitter.com/2/tweets/search/recent"
    return url + '?screen_name=' + screen_names

def get_followers():
    url = "https://api.twitter.com/1.1/followers/ids.json?screen_name=Arbeiderpartiet"
    return url

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def save_followers(party_name, json_response):
    data = json_response["data"]
    print("Size of data:", len(data))
    with open("%s/collection/%s.txt" % (path, party_name), "a") as file:
        id = str()
        [file.write(data_ob["id"] + "\n") for data_ob in json_response["data"]]

def main():
    bearer_token = auth()
    url = create_url()
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    print(json.dumps(json_response, indent=4, sort_keys=True))
    # save_followers("ap", {"data": [{"id": "123"}, {"id": "321"}]})


if __name__ == "__main__":
    main()
