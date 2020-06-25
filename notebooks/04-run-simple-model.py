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

from get_price import get_price_data
import pandas as pd
from datetime import date, datetime

# +
## download price data for apple

# tickers = ['AAPL', 'MSFT', '^GSPC']
tickers = 'AAPL'
start_date = '2016-01-01'
end_date = '2020-01-01'

priceDataDF = get_price_data(tickers,start_date,end_date,0.005)
# -

priceDataDF

# +
import matplotlib.pyplot as plt

plt.figure(figsize=(15,7))
plt.plot(priceDataDF.index, priceDataDF.raw_poc)
plt.show()
# -

priceDataDF.dtypes



priceDataDF['int_date'] = [(datetime(2020,1,1,0,0,0) - x).days for x in priceDataDF.index.tolist()]

priceDataDF['date']=priceDataDF.index.tolist()
priceDataDF=priceDataDF.set_index('int_date')
priceDataDF.tail()

print(len(priceDataDF))
print(len(priceDataDF.index.unique()))

fileName = 'usatoday_2016-01-01_till_2020-01-01.csv_processed_and_grouped_by_date_agg_mean.pkl'
newsDF = pd.read_pickle(fileName)
newsDF.head()

# introduce lag change
newsDF.index = newsDF.index - 1
newsDF.head()

print(len(newsDF))
print(len(newsDF.index.unique()))







targetDF = priceDataDF[['positive_poc']]
targetDF.head()



mergedDF = pd.merge(newsDF, targetDF, how='inner', on='int_date')
mergedDF.head()

mergedDF.to_pickle('apple-data-set-with-tweets.pkl')







from sklearn.ensemble import RandomForestClassifier,RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score





train_data = mergedDF.drop(columns=['positive_poc', 'friday paper','look friday'])
target = mergedDF[['positive_poc']]





# +
# split data into test and train set
X_train, X_test, y_train, y_test = train_test_split(
    np.array(train_data), np.array(target), test_size=0.3, random_state=1)

# X_train = X_train.fillna(0.0) ## need to check this - why Nan are produced by split above in 'somethign friday'
# X_test = X_test.fillna(0.0)

# +
# np.where(np.isnan(X_train))
# print(X_train.columns.tolist()[1849], X_train.columns.tolist()[2619])
# -



# +
# Create the model with 100 trees
# model = RandomForestClassifier(n_estimators=100, 
#                                bootstrap = True,
#                                max_features = 'sqrt')

model = RandomForestRegressor(n_estimators = 1000, random_state = 1, n_jobs = -1)
# Fit on training data
model.fit(X_train, np.ravel(y_train))

# Actual class predictions
predictions = model.predict(X_test)

# metrics.accuracy_score(y_test, predictions)
# -

print("AUC score:")
print(roc_auc_score(y_test, predictions))
print('---')
# Let's binarize and look at the confusion matrix
preds = [1 if val > 0.5 else 0 for val in predictions]
print('Confusion Matrix:')
print(metrics.confusion_matrix(y_test, preds))
print('---')
# Lets look at the accuracy
print('Acurracy:')
print(accuracy_score(y_test, preds))
print('---')







mergedDF
