
# coding: utf-8

# In[10]:


import pymongo
import json
import pandas as pd
import time
import re
import numpy as np
from gmplot import gmplot
import pickle as pickle


# # information extraction

# In[11]:


def get_coordinate(this_tweet):
    '''input  dict  tweet
       output list [LONGITUDE LATITUDE]'''
    # There are geo-tagged 3 place store geoinformation
    # User self-report place
    # geo  1 Latitude 2 Longitude
    # coordinates 1 LONGITUDE,2 Latitude
    # coordinate box same as coordinates
    coordinates = None
    try:
        coordinates=this_tweet['coordinates']['coordinates']
#         print('coordinates {}'.format(this_tweet['coordinates']['coordinates']))
    except Exception as e:
        pass

    try:
        # take average over coordinates box
        coordinates=list(np.array(this_tweet['place']['bounding_box']['coordinates'][0]).mean(axis=0))
    except Exception as e:
        pass

    coordinates = [None,None] if not coordinates else coordinates
    return coordinates

def get_retweetid(tweet):
    try:
        return(tweet["retweeted_status"]["id"])
    except:
        return None

def get_retweet_username(tweet):
    try:
        return(tweet["retweeted_status"]["user"]["name"])
    except:
        return None
def get_retweet_followers_count(tweet):
    try:
        return(tweet["retweeted_status"]["user"]["followers_count"])
    except:
        return None
def get_retweet_fa(tweet):
    try:
        return(tweet["retweeted_status"]["favorite_count"])
    except:
        return None
def get_retweet_retw(tweet):
    try:
        return(tweet["retweeted_status"]["retweet_count"])
    except:
        return None
def get_retweet_rep(tweet):
    try:
        return(tweet["retweeted_status"]["reply_count"])
    except:
        return None
def get_full_text(tweet):
    try:
        return(tweet["extended_tweet"]["full_text"])
    except:
        return(tweet["text"])

def jsontopandas(tweets_data):
    tweets=pd.DataFrame()
    tweets['id'] = list(map(lambda tweet: tweet['_id'], tweets_data))
    tweets['longitude']=list(map(lambda tweet:get_coordinate(tweet)[0], tweets_data))
    tweets['latitude']=list(map(lambda tweet: get_coordinate(tweet)[1], tweets_data))
    tweets['place_country']=list(map(lambda tweet: tweet['place']['country'] if tweet['place']!= None else None, tweets_data))
    tweets['place_full_name']=list(map(lambda tweet: tweet['place']['full_name'] if tweet['place']!= None else None, tweets_data))
    tweets['text']=list(map(lambda tweet: get_full_text(tweet), tweets_data))
    tweets["user_id"]=list(map(lambda tweet:tweet["user"]["id"],tweets_data))
    tweets["user_name"]=list(map(lambda tweet:tweet["user"]["name"],tweets_data))
    tweets["user_followers"]=list(map(lambda tweet:tweet["user"]["followers_count"],tweets_data))
    tweets['user_loc']=list(map(lambda tweet: tweet['user']['location'], tweets_data))
    tweets['lang']=list(map(lambda tweet: tweet['lang'], tweets_data))
    tweets['created_at']=list(map(lambda tweet: time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')), tweets_data))
#     tweets['retweet_id']=list(map(lambda tweet: get_retweetid(tweet),tweets_data))
#     tweets['retweet_user']=list(map(lambda tweet: get_retweet_username(tweet),tweets_data))
    return tweets


# In[12]:


if __name__ == '__main__':
    client=pymongo.MongoClient()
    client.list_database_names()

    sample    =client.pollution.tweetcollection
    population=client.twitterdb.twitter_search

    db=population
    # pattern =regx
    start=time.time()
    print("going to find tweets with language equal to fr information")
    withplace=list(db.find({"lang":'fr'}))
    print("total {} tweets found".format(len(withplace)))
    print("time elaspe ",time.time()-start,' second')

    path="../output/frjson.p"
    with open(path, 'bw') as f:
        pickle.dump(withplace, f)

    tweet_table=jsontopandas(withplace)
    tweet_table.to_csv("../output/fr.csv",encoding='utf-8',index=False)
    print ("tweets saved")
