import time
import dateparser
import pytz
import json
import pandas as pd
from helpers import *

from datetime import datetime, timedelta
from binance.client import Client
from binance.enums import HistoricalKlinesType
from binance.helpers import convert_ts_str


data_path = "data"


def _get_historical_klines(symbol, interval, days, end_str=None, futures=True):
    """Get Historical Klines from Binance
    See dateparse docs for valid start and end string formats http://dateparser.readthedocs.io/en/latest/
    If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"
    :param symbol: Name of symbol pair e.g BNBBTC
    :type symbol: str
    :param interval: Biannce Kline interval
    :type interval: str
    :param start_str: Start date string in UTC format
    :type start_str: str
    :param end_str: optional - end date string in UTC format
    :type end_str: str
    :return: list of OHLCV values
    """
    # create the Binance client, no need for api key
    client = Client("", "")
    # init our list
    output_data = []
    # setup the max limit
    limit = 500
    # convert interval to useful value in seconds
    timeframe = interval_to_milliseconds(interval)
    # convert our date strings to milliseconds
    d = datetime.now() - timedelta(days=days)
    start_ts = date_to_milliseconds(d)
    # if an end time was passed convert it
    end_ts = None
    if end_str:
        end_ts = date_to_milliseconds(end_str)
    idx = 0
    # it can be difficult to know when a symbol was listed on Binance so allow start time to be before list date
    symbol_existed = False
    while True:
        if futures:
            klines_type = HistoricalKlinesType.FUTURES
        else:
            klines_type = HistoricalKlinesType.SPOT
        # fetch the klines from start_ts up to max 500 entries or the end_ts if set
        print(pd.to_datetime(start_ts, unit="ms"))
        temp_data = client._klines(
            klines_type=klines_type,
            symbol=symbol,
            interval=interval,
            limit=limit,
            startTime=start_ts,
            endTime=end_ts,
        )
        # handle the case where our start date is before the symbol pair listed on Binance
        if not symbol_existed and len(temp_data):
            symbol_existed = True
        if symbol_existed:
            # append this loops data to our output data
            output_data += temp_data
            # update our start timestamp using the last value in the array and add the interval timeframe
            start_ts = temp_data[len(temp_data) - 1][0] + timeframe
        else:
            # it wasn't listed yet, increment our start date
            start_ts += timeframe
        idx += 1
        # check if we received less than the required limit and exit the loop
        if len(temp_data) < limit:
            # exit the while loop
            break
        # sleep after every 3rd call to be kind to the API
        if idx % 3 == 0:
            time.sleep(1)
    return output_data

def get_historical_data(
    symbol,
    days,
    interval=Client.KLINE_INTERVAL_5MINUTE,
    end=None,
    futures=False,
):
    data = _get_historical_klines(symbol, interval, days, end_str=end, futures=futures)
    df = pd.DataFrame(data)

    # format
    col_names = [
        "time",
        symbol + " price",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_asset_volume",
        "number_of_trades",
        "taker_buy_base_asset_volume",
        "taker_buy_quote_asset_volume",
        "ignore",
    ]
    rename_cols = {}
    for i in range(len(df.columns)):
        rename_cols[df.columns[i]] = col_names[i]
    df.rename(
        columns=rename_cols,
        inplace=True,
    )
    df.drop(
        columns=[
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "number_of_trades",
            "taker_buy_base_asset_volume",
            "taker_buy_quote_asset_volume",
            "ignore",
        ],
        axis=1,
        inplace=True,
    )
    df.set_index("time", inplace=True)
    df.index = pd.to_datetime(df.index, unit="ms")

    df.to_pickle(data_path + symbol + ".pkl")
    return df

def make_master_df(tickers):
    df = pd.DataFrame()
    for ticker in tickers:
        temp_df = pd.read_pickle(data_path + ticker + ".pkl")
        print(temp_df.head(5))
        df = pd.concat([df, temp_df], axis=1, join="outer")

    # this happens to be the cutoff when we can rely on the OP data
    df = df.iloc[3108:]
    print(df.head(5))

    df.to_pickle(data_path + "master_df.pkl")

    # get returns and correlation matrix
    # Assuming your dataframe is named 'df'
    df = df.astype(float)
    returns_df = df.pct_change().dropna()
    correlation_matrix = returns_df.corr()

    # Print the returns dataframe
    print("Returns:")
    print(returns_df.head())

    df.to_pickle(data_path + "master_df_returns.pkl")
    df.to_csv("master_df_returns.csv")

    # Print the correlation matrix
    print("Correlation Matrix:")
    print(correlation_matrix)

    df.to_markdown("correlations.md")



tickers = [
    "BTCUSDT", 
    "ETHUSDT", 
    "XRPUSDT", 
    "LTCUSDT", 
    "RNDRUSDT", 
    "ARBUSDT", 
    "PEPEUSDT", 
    "MATICUSDT", 
    "CFXUSDT", 
    "DOGEUSDT", 
    "SOLUSDT", 
    "SUIUSDT", 
    "INJUSDT", 
    "LDOUSDT", 
    "FTMUSDT", 
    "APTUSDT", 
    "OPUSDT", 
    "ADAUSDT",
]

# this is the subset of tickers that have data from 06-01-2022
# kinda arbitrary, but had to draw the line somewhere
# e.g. sui data only goes back a few weeks
early_tickers = [
    "BTCUSDT", 
    "ETHUSDT", 
    "XRPUSDT", 
    "LTCUSDT", 
    "RNDRUSDT", 
    # "ARBUSDT", 
    # "PEPEUSDT", 
    "MATICUSDT", 
    "CFXUSDT", 
    "DOGEUSDT", 
    "SOLUSDT", 
    # "SUIUSDT", 
    "INJUSDT", 
    "LDOUSDT", 
    "FTMUSDT", 
    # "APTUSDT", 
    "OPUSDT", 
    "ADAUSDT",
]

def get_5_min_data_for_symbols(symbols):
    for symbol in symbols:
        result = get_historical_data(symbol, 365)
        # print("--- " + symbol + " ---")
        # print(result.head(5))
        # print(result.tail(5))

get_5_min_data_for_symbols(tickers)
make_master_df(early_tickers)
