import pandas as pd
from datetime import date, datetime
from pandas_datareader import data
import math


def get_price_data(
    symbol: str, start_date: str, end_date: str, threshold: float, close_shift_step: int
):
    """
    :param symbol: ticker
    :param start_date: iso-format
    :param end_date: iso-format
    :param threshold: significance limit
    :param close_shift_step:
    :return: price df
    """
    price_data = data.DataReader(symbol, "yahoo", start_date, end_date)
    price_data["y_close"] = price_data["Close"].shift(close_shift_step)
    price_data.dropna(inplace=True)
    price_data["raw_poc"] = (price_data["Close"] - price_data["y_close"]) / price_data[
        "y_close"
    ]
    # could use np vectorize if the data is too large?
    # could just combined label +1 & -1 ?
    price_data["positive_poc"] = price_data["raw_poc"].apply(
        lambda x: 1 if x > threshold else 0
    )
    price_data["negative_poc"] = price_data["raw_poc"].apply(
        lambda x: 1 if x < -threshold else 0
    )

    return price_data


def get_price_df(tickers, start_date, end_date, threshold, close_shift_step):
    priceDataDF = get_price_data(
        tickers, start_date, end_date, threshold, close_shift_step
    )
    priceDataDF["label_date"] = [
        int(datetime.timestamp(x)) for x in priceDataDF.index.tolist()
    ]
    priceDataDF["price_date"] = priceDataDF.index.tolist()
    priceDataDF = priceDataDF.set_index("label_date")

    return priceDataDF, priceDataDF.columns.tolist()


def get_news_df_and_columns(path_to_pkl_file):
    newsDF = pd.read_pickle(path_to_pkl_file)

    return newsDF, newsDF.columns.tolist()


def merge_news_price_df(news_df, price_df):
    mergedDF = pd.merge(
        news_df, price_df, how="left", on="label_date", suffixes=("_news", "_price")
    )
    mergedDF.sort_values("label_date", inplace=True)

    return mergedDF


def IntroduceLaggedPOC(df, shift_step):
    df["lagged_poc"] = df["positive_poc"].shift(-shift_step)
    df.dropna(inplace=True)

    return df


def TreatWeekendTweets(mergedDF, newsColumns):
    # get list of holiday timestamps by looking our for NaN values in mergedDF
    holiday_days = mergedDF[mergedDF.isnull().any(axis=1)]

    # create a temporary column of dates
    mergedDF["temp_date"] = mergedDF.label_date

    # get mapping of holidays to working days / also populate the
    # temp_date column with working days
    date_mapping_df, mergedDF = CreateMappingBetweenHolidaysAndWorkdays(
        holiday_days, mergedDF
    )
    # reset index to label_date
    mergedDF = mergedDF.set_index("label_date")

    # sum tweets occuring on holidays with following working day
    mergedDF = GroupTweetsOnHolidays(mergedDF, date_mapping_df, newsColumns)
    # temp_date columns is no longer required
    mergedDF.drop(columns=["temp_date"], inplace=True)

    # finally drop the holiday rows since they contain NaN price data
    mergedDF = mergedDF.loc[~mergedDF.index.isin(date_mapping_df.holiday_date.tolist())]

    return mergedDF


def GroupTweetsOnHolidays(mergedDF, date_mapping_df, newsColumns):
    # group by on temp date and sum news columns - keep last price columns
    priceColumns=[]
    for col in mergedDF.columns.tolist():
        if col not in newsColumns:
            priceColumns.append(col)
    aggDict = {k:'sum' for k in newsColumns}
    aggDict.update({k:'last' for k in priceColumns})
    summedDF = mergedDF.groupby('temp_date').agg(aggDict)

    return summedDF


def CreateMappingBetweenHolidaysAndWorkdays(holiday_days, mergedDF):
    date_mapping_df = pd.DataFrame(columns=["holiday_date", "working_date"])
    # loop through the holiday days
    # find the following working day and append the
    # date_mapping df accordingly
    for date_number in holiday_days.label_date.tolist():
        # take the index of the date_number we are considering in the loop
        current_index = mergedDF.loc[mergedDF.label_date == date_number].index.values[0]
        # initialise the next_index variable (this will be increased in the while loop)
        next_index = current_index
        # initialise the while loop variable (the current date_number refers to a
        # NULL price data since it is a holiday)
        isnull = True
        while_loop_check = 0
        while isnull:  # need to find the next index when raw_poc is not Nan
            next_index += 1
            next_poc = mergedDF.loc[next_index].raw_poc
            if math.isnan(next_poc) == False:
                # if poc exists (not nan) then we have found the "following working day"
                next_label_date = mergedDF.loc[next_index].label_date
                date_mapping_df = date_mapping_df.append(
                    {"holiday_date": date_number, "working_date": next_label_date},
                    ignore_index=True,
                )
                isnull = False
                # populate the temp_date column with the "next working day"
                mergedDF.loc[current_index, "temp_date"] = next_label_date
            while_loop_check +=1
            if while_loop_check > 10:
                print("while loop break", date_number)
                break

    return date_mapping_df, mergedDF
