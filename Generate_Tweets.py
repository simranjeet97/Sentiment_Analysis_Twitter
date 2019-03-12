import time

import pandas as pd
import tweepy
import jsonpickle

# Consume:
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

# Access:
ACCESS_TOKEN = ''
ACCESS_SECRET = ''


def connect_to_twitter_OAuth():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    api = tweepy.API(auth)
    return api


# Create API object
api = connect_to_twitter_OAuth()


# print(api)

def get_save_tweets(filepath, api, query, max_tweets=1000, lang='en'):
    tweetCount = 0

    # Open file and save tweets
    with open(filepath, 'w') as f:
        # Send the query
        for tweet in tweepy.Cursor(api.search, q=query, lang=lang).items(max_tweets):
            # Convert to JSON format
            f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
            tweetCount += 1

        # Display how many tweets we have collected
        print("Downloaded {0} tweets".format(tweetCount))

query = '#Dogs'

# Get those tweets
get_save_tweets('tweets.json', api, query)
