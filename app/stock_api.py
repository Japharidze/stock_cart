from typing import List
from requests import get
import json

import pandas_ta as ta
from faker import Faker
from pandas import DataFrame
from yfinance import Ticker, download

from app import db
from .models import Stock, Alert

def fill_info(df, trade_log, time, buy_sell='Buy'):
    """Writes one trade info into dataframe"""

    # Fill dataframe with info. If price info is not available in the future None is written 
    df_t = DataFrame({'Date': [time],
                        'Trade Type': [buy_sell],
                        'Entry Price': [df['Close'].loc[time]]
                         })

    trade_log = trade_log.append(df_t, ignore_index=True)
    return trade_log

def get_buy_sell_info(df):
    """Agregates all trades information in DataFrame"""
    trade_log = DataFrame(columns=['Date', 'Trade Type', 'Entry Price'])
    
    for buy_time in df.loc[df['buy_K']].index:
        trade_log = fill_info(df, trade_log, buy_time, buy_sell='Buy')

    for sell_time in df.loc[df['sell_K']].index:
        trade_log = fill_info(df, trade_log, sell_time, buy_sell='Sell')
    return trade_log

def get_alerts_old(codes: List = None, period: str = '7d'):
    if not codes:
        return
    cols = ['Date', 'Trade Type', 'Stock Code', 'Entry Price', 'Current Price']
    res = DataFrame(columns=cols)
    for code in codes:
        stock = Ticker(code)
        current_price = download(code, period='5m', interval='1m')['Close'].iloc[0]
        hist = stock.history('100d')
        hist.ta.stoch(high='high', low='low', k=14, d=3, append=True)
        hist.ta.stoch(high='high', low='low', k=50, d=3, append=True)
        hist['buy_K'] = hist.apply(lambda x: x['STOCHk_14_3_3']>70 and x['STOCHk_50_3_3'] < 30, axis=1)
        hist['sell_K'] = hist.apply(lambda x: x['STOCHk_14_3_3']<30 and x['STOCHk_50_3_3'] > 70, axis=1)
        dt = get_buy_sell_info(hist)
        dt['Stock Code'] = code
        dt['Current Price'] = current_price
        dt = dt[cols]
        res = res.append(dt)
    return res

def get_alerts():
    return Alert.query.all()

def insert_stock(market: str, code: str, price: float):
    new_stock = Stock(market=market, 
                    stock_code=code, 
                    entry_price=price)
    db.session.add(new_stock)
    db.session.commit()

def delete_stocks(ids: List):
    Stock.query.filter(Stock.id.in_(ids)).delete()
    db.session.commit()

def generate_all_codes():
    r = get('https://api.iextrading.com/1.0/ref-data/symbols')
    stocks = r.json()
    stock_codes = {'codes': [x['symbol'] for x in stocks]}
    with open('stocks.json', 'w') as f:
        json.dump(stock_codes, f)