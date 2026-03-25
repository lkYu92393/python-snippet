# pip install tradingview-screener
from tradingview_screener import Query, col

base_col = ['ipo_offer_date', 'name','change', 'close', 'high','low', 'volume', 'volume|1M', 'average_volume_30d_calc', 'market_cap_basic', 'relative_volume']
cus_col = ['description','type','sector','industry'] + base_col

def get_scanner_data(market, _criteria, _col, _order_by = "market_cap_basic"):
    market_string = "america" if market == "us" else "hongkong"
    return Query().select(*_col).set_markets(market_string).where(*_criteria).order_by(_order_by, False).get_scanner_data()

def query_get_all_code(market, _criteria, _col = base_col, _order_by = "market_cap_basic", length=200):
    result_df = None
    result = get_scanner_data(market, _criteria, _col, _order_by)
    result_length = result[0]
    result_df = result[1]
    while (result[0] > 50 and result_df.shape[0] < length):
        result = get_scanner_data(market, _criteria + [col("market_cap_basic") < result_df.iloc[-1]["market_cap_basic"]], _col, _order_by)
        result_df = pd.concat([result_df, result[1]])
    result_df.index = [i for i in range(result_df.shape[0])]
    return [result_length, result_df]

def get_base_criteria(region, in_favorite = False):
    criteria = [
        col('currency').not_like('CNY'),
        col('name').not_like('/P'),
        col('exchange').not_like('OTC'),
    ]
    if in_favorite:
        criteria.append(col('name').isin(FLATTEN_STOCK_CODE[region]))
    return criteria

def get_most_traded_stock(region):
    criteria = [
        *get_base_criteria(region, False),
        col('Value.Traded|1M') > 100000000
    ]
    result = query_get_all_code(region, criteria,length=300)
    name_list = list(result[1]['name'])
    return name_list


