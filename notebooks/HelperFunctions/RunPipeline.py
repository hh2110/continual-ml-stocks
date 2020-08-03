import pandas as pd
import time
import os
from sklearn.ensemble import RandomForestClassifier
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

def TimeTaken(t0):
    return time.time() - t0