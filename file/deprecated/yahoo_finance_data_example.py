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


def extract_data_from_json(result_json):
    # example json
    # {
    #   'chart': {'result': [{'meta':'','timestamp':'', 'indicators':dict_keys(['open', 'high', 'volume', 'close', 'low'])}] ,'error': 'sth'}
    # }
    try:
        if 'timestamp' not in result_json['chart']['result'][0].keys():
            return pd.DataFrame()
        timestamp_list = result_json['chart']['result'][0]['timestamp']
        data_list = result_json['chart']['result'][0]['indicators']['quote'][0]
        new_order = ['open','high','low','close','volume']
        sorted_data_list = { key: data_list[key] for key in new_order }

        # Convert timestamps to datetime
        datetime_index = pd.to_datetime(timestamp_list, unit='s')

        # Create DataFrame
        custom_column_names = ['Open', 'High', 'Low', 'Close', 'Volume']
        df = pd.DataFrame(sorted_data_list, index=datetime_index)
        df.columns = custom_column_names  # Assign custom column names
        return df
    except:
        return pd.DataFrame()

