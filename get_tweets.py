import requests
import os
import json

PATH = os.path.dirname(__file__)
BEARER_TOKEN = os.environ.get("TWITTER_BEARER")
HEADERS = {"Authorization": "Bearer {}".format(BEARER_TOKEN)}
COUNT = 11
BASE_URL = "https://api.twitter.com/2/tweets/search/recent?user.fields=id&max_results=" + str(COUNT)
BASE_QUERY = "&query=lang%3Ano%20%28"

# "https://api.twitter.com/2/tweets/search/recent?user.fields=id&max_results=11&query=lang%3Ano%20from%3A16432083"

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

# TODO handle next_token
def main():
    for filename in os.listdir(PATH + "/data/parties"):
        """  """
        user_ids = []
        with open(PATH + "/data/parties/" + filename, "r") as file:
            for line in file:
                user_id = line.strip()
                user_ids.append(user_id)

        responses = []
        query = BASE_QUERY + "from%3A" + str(user_ids[0])
        for user in user_ids[1:]:
            new_user = "%20OR%20from%3A" + str(user)
            if len(query) + len(new_user) > 480:
                print(query)
                # TODO: Retrieve user id???
                url = query_url(query + "%29")
                response_json = connect_to_endpoint(url, HEADERS)
                responses.append(response_json)
                query = BASE_QUERY + "from%3A" + str(user)
            else:
                query += new_user
        url = query_url(query + "%29")
        response_json = connect_to_endpoint(url, HEADERS)
        responses.append(response_json)
        query = BASE_QUERY + "from%3A" + str(user)
        print(responses)
        
        # TODO: Tweets contains \n so it must be removed!
        for response in responses:
            # TODO: Some responses DONT HAVE "data"! --> try/catch?
            data = response["data"]
            for ob in data:
                text = ob["text"]
                with open(PATH + "/data/tweets/" + filename, "a") as file:
                    file.write(text + "\n")

        print("#################################")
        print("Followers for %s saved successfully" % filename[:-4], COUNT)
        print("")


if __name__ == "__main__":
    main()
