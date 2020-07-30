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
#     display_name: Python 3s
#     language: python
#     name: python3
# ---

from HelperFunctions.GetNewsData import SaveLoadOfOldTweetsIntoCSV
from datetime import date

fromDate = date(2019, 12, 1)
toDate = date(2020, 1, 1)
# investopedia recommended handles
usernameList = [
    "CNBC",
    "Benzinga",
    "Stocktwits",
    "BreakoutStocks",
    "bespokeinvest",
    "WSJmarkets",
    "Stephanie_Link",
    "nytimesbusiness",
    "IBDinvestors",
    "WSJDealJournal",
]
for username in usernameList:
    SaveLoadOfOldTweetsIntoCSV(
        username,
        fromDate,
        toDate,
        "../data/raw-tweets/investopedia-handles/{}_{}_till_{}.csv".format(
            username, fromDate, toDate
        ),
    )
