# https://pypi.org/project/tvscreener/
# !pip install tvscreener
from tvscreener import StockScreener, StockField, Market

STOCKFIELD_BASIC = [StockField.UPDATE_TIME, StockField.NAME, StockField.TYPE, StockField.SUBTYPE, StockField.MARKET_CAPITALIZATION, StockField.PRICE, StockField.OPEN, StockField.VOLUME, StockField.VOLUMEXPRICE, StockField.HIGH, StockField.HIGH_1W, StockField.HIGH_1M, StockField.LOW, StockField.LOW_1W, StockField.LOW_1M]
STOCKFIELD_MA    = [StockField.SIMPLE_MOVING_AVERAGE_20, StockField.SMA20_1W, StockField.SMA20_1M, StockField.SIMPLE_MOVING_AVERAGE_50, StockField.SMA50_1W, StockField.SMA50_1M, StockField.EXPONENTIAL_MOVING_AVERAGE_10, StockField.EMA25, StockField.EXPONENTIAL_MOVING_AVERAGE_50, StockField.EXPONENTIAL_MOVING_AVERAGE_100, StockField.EXPONENTIAL_MOVING_AVERAGE_200, StockField.EMA10_1W, StockField.EMA25_1W, StockField.EMA50_1W, StockField.EMA100_1W, StockField.EMA200_1W, StockField.EMA10_1M, StockField.EMA25_1M, StockField.EMA50_1M, StockField.EMA100_1M, StockField.EMA200_1M]
STOCKFIELD_BB    = [StockField.BOLLINGER_UPPER_BAND_20, StockField.BOLLINGER_LOWER_BAND_20, StockField.BB_UPPER_1W, StockField.BB_LOWER_1W, StockField.BB_UPPER_1M, StockField.BB_LOWER_1M]

MARKET_DICT = {
    "us": Market.AMERICA,
    "hk": Market.HONGKONG,
}

def get_default_stock_screener():
    ss = StockScreener()
    ss.select(*STOCKFIELD_BASIC, *STOCKFIELD_MA, *STOCKFIELD_BB)
    ss.where(StockField.CURRENCY != 'CNY', StockField.EXCHANGE != 'OTC')
    if region in list(MARKET_DICT.keys()):
        ss.set_markets(MARKET_DICT[region])
    if type(names) == list && len(names) > 0:
        ss.where(StockField.NAME.isin(name))
    ss.set_range(0, 10000)
    return ss

def get_tv_data(region, names: list, range: int):
    ss = get_default_stock_screener(region, names)
    ss.sort_by(StockField.MARKET_CAPITALIZATION, ascending=False)
    df = ss.get()
    return df

def get_tv_etf_data(region, names: list, , range: int):
    ss = get_default_stock_screener(region, names)
    ss.sort_by(StockField.VOLUMEXPRICE, ascending=False)
    df = ss.get()
    return df

