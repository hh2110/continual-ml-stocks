from pandas_datareader import data
import pandas as pd

def get_price_data(symbol:str, start_date:str, end_date:str, threshold:float, close_shift_step:int):
    '''

    :param symbol: ticker
    :param start_date: iso-format
    :param end_date: iso-format
    :param threshold: significance limit
    :param close_shift_step:
    :return: price df
    '''
    price_data = data.DataReader(symbol, 'yahoo', start_date, end_date)

    price_data['y_close'] = price_data['Close'].shift(close_shift_step)
    price_data.dropna(inplace=True)
    price_data['raw_poc'] = (price_data['Close'] - price_data['y_close']) / price_data['y_close']

    # price_data['raw_poc'] = (price_data['Close'] - price_data['Open']) / price_data['Open']

    # could use np vectorize if the data is too large?
    # could just combined label +1 & -1 ?
    price_data['positive_poc'] = price_data['raw_poc'].apply(lambda x: 1 if x > threshold else 0)
    price_data['negative_poc'] = price_data['raw_poc'].apply(lambda x: 1 if x < -threshold else 0)
    return price_data

# tickers = ['AAPL', 'MSFT', '^GSPC']
# tickers = 'AAPL'
#
# start_date = '2016-01-01'
# end_date = '2017-01-01'
#
# print(get_price_data(tickers,start_date,end_date,0.005))