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
import pandas as pd
from datetime import date
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
font = {'size'   : 16}

plt.rc('font', **font)
# -

# ## Get Data

fromDate = date(2016,1,1)
toDate = date(2020,1,1)
fileName = 'usatoday_{}_till_{}.csv'.format(fromDate, toDate)
tweetsDF = pd.read_csv(fileName, index_col=0)
tweetsDF.text = tweetsDF.text.fillna('none')
tweetsDF.head()

tweetsDF['textLength'] = tweetsDF.text.apply(lambda x: len(str(x)))

# ## Explore numerical columns

tweetsDF.describe()

plt.figure(figsize=(15,9))
plt.subplot(2,2,1)
sns.distplot(tweetsDF.retweets, hist_kws={'log':True}, kde=False)
plt.subplot(2,2,2)
sns.distplot(tweetsDF.favorites, hist_kws={'log':True}, kde=False)
plt.subplot(2,2,3)
sns.distplot(tweetsDF.textLength, kde=False)



# ## Explore text column - word distribution



# +
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import text
# https://towardsdatascience.com/a-complete-exploratory-data-analysis-and-visualization-for-text-data-29fb1b96fb6a


def get_top_n_words(corpus, n=None, removeStopWords = False, input_ngram_range=(1,1)):
    extraStopWords = ['https','http','ly','usat']
    if removeStopWords:
        vec = CountVectorizer(ngram_range=input_ngram_range, stop_words=text.ENGLISH_STOP_WORDS.union(extraStopWords)).fit(corpus)
    elif removeStopWords==False:
        vec = CountVectorizer(ngram_range=input_ngram_range).fit(corpus)
        
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    
    return words_freq[:n]

def PlotWordDistribution(titleString, numberOfWords, ngram_range=(1,1), stopWords=False):
    common_words = get_top_n_words(tweetsDF.text, numberOfWords, stopWords, ngram_range)
    df1 = pd.DataFrame(common_words, columns = ['TweetText' , 'Count'])
    plt.figure(figsize=(12,7))
    sns.barplot(df1['TweetText'], df1['Count'])
    plt.xticks(rotation=90)
    plt.title(titleString)
    plt.show()


# -

PlotWordDistribution('Unigram with stopwords', 25)

PlotWordDistribution('Unigram without stopwords', 25, (1,1), True)

PlotWordDistribution('Bigram with stopwords', 25, (2,2), False)

PlotWordDistribution('Bigram without stopwords', 25, (2,2), True)











# ## old code






