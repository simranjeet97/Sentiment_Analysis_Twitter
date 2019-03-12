import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient(object):
    def __init__(self):
        consumer_key = ''
        consumer_secret = ''
        access_token = ''
        access_token_secret = ''

        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)

            self.auth.set_access_token(access_token, access_token_secret)

            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        tweets = []

        try:
            fetched_tweets = self.api.search(q=query, count=count)

            for tweet in fetched_tweets:

                parsed_tweet = {}

                parsed_tweet['text'] = tweet.text

                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


def main():
    api = TwitterClient()

    topic = 'Dogs'
    count = 200

    tweets = api.get_tweets(query=topic, count=count)

    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    positive = 100 * len(ptweets) / len(tweets)

    print("Positive tweets percentage: {} %".format(positive))

    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    negative = 100 * len(ntweets) / len(tweets)

    print("Negative tweets percentage: {} %".format(negative))

    f = [x for x in tweets if x not in ntweets]
    f2 = [x for x in f if x not in ptweets]

    neutral = 100 * len(f2) / len(tweets)
    print("Neutral tweets percentage: {} %".format(neutral))


"""    
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])

"""
if __name__ == "__main__":
    main()
