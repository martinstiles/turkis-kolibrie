import requests
import os
import json
import datetime



PATH = os.path.dirname(__file__)
TODAY = datetime.date.today()
WEEK_NR = datetime.date(TODAY.year, TODAY.month, TODAY.day).isocalendar()[1]
BEARER_TOKEN = os.environ.get("TWITTER_BEARER")
HEADERS = {"Authorization": "Bearer {}".format(BEARER_TOKEN)}
COUNT = 100
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

def get_user_ids(filename):
    """
    Read user_ids from data/parties
    """
    user_ids = []
    with open(PATH + "/data/parties/" + filename, "r") as file:
        for line in file:
            user_id = line.strip()
            user_ids.append(user_id)
    return user_ids

def get_responses(user_ids):
    """
    Send requests to retrieve tweets from every user in user_ids[].
    Requests may not be longer than 512 characters.
    """
    responses = []
    next_token = ""
    query = BASE_QUERY + "from%3A" + str(user_ids[0])
    c = 1
    for user_id in user_ids[1:]:
        new_user = "%20OR%20from%3A" + str(user_id)
        if len(query) + len(new_user) > 480:
            response_json = get_response(query, next_token)
            responses.append(response_json)
            query = BASE_QUERY + "from%3A" + str(user_id)
            try:
                # Save next_token if it exists in response
                next_token = response_json["meta"]["next_token"]
            except Exception:
                # Reset next_token if it does not exist
                next_token = ""
        else:
            query += new_user
        # PRINT PROGRESS
        print("%s / %s" % (c, len(user_ids)))
        c += 1
    # Remaining batch:
    response_json = get_response(query, next_token)
    responses.append(response_json)

    # DEBUG
    print("Number of responses:", len(responses))
    # print(responses)
    print("Number of user_ids:", len(user_ids))

    return responses

def save_tweets(filename, responses):
    """
    For every response: save tweets as one line in correct text file
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

def update_counts(current_party, user_ids):
    """
    Update the number of users read for every party
    """
    party_to_count_map = {}
    current_count = len(user_ids)

    # Read previous count for every party
    with open("%s/data/tweets/counts.txt" % PATH, "r") as file:
        for line in file:
            if line == "":
                continue
            stripped_line = line.strip()
            party_name, count = stripped_line.split(',')
            party_to_count_map[party_name] = int(count)
    
    print("Count of %s before: %s" % (current_party, party_to_count_map[current_party]))
    
    # Update current party count
    if current_party in party_to_count_map:
        party_to_count_map[current_party] += current_count
    else:
        party_to_count_map[current_party] = current_count
    
    print("Count of %s after: %s" % (current_party, party_to_count_map[current_party]))

    # Save number of user_ids read for each party file:
    with open("%s/data/tweets/counts.txt" % PATH, "w") as file:
        for party, count in party_to_count_map.items():
            file.write(party + "," + str(count) + "\n")

def main():
    for filename in os.listdir(PATH + "/data/parties"):
        current_party = filename[:-4]  # Remove ".txt"

        user_ids = get_user_ids(filename)
        # NB! Arbeiderpartiet is DONE!
        # Reduce set to save tweets in batches:
        user_ids = user_ids[:1000]
        # user_ids = user_ids[1000:2000]
        # user_ids = user_ids[2000:3000]
        # user_ids = user_ids[3000:4000]
        # user_ids = user_ids[4000:]

        responses = get_responses(user_ids)

        save_tweets(filename, responses)

        update_counts(current_party, user_ids)

        print("#########################################")
        print("Followers for %s saved successfully" % current_party)
        print("")
        break


if __name__ == "__main__":
    main()
