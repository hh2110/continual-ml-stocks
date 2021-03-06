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

from HelperFunctions.VectorizeTweetData import (
    ProcessTweetDataFrame,
    VectorizeDataFrame,
    GroupByParallelProcess,
    GetQuickGroupedVectorizedDataByJoiningTweets
)

# +
fileNameUsa = "../data/raw-tweets/usatoday_2016-01-01_till_2020-01-01.csv"
fileNameWsj = "../data/raw-tweets/WSJmarkets_2016-01-01_till_2020-01-01.csv"
tweetsDF = pd.concat([
    pd.read_csv(fileNameUsa, index_col=0), 
    pd.read_csv(fileNameWsj, index_col=0)
])

processedDF = ProcessTweetDataFrame(tweetsDF, '{}.pkl'.format('all-tweets-processed.pkl'))
vectorizedDF = VectorizeDataFrame(processedDF, 1997, 'bow', stopdf)
dfList = GroupByParallelProcess(vectorizedDF, 8, 'sum')
finalDF = pd.concat(dfList, axis=1)
finalDF = finalDF.loc[:,~finalDF.columns.duplicated()]
finalDF.to_pickle('all_tweets_group_sum.pkl')

# other quicker method if just summing vectors (takes ~40s)
# finalDF = GetQuickGroupedVectorizedDataByJoiningTweets(tweetsDF, 'bow', 5000)
# finalDF.to_pickle('david-example.pkl')




















# ## Vectorize clean data
#
# - Now need to vectorize text data
# - Vectorize via BoW and TF-IDF
# - Need to union this matrix with id, date, fav, retw with DataMapper
# - Aggregate in 24 hour time periods:
#     - could sum in 24 hours
#     - could average too
#     - https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html
# - Save it - ready to be merged with Stock data
#
# - good tutorial for using sklearn's count-vectorizer: https://kavita-ganesan.com/how-to-use-countvectorizer/#.XvEVk2hKg2w
#
# - imporvements:
#     - could use lemmatisation to reduce number of features
#     - need to analyse top 5000 features - some are probably not useful
#     - could do some more investigation into these 5000 features - look at using pca to reduce them further?
#     - weight the aggregation mean by favorites or by retweets



