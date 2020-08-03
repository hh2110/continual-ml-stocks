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
import numpy as np
import pandas as pd
from datetime import datetime, date
import math

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

tickers = 'AAPL'
start_date = '2015-11-01'
end_date = '2020-01-01'
threshold = 0.005
close_shift_step = 1

priceDF, priceColumns = get_price_df(
    tickers, start_date, end_date, threshold, close_shift_step
)
newsDF, newsColumns = get_news_df_and_columns('david-example.pkl')
newsDF = newsDF.sparse.to_dense()
newsColumns = [k for k in newsColumns if k!='label_date']
mergedDF = merge_news_price_df(newsDF, priceDF)
weekendTreatedMergedDF = TreatWeekendTweets(mergedDF, newsColumns)
modelReadyDF = IntroduceLaggedPOC(weekendTreatedMergedDF, 1)
modelReadyDF.to_pickle('model-ready.pkl')
# -

from tqdm import tqdm


