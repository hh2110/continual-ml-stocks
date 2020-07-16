from get_price import get_price_data
import pandas as pd
from datetime import date, datetime
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier,RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score


def get_price_df(tickers, start_date, end_date, threshold, close_shift_step):

    priceDataDF = get_price_data(tickers, start_date, end_date, threshold, close_shift_step)
    priceDataDF['label_date'] = [int(datetime.timestamp(x)) for x in priceDataDF.index.tolist()]
    priceDataDF['date'] = priceDataDF.index.tolist()
    priceDataDF = priceDataDF.set_index('label_date')
    return priceDataDF

def get_news_df(path_to_pkl_file):
    newsDF = pd.read_pickle(path_to_pkl_file)
    return newsDF



def merge_news_price_df(news_df, price_df, shift_step):
    mergedDF = pd.merge(news_df, price_df, how='inner', on='label_date')
    mergedDF['lagged_poc']=mergedDF['positive_poc'].shift(-shift_step)
    mergedDF.drop(mergedDF.index.max(), inplace=True)
    return mergedDF

def do_ml(merged_df, test_size, ml_model, **kwargs):
    train_data = merged_df.drop(columns=['lagged_poc','date_y','label_id','Low','High','Open','Close','Adj Close','positive_poc','negative_poc'])
    target = merged_df[['lagged_poc']]
    X_train, X_test, y_train, y_test = train_test_split(
        np.array(train_data), np.array(target), test_size=test_size, random_state=1)

    model = ml_model(**kwargs)

    # Fit on training data
    model.fit(X_train, np.ravel(y_train))

    # Actual class predictions
    predictions = model.predict(X_test)

    confusion_matrix = metrics.confusion_matrix(y_test, predictions)
    accuracy_score = metrics.accuracy_score(y_test, predictions)

    # feature importance
    plot_feature_importance(model, train_data)

    return confusion_matrix, accuracy_score


def plot_feature_importance(model, train_data):
    featureImportances = model.feature_importances_
    fiDF = pd.DataFrame()
    fiDF['fi'] = featureImportances
    fiDF['f'] = train_data.columns
    fiDF = fiDF.sort_values('fi', ascending=False)
    fiDF.head()
    nf = 50
    plt.rcParams.update({'font.size': 12})
    plt.figure(figsize=(16, 8))
    plt.plot(fiDF.f.iloc[0:nf], fiDF.fi.iloc[0:nf])
    plt.xticks(rotation=90)
    plt.show()


price_df = get_price_df('MSFT', '2016-01-01', '2020-01-01', 0.005, 1)
news_df = get_news_df('FT_merged_w_average_bow.pkl')
merged_df = merge_news_price_df(news_df, price_df, 1)
result_confusion_matrix, result_accuracy_score = do_ml(merged_df, 0.4, RandomForestClassifier, n_estimators=500, bootstrap = True, max_features = 'sqrt')
print(result_confusion_matrix)
print(result_accuracy_score)
