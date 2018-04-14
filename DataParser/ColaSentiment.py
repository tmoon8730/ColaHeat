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
import time
from pymongo import MongoClient
from random import randint

# Connection Data
client = MongoClient('mongodb://localhost:27017')
db = client.ColaHeat


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
        # return sentiment
        return analysis.sentiment.polarity

    def get_tweets(self, query, count):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # Call the api to get the tweets
            fetched_tweets = self.api.search(q = query, count = count, geocode="34.000471,-81.041786,150mi")

            # Parse each tweet
            for tweet in fetched_tweets:
                # If the tweet has a location
                if(tweet._json['place'] != None):
                    print(tweet._json['place']['bounding_box']['coordinates'][0][0])
                    parsed_tweet = {}
                    parsed_tweet['text'] = tweet.text
                    parsed_tweet['coordinates'] = tweet._json['place']['bounding_box']['coordinates'][0][0]
                    parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                    # Append to array
                    if tweet.retweet_count > 0:
                        if parsed_tweet not in tweets:
                            tweets.append(parsed_tweet)
                    else:
                        tweets.append(parsed_tweet)

            # Return the list of parsed tweets
            return tweets
        except tweepy.TweepError as e:
            print("Error : " + str(e))


def worker():
    '''
    Method that runs the twitter client and then updates
    the database
    '''
    # Instantiate a Twitter Client
    api = TwitterClient()

    # Get all the tweets that contain a space
    tweets = api.get_tweets(query = ' ', count = 100)

    # For each tweet add the sentiment and coordinates to the db
    for tweet in tweets:
        update(tweet['sentiment'],tweet['coordinates']);

def update(sentimentValue, coordinates):
    '''
    Method that adds a given sentimentValue and coordinates
    array to the database
    '''

    # Using only one documents so just pull off the first doc
    old = db.data.find_one({})

    # Append to the data array
    old['data'].append({'value': sentimentValue,'coordinates': coordinates,'date': time.ctime()})

    # Upsert operation
    db.data.replace_one({'_id': old.get('_id') }, old, True);


def main():
    '''
    Main method which calls the worker method every 10 seconds
    '''
    while(True):
        worker()
        print("\nFinished running at: %s\n" % time.ctime())
        time.sleep(10)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
