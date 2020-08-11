import pandas as pd
import time
import os
from sklearn.ensemble import RandomForestClassifier
from GetNewsData import (
    CreateEmptyTweetDataframe
)
from VectorizeTweetData import (
    GetQuickGroupedVectorizedDataByJoiningTweets
)
from MergePriceData import (
    get_price_df,
    get_news_df_and_columns,
    merge_news_price_df,
    TreatWeekendTweets,
    IntroduceLaggedPOC
)
from RunModel import (
    do_ml
)

def TimeTaken(t0):
    return time.time() - t0