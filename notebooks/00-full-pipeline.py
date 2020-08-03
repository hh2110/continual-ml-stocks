# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.5.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
import pandas as pd
import numpy as np
import time
import os
from sklearn.ensemble import RandomForestClassifier

def TimeTaken(t0):
    return time.time() - t0

from HelperFunctions.GetNewsData import (
    CreateEmptyTweetDataframe
)

from HelperFunctions.VectorizeTweetData import (
    GetQuickGroupedVectorizedDataByJoiningTweets
)

from HelperFunctions.MergePriceData import (
    get_price_df,
    get_news_df_and_columns,
    merge_news_price_df,
    TreatWeekendTweets,
    IntroduceLaggedPOC
)

from HelperFunctions.RunModel import (
    do_ml
)

# +
t0_create_raw_tweets_df = time.time()
filePath = "../data/raw-tweets/investopedia-handles/jan-15-till-jan-20/"
tweetsDF = CreateEmptyTweetDataframe('got3')
for fileName in os.listdir(filePath):
    tweetsDF = tweetsDF.append(pd.read_csv(filePath+fileName, index_col=0))
print("create raw tweets df \t", TimeTaken(t0_create_raw_tweets_df))


t0_vectorize_tweets = time.time()
vectorizeMethod = 'tfidf'
vectorizedTweets = GetQuickGroupedVectorizedDataByJoiningTweets(
    tweetsDF, vectorizeMethod, 500
)
print("vectorize tweets df \t", TimeTaken(t0_vectorize_tweets))


t0_get_price_date = time.time()
tickers = 'AAPL'
start_date = '2015-01-01'
end_date = '2020-01-01'
threshold = 0.005
close_shift_step = 1
priceDF, priceColumns = get_price_df(
    tickers, start_date, end_date, threshold, close_shift_step
)
print("get price data df \t", TimeTaken(t0_get_price_date))


t0_treat_weekends = time.time()
newsDF = vectorizedTweets.sparse.to_dense()
newsColumns = [k for k in vectorizedTweets.columns.tolist() if k!='label_date']
mergedDF = merge_news_price_df(newsDF, priceDF)
if vectorizeMethod == 'bow':
    weekendTreatedMergedDF = TreatWeekendTweets(mergedDF, newsColumns)
elif vectorizeMethod == 'tfidf':
    weekendTreatedMergedDF = mergedDF.copy().dropna()
modelReadyDF = IntroduceLaggedPOC(weekendTreatedMergedDF, 1)
print("fix tweets weekends \t", TimeTaken(t0_treat_weekends))


t0_run_model = time.time()
result_confusion_matrix, result_accuracy_score = do_ml(
    modelReadyDF, 0.4, RandomForestClassifier, n_estimators=500, 
    bootstrap = True, max_features = 'sqrt'
)
print(result_confusion_matrix)
print("Running classifier \t", TimeTaken(t0_run_model))

print(' ')
print('total time taken \t', TimeTaken(t0_create_raw_tweets_df))
# -

weekendTreatedMergedDF




