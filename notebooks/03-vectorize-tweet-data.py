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
    GroupByParallelProcess
)

# +
# fileName = "usatoday_2016-01-01_till_2020-01-01.csv"
# fileName = "../data/WSJmarkets_2016-01-01_till_2020-01-01.csv"
fileName = "../data/FT_2016-01-01_till_2020-01-01.csv"
tweetsDF = pd.read_csv(fileName, index_col=0)

processedDF = ProcessTweetDataFrame(tweetsDF, '{}.pkl'.format(fileName.split('.')[0]))
vectorizedDF = VectorizeDataFrame(processedDF, 37)
dfList = GroupByParallelProcess(vectorizedDF, 8)
finalDF = pd.concat(dfList, axis=1)
finalDF = finalDF.loc[:,~finalDF.columns.duplicated()]
finalDF.to_pickle(fileName + 'test_weighted_avg.pkl')
# -





















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



