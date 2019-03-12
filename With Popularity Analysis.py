from To_DataFrame import *
from textblob import TextBlob

# Convert Series To DataFrame

# import pandas as pd
# df = pd.DataFrame({'Tweets':text.values})
# print(type(df))

import tweepy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

tweets = api.user_timeline(screen_name="realDonaldTrump", count=200)
print("Number of Extracted Tweets : {}.\n".format(len(tweets)))

"""for tweet in tweets[:5]:
    print(tweet.text)
    print()"""

data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
# print(data.head(10))
# print(dir(tweets[0]))

# We add relevant data:
data['len'] = np.array([len(tweet.text) for tweet in tweets])
data['ID'] = np.array([tweet.id for tweet in tweets])
data['Date'] = np.array([tweet.created_at for tweet in tweets])
data['Source'] = np.array([tweet.source for tweet in tweets])
data['Likes'] = np.array([tweet.favorite_count for tweet in tweets])
data['RTs'] = np.array([tweet.retweet_count for tweet in tweets])

# print(data.head(1))

mean = np.mean(data['len'])
#print("The Length Average in Tweets is {}.".format(mean))

fav = np.max(data['Likes'])
retweets = np.max(data['RTs'])

fav_one = data[data.Likes == fav].index[0]
more_rt = data[data.RTs == retweets].index[0]
"""
print("Tweet with more Likes is \n {}".format(data['Tweets'][fav_one]))
print("No of Likes is {}".format(fav))
print("{} Characters \n".format(data['len'][fav_one]))

print("Tweet with more Retweets is \n {}".format(data['Tweets'][more_rt]))
print("No of Retweets is {}".format(retweets))
print("{} Characters \n".format(data['len'][more_rt]))
"""
tlen = pd.Series(data=data['len'].values, index=data['Date'])
tfav = pd.Series(data=data['Likes'].values, index=data['Date'])
tret = pd.Series(data=data['RTs'].values, index=data['Date'])

# tlen.plot(figsize=(16,4),label="Length",legend=True);

# tfav.plot(figsize=(16,4), label="Likes", legend=True)
# tret.plot(figsize=(16,4), label="Retweets", legend=True);
# plt.show()

from textblob import TextBlob
import re


def clean_tweet(tweet):
    '''
    Utility function to clean the text in a tweet by removing
    links and special characters using regex.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def analize_sentiment(tweet):
    '''
    Utility function to classify the polarity of a tweet
    using textblob.
    '''
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1

data['SA'] = np.array([analize_sentiment(tweet) for tweet in data['Tweets']])

pos_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] > 0]
neu_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] == 0]
neg_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] < 0]

p = len(pos_tweets)*100/len(data['Tweets'])
n = len(neg_tweets)*100/len(data['Tweets'])
nu = len(neu_tweets)*100/len(data['Tweets'])

print("Percentage of positive tweets: {}%".format(p))
print("Percentage of neutral tweets: {}%".format(nu))
print("Percentage de negative tweets: {}%".format(n))

colors = ['green', 'red', 'grey']
sizes = [p,n,nu]
labels = 'Positive', 'Negative', 'Neutral'

## use matplotlib to plot the chart
plt.pie(
   x=sizes,
   shadow=True,
   colors=colors,
   labels=labels,
   startangle=90
)

plt.title("Sentiment Analysis.")
plt.show()
