import pandas as pd
from datetime import date, datetime
import re
import logging
import spacy
from sklearn.feature_extraction import text
import scipy as sp
import scipy.sparse
import numpy as np
import multiprocessing as mp
from pathos.multiprocessing import ProcessingPool as Pool

nlp = spacy.load("en_core_web_sm")
tokenizer = nlp.Defaults.create_tokenizer(nlp)

logging.basicConfig(
    filename="vectorize-tweets.log",
    filemode="a",
    format="%(asctime)s - %(message)s",
    level=logging.INFO,
)

# split dataframe into splitNumber parts:
def GetListOfSplitDFs(df, splitNumber):
    """
    splits df into list of splitNumber df's - make sure len(df)%splitNumber=0 
    """
    columnList = df.columns.tolist()
    totalColumnNumber = len(columnList)
    columnsPerDF = totalColumnNumber / splitNumber

    dfList = []
    if totalColumnNumber % splitNumber == 0:
        for i in range(0, splitNumber):
            startColumnIndex = int(i * columnsPerDF)
            endColumnIndex = int(startColumnIndex + columnsPerDF)
            splitDF = df[columnList[startColumnIndex:endColumnIndex]]
            if splitDF.shape[1] == columnsPerDF:
                # add in label_retweets and label_favourites columns
                splitDF["label_retweets"] = df.copy().label_retweets
                splitDF["label_favorites"] = df.copy().label_favorites
                dfList.append(splitDF)
            else:
                logging.error("probably duplicate column names")
                return None
        return dfList
    else:
        logging.error("make sure len(columns) is divisible by splitNumber")
        return None


# apply groupby and then average over result and return averaged df
def PerformGroupbyAndAggregate(inputDF):
    return inputDF.groupby("label_date").apply(ApplyWAtoDF)


def PerformSum(inputDF):
    return inputDF.groupby("label_date").sum()


def PerformMean(inputDF):
    return inputDF.groupby("label_date").mean()


def ApplyWAtoDF(i_df):
    """
    Average the ngram values weighted by number of retweets
    Will return NaN if there are no retweets on a specific day - that is fine
    """
    weightedAverageDF = (
        i_df.drop(columns=["label_retweets", "label_favorites"])
        .mul(i_df["label_retweets"], axis=0)
        .sum(axis=0)
        / i_df.sum(axis=0).label_retweets
    )
    weightedAverageDF["label_retweets"] = np.mean(i_df["label_retweets"])
    weightedAverageDF["label_favorites"] = np.mean(i_df["label_favorites"])
    return weightedAverageDF


def GroupByParallelProcess(tweetsDF, cores, groupMethod):
    """
    Group by and aggregate on time via a parallel process
    """

    tweetsDF.label_date = tweetsDF.label_date.astype(int)
    tweetsDF = tweetsDF.set_index("label_date")
    # Parallelizing using Pool.apply()
    df_split = GetListOfSplitDFs(tweetsDF, cores)
    # create the multiprocessing pool
    pool = Pool(cores)
    # process the DataFrame by mapping function to each df across the pool
    logging.info('Starting the grouping and aggregating process.')
    if groupMethod == "weighted-average":
        df_out = pool.map(PerformGroupbyAndAggregate, df_split)
    elif groupMethod == "sum":
        df_out = pool.map(PerformSum, df_split)
    elif groupMethod == "mean":
        df_out = pool.map(PerformMean, df_split)
    else:
        logging.error("Choose correct group by method.")
        return None

    # close down the pool and join
    pool.close()
    pool.join()
    pool.clear()

    logging.info('Ended the grouping and aggregating process.')

    return df_out


def VectorizeDataFrame(
    tweetsDF,
    maxFeatures,
    vectorType="bow",
    extraStopWords=[],
    extraColumnLabels=["id", "retweets", "favorites", "date"],
):
    """
    Take a data set, vectorize 'text' column and return DF with all feature columns
    NB: all columns must be numbers!
    """
    if vectorType == "bow":
        vectorizer = text.CountVectorizer(
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.5,
            stop_words=text.ENGLISH_STOP_WORDS.union(extraStopWords),
            max_features=maxFeatures,
            preprocessor=ProcessText,
            tokenizer=SpacyTokenizerLemmatizer,
        )
    elif vectorType == "tfidf":
        vectorizer = text.TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.5,
            stop_words=text.ENGLISH_STOP_WORDS.union(extraStopWords),
            max_features=maxFeatures,
            preprocessor=ProcessText,
            tokenizer=SpacyTokenizerLemmatizer,
        )
    else:
        logging.error("choose type of vectorisation: bow OR tfidf")
        return None

    # horizontally stack vectorised text data with extra columns in DF
    X = sp.sparse.hstack(
        (
            vectorizer.fit_transform(tweetsDF.text),
            tweetsDF[extraColumnLabels].astype(float),
        ),
        format="csr",
    )
    X_columns = vectorizer.get_feature_names() + [
        "label_" + i for i in extraColumnLabels
    ]

    # convert sparse matrix to dataframe
    df = pd.DataFrame.sparse.from_spmatrix(X)
    df.columns = X_columns

    return df


