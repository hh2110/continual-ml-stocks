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

from HelperFunctions.GetNewsData import (
    SaveLoadOfOldTweetsIntoCSV
)
from datetime import date

fromDate = date(2016,4,16)
toDate = date(2020,7,1)
username = 'WSJ'
SaveLoadOfOldTweetsIntoCSV(
    username, 
    fromDate, 
    toDate,
    '{}_{}_till_{}.csv'.format(username, fromDate, toDate)
)


