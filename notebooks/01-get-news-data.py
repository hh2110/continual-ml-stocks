# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

from HelperFunctions import (
    SaveLoadOfOldTweetsIntoCSV
)
from datetime import date


SaveLoadOfOldTweetsIntoCSV(
    'USATODAY', 
    date(2020,6,2), 
    date(2020,6,13),
    'test-tweets.csv'
)




# +

def CreateDatesList(fromDate, toDate):
    """
    Create a vector of dates spaced by a week between the two input dates
    """
    currentDate=fromDate
    datesList = []
    while currentDate <= toDate:
        datesList.append(currentDate)
        currentDate += timedelta(7)
    
    datesList.append(toDate)
        
    return datesList
        
datesList = CreateDatesList(date(2020,6,2), date(2020,7,3))
fromDateList = datesList[0:-1]
toDateList = datesList[1:]
for i,j in zip(fromDateList, toDateList):
    print(i,j)
# -















# ## old code



# +

# import sys
# import os
# import tweepy
# import pandas as p

# username = 'USATODAY'  # this is what we're searching for
# maxTweets = 10 # Some arbitrary large number
# tweetsPerQry = 2  # this is the max the API permits
# fName = username+'_tweets.csv' # We'll store the tweets in a text file.


# # If results from a specific ID onwards are reqd, set since_id to that ID.
# # else default to no lower limit, go as far back as API allows
# sinceId = None

# # If results only below a specific ID are, set max_id to that ID.
# # else default to no upper limit, start from the most recent tweet matching the search query.
# max_id = -1

# tweetCount = 0
# print("Downloading max {0} tweets".format(maxTweets))

# api = SetUpTwitterAPI()

# tweetsDF = pd.DataFrame(
#     columns=["id_str", "created_at", "full_text", "retweet_count"]
# )
# tweetsDF.to_csv('tweets.csv', mode='a')


# while tweetCount < maxTweets:
#     try:
#         if (max_id <= 0):
#             if (not sinceId):
#                 new_tweets = tweepy.Cursor(
#                     api.user_timeline, screen_name=username, 
#                     tweet_mode="extended"
#                 ).items(tweetsPerQry)
#             else:
#                 new_tweets = tweepy.Cursor(
#                     api.user_timeline, screen_name=username, 
#                     tweet_mode="extended", since_id=sinceId
#                 ).items(tweetsPerQry)
#         else:
#             if (not sinceId):
#                 new_tweets = tweepy.Cursor(
#                     api.user_timeline, screen_name=username, 
#                     tweet_mode="extended", max_id=str(max_id - 1)
#                 ).items(tweetsPerQry)
#             else:
#                 new_tweets = tweepy.Cursor(
#                     api.user_timeline, screen_name=username, 
#                     tweet_mode="extended", max_id=str(max_id - 1),
#                     since_id=sinceId
#                 ).items(tweetsPerQry)
#         if not new_tweets:
#             print("No more tweets found")
#             break
#         tweetsDF = pd.DataFrame(
#             columns=["id_str", "created_at", "full_text", "retweet_count"]
#         )
#         for tweet in new_tweets:
#             tweetsDF = tweetsDF.append(CreateTweetDict(tweet), ignore_index=True)
#         tweetsDF.to_csv('tweets.csv', mode='a', header=False)

#         tweetCount += new_tweets.num_tweets
#         print("Downloaded {0} tweets".format(tweetCount))
#         max_id = new_tweets.current_page.max_id
#     except tweepy.TweepError as e:
#         # Just exit if any error
#         print("some error : " + str(e))
#         break

# print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))

# -


