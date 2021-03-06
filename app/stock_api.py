import json
from typing import List, Tuple
from flask_migrate import current
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta

import pandas_ta as ta
from pandas import DataFrame, Series
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

def generate_alerts(period: str ='100d', clip_today=False, codes=[]):
    if not codes:
        codes = Stock.query.all()
    else:
        codes = Stock.query.filter(Stock.stock_code.in_(codes)).all()
    for code in codes:
        stock = Ticker(code.stock_code)
        hist = stock.history(period)
        hist.ta.stoch(high='high', low='low', k=14, d=3, append=True)
        hist.ta.stoch(high='high', low='low', k=50, d=3, append=True)
        hist['buy_K'] = hist.apply(lambda x: x['STOCHk_14_3_3']>70 and x['STOCHk_50_3_3'] < 30, axis=1)
        hist['sell_K'] = hist.apply(lambda x: x['STOCHk_14_3_3']<30 and x['STOCHk_50_3_3'] > 70, axis=1)
        dt = get_buy_sell_info(hist)
        dt['Stock Code'] = code
        if clip_today:
            dt = dt[dt['Date'] >= datetime.combine(date.today(), datetime.min.time())]
        for _, row in dt.iterrows():
            alert = Alert(date=row['Date'],
                        trade_type=row['Trade Type'],
                        stock_id=code.id,
                        alert_price=row['Entry Price'])
            db.session.add(alert)
    db.session.commit()

def get_alerts():
    query = Alert.query.join(Stock.alerts).with_entities(Alert.date,
                                                        Alert.trade_type,
                                                        Stock.stock_code,
                                                        Alert.alert_price
                                                        ).order_by(Alert.id)
    last_day = query.filter(Alert.date == date.today()).all()
    last_week = query.filter(Alert.date > date.today() - timedelta(70)).all()
    return append_current_prices(last_day), append_current_prices(last_week)

def insert_stock(market: str, code: str):
    stock_info = Ticker(code).info
    new_stock = Stock(market=market, 
                    stock_code=code,
                    company_name=stock_info['longName'],
                    entry_price=round(stock_info['currentPrice'], 2))
    db.session.add(new_stock)
    db.session.commit()
    generate_alerts('5000d', codes=[code])

def delete_stocks(ids: List):
    Stock.query.filter(Stock.id.in_(ids)).delete()
    db.session.commit()

def historical_model(amt: int = None, trade_type: str = None) -> List[Tuple]:
    query = Alert.query.join(Stock.alerts).with_entities(
                                            Alert.date,
                                            Alert.trade_type,
                                            Stock.stock_code,
                                            Alert.alert_price
    )
    if query.count() == 0:
        return None
    today = date.today()
    date_filters = [2, 5, 10]
    date_filters = [today - relativedelta(years=x) for x in date_filters]

    queries = [query.filter(Alert.date >= dt_f) for dt_f in date_filters]
    if trade_type != 'Both':
        data = [q.filter(Alert.trade_type == trade_type).all() for q in queries]
    else:
        data = [q.all() for q in queries]
    
    stocks = list(set([s.stock_code for s in data[2]]))
    current_prices = fetch_current_prices(stocks)

    res = []
    for period in data:
        count_of_trades = len(period)
        portfolio_value = 0
        for t in period:
            diff = t.alert_price - (current_prices[t.stock_code] or 0)
            if t.trade_type == 'Sell':
                portfolio_value += diff
            else:
                portfolio_value -= diff
        res.append((round(count_of_trades, 2), round(portfolio_value, 2)))

    return res

def append_current_prices(rows):
    if len(rows) == 0:
        return rows
    stocks = set([r.stock_code for r in rows])
    current_prices = fetch_current_prices(stocks)
    res = []
    for r in rows:
        r = dict(r)
        r['current_price'] = current_prices[r['stock_code']]
        res.append(r)

    return res

def fetch_current_prices(stocks: List):
    # IDK why but the download function doesn's work where list contains dot_named_stocks
    dot_named_stocks = [s for s in stocks if '.' in s]
    stocks = [s for s in stocks if s not in dot_named_stocks]
    dots_is_empty = len(dot_named_stocks) == 0
    normals_is_empty = len(stocks) == 0

    current_prices = Series(dtype=float)
    if not normals_is_empty:
        current_prices = current_prices.append(download(stocks + [''],
                            period='1d',
                            # interval='15m',
                            show_errors=False,
                            rounding=True)['Close'].iloc[-1])
    if not dots_is_empty:
        current_prices = current_prices.append(download(dot_named_stocks + [''],
                                                period='1d',
                                                # interval='15m',
                                                show_errors=False,
                                                rounding=True)['Close'].iloc[-1])
    return current_prices