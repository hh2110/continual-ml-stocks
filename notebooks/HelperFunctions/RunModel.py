from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def do_ml(merged_df, test_size, ml_model, **kwargs):
    train_data = merged_df.drop(
        columns=[
            "lagged_poc",
            "price_date",
            "label_id",
            # "Low",
            # "High",
            # "Open",
            # "Close",
            # "Adj Close",
            # "positive_poc",
            "negative_poc",
        ]
    )
    target = merged_df[["lagged_poc"]]
    X_train, X_test, y_train, y_test = train_test_split(
        np.array(train_data), np.array(target), test_size=test_size, random_state=1
    )

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
    fiDF["fi"] = featureImportances
    fiDF["f"] = train_data.columns
    fiDF = fiDF.sort_values("fi", ascending=False)
    fiDF.head()
    nf = 50
    plt.rcParams.update({"font.size": 7})
    plt.figure(figsize=(6, 4))
    plt.plot(fiDF.f.iloc[0:nf], fiDF.fi.iloc[0:nf])
    plt.xticks(rotation=90)
    plt.show()
