import os
import tweepy
import pandas as pd
import GetOldTweets3 as got
from datetime import datetime, timedelta, date
import logging
import time

logging.basicConfig(
    filename="tweet-download.log",
    filemode="a",
    format="%(asctime)s - %(message)s",
    level=logging.INFO,
)


def CreateTweetDict(tweetInput, whichAPI):
    """
    Given a tweet object, take the relevant items and create custom dict
    """
    tweetDict = {}

    if whichAPI == "twitter":
        tweetDict["id_str"] = int(tweetInput.id_str)
        tweetDict["created_at"] = tweetInput.created_at
        tweetDict["full_text"] = tweetInput.full_text.replace("\n", " ")
        tweetDict["retweet_count"] = int(tweetInput.retweet_count)
    elif whichAPI == "got3":
        tweetDict["id"] = tweetInput.id
        tweetDict["permalink"] = tweetInput.permalink
        tweetDict["username"] = tweetInput.username
        tweetDict["to"] = tweetInput.to
        tweetDict["text"] = tweetInput.text
        tweetDict["date"] = tweetInput.date
        tweetDict["retweets"] = tweetInput.retweets
        tweetDict["favorites"] = tweetInput.favorites
        tweetDict["mentions"] = tweetInput.mentions
        tweetDict["hashtags"] = tweetInput.hashtags
        tweetDict["geo"] = tweetInput.geo

    return tweetDict


def GetOldTweetsIntoDF(username, fromDate, toDate=datetime.utcnow()):
    """
    Making use of library get-old-tweets-3 to download tweets into df
    """
    fromDateStr = fromDate.strftime("%Y-%m-%d")
    toDateStr = toDate.strftime("%Y-%m-%d")
    # Creation of query object
    tweetCriteria = (
        got.manager.TweetCriteria()
        .setUsername(username)
        .setSince(fromDateStr)
        .setUntil(toDateStr)
    )
    # Creation of list that contains all tweets
    tweetsObject = got.manager.TweetManager.getTweets(tweetCriteria)
    # Creating DF of chosen tweet data
    tweetsDF = CreateEmptyTweetDataframe("got3")
    for tweetItem in tweetsObject:
        try:
            tweetsDF = tweetsDF.append(
                CreateTweetDict(tweetItem, "got3"), ignore_index=True
            )
        except:
            continue

    return tweetsDF


def CreateEmptyTweetDataframe(whichAPI):
    """
    Creates an empty dataframe with correct headings
    """
    if whichAPI == "got3":
        columnsList = [
            "id",
            "permalink",
            "username",
            "to",
            "text",
            "date",
            "retweets",
            "favorites",
            "mentions",
            "hashtags",
            "geo",
        ]
    tweetsDF = pd.DataFrame(columns=columnsList)

    return tweetsDF


def SaveLoadOfOldTweetsIntoCSV(username, fromDate, toDate, fileName):
    """
    Saves tweets to csv file on a N weekly basis between two dates with 2 min sleep in between
    each saving action - to stop overloading the API
    """

    logging.info(
        "Creating CSV file of tweets between {} and {}.".format(fromDate, toDate)
    )

    tweetsDF = CreateEmptyTweetDataframe("got3")
    tweetsDF.to_csv(fileName)
    datesList = CreateDatesList(fromDate, toDate, 4)
    fromDateList = datesList[0:-1]
    toDateList = datesList[1:]

    numberOfTweets = 0
    for i, j in zip(fromDateList, toDateList):
        currentTweetsDF = GetOldTweetsIntoDF(username, i, j)
        numberOfTweets += len(currentTweetsDF)
        currentTweetsDF.to_csv(fileName, mode="a", header=False)
        logging.info(
            "Update CSV file. Total number of Tweets: {} from {} till {}".format(
                numberOfTweets, fromDate, j
            )
        )
        time.sleep(120)

    logging.info(
        "Completed the download of all {} tweets from {} into file: {} from {} till {}.".format(
            numberOfTweets, username, fileName, fromDate, toDate
        )
    )

    return None


def CreateDatesList(fromDate, toDate, weeksNumber):
    """
    Create a vector of dates spaced by N weeks between the two input dates
    """
    currentDate = fromDate
    datesList = []
    while currentDate <= toDate:
        datesList.append(currentDate)
        currentDate += timedelta(7 * weeksNumber)

    datesList.append(toDate)

    return datesList
