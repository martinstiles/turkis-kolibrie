import requests
import os
import json
import datetime



PATH = os.path.dirname(__file__)
TODAY = datetime.date.today()
WEEK_NR = datetime.date(TODAY.year, TODAY.month, TODAY.day).isocalendar()[1]
BEARER_TOKEN = os.environ.get("TWITTER_BEARER")
HEADERS = {"Authorization": "Bearer {}".format(BEARER_TOKEN)}
COUNT = 11
BASE_URL = "https://api.twitter.com/2/tweets/search/recent?user.fields=id&max_results=" + str(COUNT)
BASE_QUERY = "&query=lang%3Ano%20%28"


def query_url(query):
    return BASE_URL + query


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_response(query, next_token):
    # TODO: retrieve user_id too?
    url = query_url(query + "%29")
    if next_token:
        url += "next_token=" + next_token
    response_json = connect_to_endpoint(url, HEADERS)
    return response_json


def main():
    for filename in os.listdir(PATH + "/data/parties"):
        """
        Read user_ids from data/parties
        """
        user_ids = []
        with open(PATH + "/data/parties/" + filename, "r") as file:
            for line in file:
                user_id = line.strip()
                user_ids.append(user_id)

        """
        Send requests to retrieve tweets from every user in user_ids[].
        Requests may not be longer than 512 characters.
        """
        responses = []
        next_token = ""
        query = BASE_QUERY + "from%3A" + str(user_ids[0])
        for user in user_ids[1:]:
            new_user = "%20OR%20from%3A" + str(user)
            if len(query) + len(new_user) > 480:
                response_json = get_response(query, next_token)
                responses.append(response_json)
                query = BASE_QUERY + "from%3A" + str(user)
            else:
                query += new_user
        # Remaining batch:
        response_json = get_response(query, next_token)
        responses.append(response_json)
        print("Number of responses:", len(responses))

        """
        For every response: save tweets in one line in correct text file
        """
        for response in responses:
            try:
                data = response["data"]
                for ob in data:
                    text = ob["text"]
                    stripped_text = text.replace("\n", "")
                    with open(PATH + "/data/tweets/" + filename, "a") as file:
                        file.write(stripped_text + "\n")
            except Exception:
                # Response has no data field
                pass

        print("#######################################")
        print("Followers for %s saved successfully" % filename[:-4], COUNT)
        print("")
        break


if __name__ == "__main__":
    main()