def ProcessTweetDataFrame(tweetsDF, pklFileName):
    """
    Set of processing steps for tweets DF
    Returns a cleaned dataframe of tweet data and saves a pkl file of clean data
    """
    # clean the dataframe and make it ready for text processing
    tweetsDF = CleanTweetsDataFrame(tweetsDF)

    return tweetsDF


def SpacyTokenizerLemmatizer(text, extraStopWords=[]):
    """
    Takes a string, tokenizes it, then returns a list of lemmatized words as long as they
    are not spacy stop words
    """
    tokens = tokenizer(text)
    return [
        i.lemma_
        for i in tokens
        if i.is_stop is False and i.lemma_ not in extraStopWords
    ]


def ProcessText(text):
    """
    processes either a string or list of tokenized words
    """
    if isinstance((text), (str)):
        # remove non-word characters and lower the letters
        text = re.sub(r"<[^>]*>", r"", text)
        text = re.sub(r"#(\w+)", "", text)
        text = re.sub(r"@", "", text)
        text = re.sub(r"[^a-zA-Z0-9\s]+", r"", text.lower())
        # remove url strings from text
        text = RemoveUrl(text)
        # remove extra spaces
        text = re.sub(r"^ +", r"", text)
        text = re.sub(r" +", r" ", text)
        return text
    if isinstance((text), (list)):
        return_list = []
        for i in range(len(text)):
            # remove non-word characters and lower the letters
            temp_text = re.sub(r"<[^>]*>", r"", text[i])
            temp_text = re.sub(r"#(\w+)", "", temp_text)
            temp_text = re.sub(r"@", "", temp_text)
            temp_text = re.sub(r"[^a-zA-Z0-9\s]+", r"", temp_text.lower())
            # remove url strings from text
            temp_text = RemoveUrl(temp_text)
            # remove extra spaces
            temp_text = re.sub(r"^ +", r"", temp_text)
            temp_text = re.sub(r" +", r" ", temp_text)
            return_list.append(temp_text)
        return return_list
    else:
        pass


def RemoveUrl(sample):
    """
    Remove URLs from a sample string
    """
    return re.sub(r"http\S+", "", sample)


def CleanTweetsDataFrame(tweetsDF):
    """
    Function to clean df and return it
    """
    # remove unwanted columns
    tweetsDF = tweetsDF.drop(
        columns=["permalink", "username", "to", "mentions", "hashtags", "geo"],
        errors="ignore",
    )
    logging.info("Unwanted columns dropped.")

    # convert types accordingly
    tweetsDF.id = tweetsDF.id.apply(pd.to_numeric)
    tweetsDF.favorites = tweetsDF.favorites.apply(pd.to_numeric)
    tweetsDF.retweets = tweetsDF.retweets.apply(pd.to_numeric)
    tweetsDF.date = tweetsDF.date.apply(getDateFromDatetime)
    logging.info("Columns converted to corresponding types.")

    # drop duplicates, but sort by date first and keep the earliest date duplicate tweet
    logging.info(
        "Dropping {} duplicate tweets and keeping the earliest duplicate tweets.".format(
            len(tweetsDF[tweetsDF.duplicated(["text"])])
        )
    )
    tweetsDF = tweetsDF.sort_values("date", ascending=False)
    tweetsDF = tweetsDF.drop_duplicates(subset="text", keep="last")

    # drop nan text, date or id
    for columnName in ["id", "date", "text"]:
        tweetsDF = tweetsDF[tweetsDF[columnName].notna()]

    # fill nans in retweets and favourites with 0
    for columnName in ["retweets", "favorites"]:
        tweetsDF[columnName] = tweetsDF[columnName].fillna(0)

    logging.info(
        "Rows with NaN id, date, text dropped and NaN favorites and retweets set to 0."
    )

    # print number of nan values in each column
    for columnName in ["id", "date", "retweets", "favorites", "text"]:
        nanCount = tweetsDF[columnName].isna().sum()
        logging.info(
            "There are {} Nan values in {} column.".format(nanCount, columnName)
        )

    # convert datetime objects into integers (timestamp)
    tweetsDF.date = tweetsDF.date.apply(lambda x: int(datetime.timestamp(x)))

    return tweetsDF


def getDateFromDatetime(inputDateString):
    """
    Given a datetime string - return a date object + 1 day ahead since
    tweets from day X are registered to midnight at day X+1
    """
    dateOnly = inputDateString.split(" ")[0]
    dateOnlyList = [int(x) for x in dateOnly.split("-")]
    returnDate = datetime(dateOnlyList[0], dateOnlyList[1], dateOnlyList[2], 0, 0, 0)
    
    return returnDate
