import requests
import datetime
import json
import pandas as pd

def send_request_to_query_yf(symbol, period1, period2, interval):
    headers = { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    if isinstance(period1, str):
      period1 = int(datetime.datetime.strptime(period1, '%Y-%m-%d').timestamp())
    if isinstance(period2, str):
      period2 = int(datetime.datetime.strptime(period2, '%Y-%m-%d').timestamp())
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?period1={period1}&period2={period2}&interval={interval}'
    return requests.get(url, headers=headers)

def send_request_to_query_yf_range(symbol, range, interval):
    headers = { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={range}&interval={interval}'
    return requests.get(url, headers=headers)
