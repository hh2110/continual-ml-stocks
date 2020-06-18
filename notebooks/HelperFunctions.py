import configparser
import os
import tweepy
import pandas as pd

config = configparser.ConfigParser()
config.read("code.conf")


def SetUpEnvironmentVariables():
    """
    sets up environment with information regarding openblender - can also set up other
    information to access data from other providers
    return: none
    """
    parameterList = [
        "OPEN_BLENDER_API_TOKEN",
        "TWITTER_API_KEY",
        "TWITTER_SECRET_KEY",
        "TWITTER_ACCESS_TOKEN",
        "TWITTER_ACCESS_TOKEN_SECRET",
    ]

    if os.environ["COMPUTERNAME"] == "UK-L-0318":
        for parameter in parameterList:
            os.environ[parameter] = config["DATA"][parameter]


def GetTweetsDataFrame(username, lastNTweets):
    """
    gets last N tweets of a particular user - returns DF containing the tweets
    return: dataframe of tweets
    """
    auth = tweepy.AppAuthHandler(
        os.environ["TWITTER_API_KEY"], os.environ["TWITTER_SECRET_KEY"]
    )
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # get tweets
    tweetsDF = pd.DataFrame(
        columns=["id_str", "created_at", "full_text", "retweet_count"]
    )
    for tweet in tweepy.Cursor(
        api.user_timeline, screen_name=username, tweet_mode="extended"
    ).items(lastNTweets):
        try:
            tweetsDF = tweetsDF.append(CreateTweetDict(tweet), ignore_index=True)
        except:
            continue

    return tweetsDF


def CreateTweetDict(tweetInput):
    """
    Given a tweet object, take the relevant items and create custom dict
    """
    tweetDict = {}
    tweetDict["id_str"] = int(tweetInput.id_str)
    tweetDict["created_at"] = tweetInput.created_at
    tweetDict["full_text"] = tweetInput.full_text
    tweetDict["retweet_count"] = int(tweetInput.retweet_count)

    return tweetDict


def DownloadManyTweets(username, numberOfTweets):
    """
    Method to get LOADS of tweets
    This will include a timer to not go over the twitter API limit
    This will also keep track of tweet IDs so tweets are not duplicated
    This will save results as a pkl file.
    https://bhaskarvk.github.io/2015/01/how-to-use-twitters-search-rest-api-most-effectively./#:~:text=To%20start%20with%20the%20API,window%20for%20per%2Duser%20authentication.
    """

    return None
