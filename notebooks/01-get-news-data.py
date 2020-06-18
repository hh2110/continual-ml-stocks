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

# +
import OpenBlender, os
import pandas as pd
import json
import tweepy

from HelperFunctions import (
    SetUpEnvironmentVariables,
    GetTweetsDataFrame
)
# -

SetUpEnvironmentVariables()
tester = GetTweetsDataFrame('USATODAY',100)

tester = tester.sort_values('id_str')
print(tester.iloc[0])
print(tester.iloc[-1])

# +
# 1000 tweets - 5/6 till 18/6 = 2 weeks
# 52 weeks = 1 year tweets = 26,000 tweets
# 5 years tweets = 130,000 tweets
