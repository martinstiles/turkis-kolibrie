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
BASE_URL = "https://api.twitter.com/2/tweets/search/recent?max_results=" + str(COUNT) + "&tweet.fields=author_id,public_metrics,referenced_tweets"
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

def get_responses(filename, user_ids):
    """
    Send requests to retrieve tweets from every user in user_ids[].
    Requests may not be longer than 512 characters.
    """
    current_party = filename[:-4]  # Remove ".txt"
    print("Retrieving for tweets for:", current_party)

    responses = []
    query = BASE_QUERY + "from%3A" + str(user_ids[0])
    counter = 1
    for user_id in user_ids[1:]:
        new_user = "%20OR%20from%3A" + str(user_id)
        if len(query) + len(new_user) > 480:
            next_token = ""
            while next_token is not None:
                response_json = get_response(query, next_token)
                responses.append(response_json)
                try:
                    # Save next_token if it exists in response
                    next_token = response_json["meta"]["next_token"]
                except Exception:
                    # Reset next_token if it does not exist
                    next_token = None
            query = BASE_QUERY + "from%3A" + str(user_id)
        else:
            query += new_user
        # PRINT PROGRESS
        print("%s / %s" % (counter, len(user_ids)))
        counter += 1
    # Remaining batch:
    response_json = get_response(query, next_token)
    responses.append(response_json)

    return responses

def save_tweets(filename, responses):
    """
    For every response: save tweets as one line in correct text file
    """
    current_party = filename[:-4]  # Remove ".txt"

    # Load json file into a dictionary
    with open(PATH + "/data/tweets/" + current_party + ".json", "r") as file:
        tweets = json.load(file)

    # Add new tweets to the dictionary
    new_tweets_dict = {}
    for response in responses:
        try:
            new_tweets_list = response["data"]
            for tweet_obj in new_tweets_list:
                tweet_id = tweet_obj["id"]
                del tweet_obj["id"]
                new_tweets_dict[tweet_id] = tweet_obj # tweet object without id
        except KeyError as e:
            pass
    tweets.update(new_tweets_dict)

    # Write the dictionary back to json file
    # TODO: add week nr to directory (rememer to update load etc.)
    with open(PATH + "/data/tweets/" + current_party + ".json", "w") as file:
        json.dump(tweets, file, indent=4, sort_keys=True)
    
    print("#########################################")
    print("Followers for %s saved successfully" % current_party)

def update_counts(filename, user_ids):
    """
    Update the number of users read for every party
    """
    party_to_count_map = {}
    current_count = len(user_ids)
    current_party = filename[:-4]  # Remove ".txt"

    # Read previous count for every party
    with open("%s/data/tweets/counts.txt" % PATH, "r") as file:
        for line in file:
            if line == "":
                continue
            stripped_line = line.strip()
            party_name, count = stripped_line.split(',')
            party_to_count_map[party_name] = int(count)
    
    # Update current party count
    if current_party in party_to_count_map:
        party_to_count_map[current_party] += current_count
    else:
        party_to_count_map[current_party] = current_count
    
    print("New count of %s: %s" % (current_party, party_to_count_map[current_party]))

    # Save number of user_ids read for each party file:
    with open("%s/data/tweets/counts.txt" % PATH, "w") as file:
        for party, count in party_to_count_map.items():
            file.write(party + "," + str(count) + "\n")

def check_duplicates(temp):
    # TODO: Make a method to check if the user id has already been added
    # SHOULD probably have a dictionary: userId -> tweetIds[]
    pass

parties_to_skip = [
    # "Arbeiderpartiet",
    # "Hoyre",
    # "SVparti",
    # "Venstre",
    # "Partiet",
    # "Raudt",
    # "frp_no",
    # "KrFNorge",
    # "Senterpartiet"
]

def main():
    for filename in os.listdir(PATH + "/data/parties"):
        if filename[:-4] in parties_to_skip or filename == "cursors.json":
            print("OHHHHH NO!!!", filename)
            continue

        user_ids = get_user_ids(filename)
        # Reduce set to save tweets in batches:
        # previous run: [:15000]
        user_ids = user_ids[16400:17100]

        responses = get_responses(filename, user_ids)

        save_tweets(filename, responses)

        update_counts(filename, user_ids)

        print("")


if __name__ == "__main__":
    main()

"""
* text
* id
* public_metrics
    * retweet_count
    * reply_count
    * like_count
    * quote_count
* author_id
"""