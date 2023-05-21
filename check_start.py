import pytz
import pandas as pd

from datetime import datetime, timedelta
from binance.client import Client
from binance.enums import HistoricalKlinesType

def date_to_milliseconds(d):
    """Convert UTC date to milliseconds
    If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"
    See dateparse docs for formats http://dateparser.readthedocs.io/en/latest/
    :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
    :type date_str: str
    """
    # get epoch value in UTC
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    # if the date is not timezone aware apply UTC timezone
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)

    # return the difference in time
    return int((d - epoch).total_seconds() * 1000.0)

def _get_beginning(symbol):
    client = Client("", "")
    d = datetime.now() - timedelta(days=4000)
    start_ts = date_to_milliseconds(d)
    data = client._klines(
        klines_type=HistoricalKlinesType.SPOT,
        symbol=symbol,
        interval=Client.KLINE_INTERVAL_5MINUTE,
        limit=None,
        startTime=start_ts,
        endTime=None,
    )
    df = pd.DataFrame(data)
    df[0] = pd.to_datetime(df[0], unit="ms")
    # print(df.head(10))
    print(symbol, " data starts at ", df.iloc[0, 0])

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

for ticker in tickers:
  _get_beginning(ticker)