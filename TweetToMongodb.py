from __future__ import print_function
import json
from typing import List
import os
import tweepy
from pymongo import MongoClient

# keywordlist

user = ["@BeijingAir"]
original = ['@NBA','NBA',"#NBA","air #pollution", "空气污染", "#airpollution", "वायु प्रदुषण", "la pollution de l'air", "la #pollution",
            "air #pollution", "l'air #pollution", "वायु प्रदुषण",'air quality,','smog','changement climatique','#changementclimatique','embouteillage',"#वायु प्रदुषण","वायु #प्रदूषण"]
category_1 = ["forest fire", "forest fires"]
category_2 = ["water poisoning", "water contamination"]
category_3: List[str] = ["flood flash", 'flood water', "flood warning"]
category_4 = ["earthquake"]
category_5 = ["oil spill", "pipeline spill", "tarsands spill", "tankers spill", "fossilfuel spill", "petroleum spill"]
category_6 = ["acid rain", "toxic rain", "mildew home", "mildew infested", "mildew basement", "mildew removal",
              "mildew growth", "mildew inspection", "mold flood", "mildew flood"]
category_7 = ["adelgid", "aphid", "beetle", "earwig", "insect", "locust", "louse", "moth", "psyllid", "termites",
              "termite bites", "bug bites", "bugs bites"]
category_8: List[str] = """allergy
allergins
pollen
dander
allergy + cough
allergies + cough
pollen + cough
dander + cough
dust + cough
allergy + sneeze
allergies + sneeze
pollen + sneeze
dander + sneeze
dust + sneeze
allergy + asthma
allergies + asthma
pollen + asthma
dander + asthma
dust + asthma
allergy + respiratory
allergies + respiratory
pollen + respiratory
dander + respiratory
dust + respiratory
allergy + lung
allergies + lung
pollen + lung
dander + lung
dust + lung""".split("\n")
category_8 = [word.replace("+", "") for word in category_8]
category_8 = [word.replace("  ", " ") for word in category_8]
category_9 = ["dust"]
category_10 = ["bed bugs"]
# MONGO_HOST= 'mongodb://localhost/twitterdb'  # assuming you have mongoDB installed locally
# and a database called 'twitterdb'
keywordlist = user + original + category_1 + category_2 + category_3 + category_4 + category_5 + category_6 + category_7 + category_8 + category_9 + category_10
WORDS = keywordlist


class StreamListener(tweepy.StreamListener):
    # This is a class provided by tweepy to access the Twitter Streaming API.
    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")

    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occurred: ' + repr(status_code))
        return False

    def on_data(self, data):
        # This is the meat of the script...it connects to your mongoDB and stores the tweet
        try:
            #                 client = MongoClient(MONGO_HOST)

            # Decode the JSON from Twitter
            datajson = json.loads(data)

            # use tweet id as mongodb id
            datajson["_id"] = datajson.pop("id")

            # grab the 'created_at' data from the Tweet to use for display
            # created_at = datajson['created_at']

            # print out a message to the screen that we have collected a tweet
            # print("Tweet collected at " + str(created_at))

            # insert the data into the mongoDB into a collection called twitter_search
            # if twitter_search doesn't exist, it will be created.
            db.twitter_search.insert_one(datajson)
        except Exception as e:
            print(e)

            with open(filename, 'w+') as f:
                f.write(data)


def main():
    # wesley
    ckey = 'NdQdQm2OALKTJgtCr9mz8SEAK'
    csecret = '2GVLXTHcIy3htHqD5NEIX1IGVuTNjiHMHNEXT2OTTlvjP50hKw'
    atoken = '980527124133109766-R2NKGIqJjrUvkOALRw7bdzAHRa4FV18'
    asecret = 'r5Px3c5gLtXVuNjJI53qoImV1PW6CeXwRyv8gnjqwTzt0'

    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)

    # Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
    listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
    streamer = tweepy.Stream(auth=auth, listener=listener)
    print("Tracking: " + str(WORDS))
    streamer.filter(track=WORDS, follow='5527964')


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # print(dir_path)
    filename = dir_path + '/data/duplicate.json'
    print(filename)
    client = MongoClient()
    db = client.twitterdb

    main()
