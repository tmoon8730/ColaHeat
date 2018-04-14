#############################################################
# File: ColaSentiment.py                                    #
# Author: Tyler Moon                                        #
# Date: 4/14/2018                                           #
# Purpose: This python file pulls in the recent Tweets      #
#          from the Columbia area, runs sentiment analysis, #
#          and outputs to a MongoDB database                #
#############################################################


# Library imports
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import os

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        # Keys and tokens from the Twitter Dev Console
        consumer_key = os.environ['CONSUMER_KEY']
        consumer_secret = os.environ['CONSUMER_SECRET']
        access_token = os.environ['ACCESS_TOKEN']
        access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

        # Authentication
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Twitter Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing all the links and
        special characters using simple regex statements
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+) | ([^0-9A-Za-z \t]) | (\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # Set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        else:
            return 'negative'

    def get_tweets(self, query, count = 10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # Call the api to get the tweets
            fetched_tweets = self.api.search(q = query, count = count, geocode="34.000471,-81.041786,50mi")

            # Parse each tweet
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # Return the list of parsed tweets
            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))



def main():
    api = TwitterClient()
    tweets = api.get_tweets(query = ' ', count = 200)

    # Parse out the positive and negative tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])


    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))



if __name__ == "__main__":
    main()
