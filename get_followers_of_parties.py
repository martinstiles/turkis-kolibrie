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
    # TODO: Use next_cursor
    ids = json_response["ids"]
    print("Size of ids:", len(ids))
    with open("%s/data/parties/%s.txt" % (PATH, party_name), "a") as file:
        for id in ids:
            file.write(str(id) + "\n")

def main():
    # TODO: Retrieve next cursor from /data/parties/cursors.txt before running
    iterations = 0
    for party_name in SCREEN_NAMES:
        # TODO: Assert next cursor if it exists in cursors.txt
        next_cursor = ""
        while True:
            url = get_url(party_name)
            if next_cursor:
                url += "&cursor=" + next_cursor
                # print(url)
            json_response = connect_to_endpoint(url, HEADERS)
            # print(json_response)
            next_cursor = json_response["next_cursor_str"]
            save_followers(party_name, json_response)

            print("#################################")
            print("Followers for %s saved successfully" % party_name, COUNT)
            print("")

            iterations += 1
            if iterations >= 1:  # 1 iteration
                break
        
        # Save next_cursor
        with open("%s/data/parties/cursors.txt" % PATH, "a") as file:
            file.write(party_name + "," + next_cursor + "\n")


if __name__ == "__main__":
    main()
