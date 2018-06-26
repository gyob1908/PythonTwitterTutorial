rg#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 13:45:27 2018

@author: oliverbeatson
"""

# Import the required libraries.

import tweepy
import pandas as pd
import numpy as np
import AccessKeys

# Use tweepy.OAuthHandler to create an authentication using the given. 
# Insert your keys into the corresponding area.

auth = tweepy.OAuthHandler(AccessKeys.ConsumerKey, AccessKeys.ConsumerSecret)
auth.set_access_token(AccessKeys.AccessToken, AccessKeys.AccessTokenSecret)

# Connect to the Twitter API using the authentication.
api = tweepy.API(auth)

# Perform a basic search query.

result = api.search(q='Buhari') #%23 is used to specify '#' to search for a hashtag

results = []

#Get the first 500 items based on the search query
#It is possible to increase this but Twitter will time out as if there are too many requests
for tweet in tweepy.Cursor(api.search, q='Buhari').items(500):
    results.append(tweet)


# Create a function to convert a given list of tweets into a Pandas DataFrame.
# The DataFrame will consist of only the values, which might be useful for analysis.


def toDataFrame(tweets):

    Tweets = pd.DataFrame()

    Tweets['tweetID'] = [tweet.id for tweet in tweets]
    Tweets['Text'] = [tweet.text for tweet in tweets]
    Tweets['RetweetCt'] = [tweet.retweet_count for tweet in tweets]
    Tweets['FavoriteCt'] = [tweet.favorite_count for tweet in tweets]
    Tweets['Source'] = [tweet.source for tweet in tweets]
    Tweets['Created'] = [tweet.created_at for tweet in tweets]
    Tweets['userID'] = [tweet.user.id for tweet in tweets]
    Tweets['ScreenName'] = [tweet.user.screen_name for tweet in tweets]
    Tweets['userName'] = [tweet.user.name for tweet in tweets]
    Tweets['userCreateDt'] = [tweet.user.created_at for tweet in tweets]
    Tweets['userDesc'] = [tweet.user.description for tweet in tweets]
    Tweets['FollowerCt'] = [tweet.user.followers_count for tweet in tweets]
    Tweets['FriendsCt'] = [tweet.user.friends_count for tweet in tweets]
    Tweets['Location'] = [tweet.user.location for tweet in tweets]
    Tweets['Timezone'] = [tweet.user.time_zone for tweet in tweets]

    return Tweets

#Pass the tweets list to the above function to create a DataFrame
    
Tweets = toDataFrame(results)
Tweets.to_csv('Tweets.csv')

# Identify information for the most retweeted tweet

Retweeted = Tweets.sort_values(['RetweetCt'], ascending=False)
Retweeted.head(1)

# Identify information for the most retweeted tweet

Favourited = Tweets.sort_values(['FavoriteCt'], ascending=False)
Favourited.head(1)

# Histogram of the Follower count variable
Tweets['FollowerCt'].plot.hist(bins=100);

# Gives mean value for a specified variable
np.mean(Tweets['FollowerCt'])

# Creates a list of the tweet source of each tweet by grouping each response.
TweetsSource = Tweets.groupby('Source').size()
# Creates a bar plot of the count produced in the above function
TweetsSource.plot.bar();
