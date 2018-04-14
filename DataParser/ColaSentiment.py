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


def output():
    api = TwitterClient()
    tweets = api.get_tweets(query = ' ', count = 200)

    # Parse out the positive and negative tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

    print("\n\nPositive tweets:")
    for tweet in ptweets[:2]:
        print(tweet['text'])
    print("\n\nNegative tweets:")
    for tweet in ntweets[:2]:
        print(tweet['text'])

    posPercent = 100*len(ptweets)/len(tweets)
    negPercent = 100*len(ntweets)/len(tweets)


    print("Positive tweets percentage: {} %".format(posPercent))
    print("Negative tweets percentage: {} %".format(negPercent))

    update(posPercent,negPercent);

def update(positiveValue, negativeValue):
    old = db.data.find_one({})
    old['positive'].append({'percent': positiveValue,'date': time.ctime()})
    old['negative'].append({'percent': negativeValue,'date': time.ctime()})
    result = db.data.replace_one({'_id': old.get('_id') }, old, True);

def main():
    while(True):
        output()
        print(time.ctime())
        time.sleep(10)

    # names = ['Kitchen','Animal','State', 'Tastey', 'Big','City','Fish', 'Pizza','Goat', 'Salty','Sandwich','Lazy', 'Fun']
    # company_type = ['LLC','Inc','Company','Corporation']
    # company_cuisine = ['Pizza', 'Bar Food', 'Fast Food', 'Italian', 'Mexican', 'American', 'Sushi Bar', 'Vegetarian']
    # for x in xrange(1, 501):
    #     business = {
    #         'name' : names[randint(0, (len(names)-1))] + ' ' + names[randint(0, (len(names)-1))]  + ' ' + company_type[randint(0, (len(company_type)-1))],
    #         'rating' : randint(1, 5),
    #         'cuisine' : company_cuisine[randint(0, (len(company_cuisine)-1))]
    #     }
    # result = db.reviews.insert_one(business)
    # print('Created {0} of 100 as {1}'.format(x,result.inserted_id))


    # outputData = {
    #     'positive': [
    #         {
    #             'percent': '24',
    #             'date': time.ctime()
    #         },
    #         {
    #             'percent': '30',
    #             'date': time.ctime()
    #         }
    #     ],
    #     'negative': [
    #         {
    #             'percent': '24',
    #             'date': time.ctime()
    #         },
    #         {
    #             'percent': '30',
    #             'date': time.ctime()
    #         }
    #     ],
    # }
    #
    # db.data.insert_one(outputData);

    # posUpdate = outputData['positive']#.extend({'percent':'55','date': time.ctime()})
    # a = []
    # print(result.inserted_id)
    # old = db.data.find_one({})
    # b = {'percent':'65','date': time.ctime()}
    # old['positive'].append(b)
    # # print(outputData)
    # result = db.data.replace_one({'_id': old.get('_id') }, old, True);
if __name__ == "__main__":
    main()
