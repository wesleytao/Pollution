


version 1:
table:
# user profile
* user id (key)
* user country
* user gender
* followers_count
* friends_count
* favourite_count
* status_count
* topic [str]
(sep by comma)


# user timeline(pending)
* user id 
* time 
* tweet id
* like count
* follower count

# event timeline
* tweet id
* time
* like 
* comment
* retweet_count(changing)
* favorite_count(changing)

# tweet 
* tweet id (key)  
* keyword/topic:
* tweet user id (key)
* tweet time
* tweet text
* retweeted


# retweet time 
* tweet id (key)
* retweet id (key)
* time (key)

