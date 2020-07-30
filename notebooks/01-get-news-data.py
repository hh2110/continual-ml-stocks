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

fromDate = date(2015, 1, 1)
toDate = date(2020, 1, 1)
# investopedia recommended handles
usernameList = [
    "CNBC",
    "Benzinga",
    "Stocktwits",
    "BreakoutStocks",
    "bespokeinvest",
    "WSJmarkets",
    "nytimesbusiness",
    "IBDinvestors",
    "WSJdeals",
]
for username in usernameList:
    SaveLoadOfOldTweetsIntoCSV(
        username,
        fromDate,
        toDate,
        "../data/raw-tweets/investopedia-handles/jan-15-till-jan-20/{}_{}_till_{}.csv".format(
            username, fromDate, toDate
        ),
    )
