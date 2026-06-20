# pip install ta==0.11
import ta
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def cross_func(this_row, last_row, param_that_cross, param_being_crossed):
    return (last_row[param_that_cross] < last_row[param_being_crossed]
            and this_row[param_that_cross] >= this_row[param_being_crossed])

def ta_bbm(df, window=20, window_dev=2):
    # Initialize Bollinger Bands Indicator
    indicator_bb = ta.volatility.BollingerBands(close=df["Close"], window=window, window_dev=window_dev)
    return (
        indicator_bb.bollinger_mavg(), indicator_bb.bollinger_hband(), indicator_bb.bollinger_lband(
        ), indicator_bb.bollinger_hband_indicator(), indicator_bb.bollinger_lband_indicator()
    )

def forcast(df, period):
    def _forcast(num_array):
        x = np.array([i for i in range(num_array.shape[0])]).reshape(-1, 1)
        y = num_array.to_numpy()
        reg = LinearRegression().fit(x, y)

        return round(reg.predict(np.array([[num_array.shape[0] - 1]]))[0], 5)
    return df.rolling(period).apply(_forcast)

def get_de(src_series: pd.Series):
    EMA5 = src_series.ewm(span=5, adjust=False).mean()
    EMA8 = src_series.ewm(span=8, adjust=False).mean()
    EMA11 = src_series.ewm(span=11, adjust=False).mean()
    EMA14 = src_series.ewm(span=14, adjust=False).mean()
    EMA17 = src_series.ewm(span=17, adjust=False).mean()

    B = forcast(EMA5, 6) + forcast(EMA8, 6) + forcast(EMA11, 6) + \
        forcast(EMA14, 6) - 4 * forcast(EMA17, 6)

    return B.ewm(span=2, adjust=False).mean()


# transcribed from https://github.com/joshuaulrich/TTR/blob/master/src/zigzag.c
def get_zigzag(HL, change=10, initial_signal=0, percent=True, retrace=False, last_extreme=True):

    if type(HL) == pd.Series:
        high = HL
        low = high
    else:
        high = HL.loc[:, "High"]
        low = HL.loc[:, "Low"]

    if percent:
        change /= 100

    ref_index = 0
    ref_price = (high.iloc[0] + low.iloc[0]) / 2
    inf_index = 1
    inf_price = (high.iloc[1] + low.iloc[1]) / 2

    extreme_min = 0.0
    extreme_max = 0.0
    local_min = 0.0
    local_max = 0.0
    signal = initial_signal
    zigzag = [None for _ in range(high.shape[0])]
    zigzag_signal = [None for _ in range(high.shape[0])]

    for i in range(1, HL.shape[0]):
        if percent:
            extreme_min = inf_price * (1 - change)
            extreme_max = inf_price * (1 + change)
        else:
            extreme_min = inf_price - change
            extreme_max = inf_price + change

        local_max = max(inf_price, high.iloc[i])
        local_min = min(inf_price, high.iloc[i])

        if (signal == 0):
            if retrace:
                signal = 1 if inf_price >= ref_price else -1
            else:
                if local_min <= extreme_min:
                    signal = -1

                if local_max >= extreme_max:
                    signal = 1

        if (signal == -1):
            if low.iloc[i] == local_min:
                if (last_extreme) or (low.iloc[i] != low.iloc[i-1]):
                    inf_price = low.iloc[i]
                    inf_index = i
                # else:
                #     if low.iloc[i] != low.iloc[i-1]:
                #         inf_price = low.iloc[i]
                #         inf_index = i
            if retrace:
                extreme_max = inf_price + (ref_price - inf_price) * change

            if high.iloc[i] >= extreme_max:
                zigzag[ref_index] = ref_price
                zigzag_signal[ref_index] = signal
                ref_price = inf_price
                ref_index = inf_index
                inf_price = high.iloc[i]
                inf_index = i
                signal = 1
                continue

        if (signal == 1):
            if high.iloc[i] == local_max:
                if (last_extreme) or (high.iloc[i] != high.iloc[i-1]):
                    inf_price = high.iloc[i]
                    inf_index = i
                # else:
                #     if high.iloc[i] != high.iloc[i-1]:
                #         inf_price = high.iloc[i]
                #         inf_index = i
            if retrace:
                extreme_min = inf_price + (inf_price - ref_price) * change

            if low.iloc[i] <= extreme_min:
                zigzag[ref_index] = ref_price
                zigzag_signal[ref_index] = signal
                ref_price = inf_price
                ref_index = inf_index
                inf_price = low.iloc[i]
                inf_index = i
                signal = -1

    zigzag[ref_index] = ref_price
    zigzag[inf_index] = inf_price
    zigzag_signal[ref_index] = signal
    zigzag_signal[inf_index] = -1 * signal
    return zigzag, zigzag_signal

def mcd(df):
    mm_base = 50
    mm_period = 50
    mm_sens = 1.5

    hot_base = 30
    hot_period = 40
    hot_sens = 0.7

    temp1 = (df["Close"] - df.loc[:,"Close"].shift(1)).apply(lambda x: max(x, 0))
    temp2 = (df["Close"] - df.loc[:,"Close"].shift(1)).apply(abs)

    rsi1 = (temp1.ewm(alpha=1 / mm_period, min_periods=mm_period, adjust=False).mean() /
            temp2.ewm(alpha=1 / mm_period, min_periods=mm_period, adjust=False).mean()) * 100
    rsi_b = mm_sens * (rsi1 - mm_base)
    mm_rsi = rsi_b.copy()
    mm_rsi[mm_rsi > 20] = 20
    mm_rsi[mm_rsi < 0] = 0

    rsi2 = (temp1.ewm(alpha=1 / hot_period, min_periods=hot_period, adjust=False).mean() /
            temp2.ewm(alpha=1 / hot_period, min_periods=hot_period, adjust=False).mean()) * 100
    rsi_m = hot_sens * (rsi2 - hot_base)
    hot_rsi = rsi_m.copy()
    hot_rsi[hot_rsi > 20] = 20
    hot_rsi[hot_rsi < 0] = 0

    # hot is yellow, mm is red

    return hot_rsi, mm_rsi


def add_additional_column_and_remove_dividend(df, additional_function = None):
    new_df = df.copy()
    if "Dividend" in new_df.columns:
        new_df.drop(columns=["Dividend"])

    # new_df["next_open"] = new_df.loc[:, "Open"].shift(-1)
    # new_df["next_close"] = new_df.loc[:, "Close"].shift(-1)
    new_df["last_close"] = new_df.loc[:, "Close"].shift(1)

    def get_n_day_change(days, in_percentage = False):
        numerator = (new_df.loc[:, "Close"] - new_df.loc[:, "Close"].shift(days))
        if in_percentage:
            numerator /= new_df.loc[:, "Close"].shift(days)
        return numerator
    # new_df["1d_Change"] = get_n_day_change(1)
    # new_df["1d_Change_percentage"] = get_n_day_change(1, True)
    new_df["5d_Change"] = get_n_day_change(5)
    new_df["5d_Change_percentage"] = get_n_day_change(5, True)
    # new_df["1dR"] = new_df.loc[:, "Close"] - new_df.loc[:, "Close"].shift(-1)
    # new_df["5dR"] = new_df.loc[:, "Close"] - new_df.loc[:, "Close"].shift(-5)
    # new_df["20dR"] = new_df.loc[:, "Close"] - new_df.loc[:, "Close"].shift(-20)
    # new_df["5dmR"] = new_df.loc[:, "Close"].rolling(
    #     5).apply(lambda x: x.max() - x[0]).shift(-4)
    # new_df["20dmR"] = new_df.loc[:, "Close"].rolling(
    #     20).apply(lambda x: x.max() - x[0]).shift(-19)
    # new_df["30dmR"] = new_df.loc[:, "Close"].rolling(
    #     30).apply(lambda x: x.max() - x[0]).shift(-29)

    new_df["ma60"] = new_df["Close"].rolling(60).mean()

    # [6,9,11,13,25,48,200]
    for i in [9,11,25,48,200]:
        new_df[f"ema{i}"] = new_df.loc[:, "Close"].ewm(span=i, min_periods=0, adjust=False).mean()

    ema_mask = new_df["ema11"] >= new_df["ema25"]

    new_df['ema_bullish'] = 0
    count_true = 0
    count_false = 0

    # Iterate over the DataFrame
    for i in range(len(new_df)):
        if ema_mask.iloc[i]:  # If True
            count_true += 1
            count_false = 0
            new_df.loc[new_df.index[i], 'ema_bullish'] = count_true
        else:  # If False
            count_false += 1
            count_true = 0
            new_df.loc[new_df.index[i], 'ema_bullish'] = -count_false

    new_df["rsi6"] = ta.momentum.RSIIndicator(close=new_df["Close"], window=6).rsi()
    new_df["rsi14"] = ta.momentum.RSIIndicator(close=new_df["Close"], window=14).rsi()
    new_df["rsi14_ma14"] = new_df["rsi14"].rolling(14).mean()

    new_df["bb_dev"] = new_df["Close"].rolling(20).std(ddof=0)
    new_df["bb_bbm"], new_df["bb_bbh"], new_df["bb_bbl"], new_df["bb_bbhi"], new_df["bb_bbli"] = ta_bbm(new_df)
    new_df["super_bbm"], new_df["super_bbh"], new_df["super_bbl"], _, _ = ta_bbm(new_df, 330, 2.5)

    new_df["tsi"] = ta.momentum.TSIIndicator(close=new_df["Close"], window_slow=13, window_fast=5).tsi()
    new_df["tsi_smooth"] = new_df.loc[:, "tsi"].ewm(span=10, min_periods=0, adjust=False).mean()

    new_df["bb_bbm_d"] = new_df.loc[:, "Close"].ewm(span=48, min_periods=0, adjust=False).mean().rolling(2).apply(lambda x: 1 if ((x.iloc[1]-x.iloc[0]) > 0) else 0)

    def bb_pos(row):
        return 2 * (row["Close"] - row["bb_bbm"]) / (row["bb_bbh"] - row["bb_bbl"])
    new_df["bb_pos"] = new_df.apply(bb_pos, axis=1)

    def bb_hpos(row):
        return 2 * (row["High"] - row["bb_bbm"]) / (row["bb_bbh"] - row["bb_bbl"])
    new_df["bb_hpos"] = new_df.apply(bb_hpos, axis=1)

    def bb_lpos(row):
        return 2 * (row["Low"] - row["bb_bbm"]) / (row["bb_bbh"] - row["bb_bbl"])
    new_df["bb_lpos"] = new_df.apply(bb_lpos, axis=1)

    try:
        new_df["zz"], new_df["zz_signal"] = get_zigzag(df.loc[:, "Close"], change=10)
    except:
        print("Fail to get zz.")

    try:
        new_df["de"] = get_de(df.loc[:, "Close"])
        new_df["de_norm"] = 2 * new_df["de"] / \
            (new_df["Close"] + new_df["Open"])
        new_df["de_change"] = new_df["de"].rolling(
            2).apply(lambda x: x.iloc[1] / x.iloc[0] - 1)

        def de_cross(col):
            value = 0
            if col.iloc[1] > 0 and col.iloc[0] < 0:
                value = 1
            elif col.iloc[1] < 0 and col.iloc[0] > 0:
                value = -1
            return value
        new_df["de_cross"] = new_df.loc[:, "de"].rolling(2).apply(de_cross)
    except:
        print("Fail to get DE.")
        sys.exit(1)

    new_df["Volume_ma5"] = new_df.loc[:, "Volume"].rolling(5).mean()
    new_df["Volume_ma5_ratio"] = (new_df.loc[:, "Volume"] / new_df.loc[:, "Volume_ma5"]).apply(lambda x: round(x, 2))
    new_df["Volume_ma20"] = new_df.loc[:, "Volume"].rolling(20).mean()
    new_df["Volume_ma20_ratio"] = (new_df.loc[:, "Volume"] / new_df.loc[:, "Volume_ma20"]).apply(lambda x: round(x, 2))

    # new_df["buyer"], new_df["pre_buyer"], new_df["retail"], new_df["market_maker"] = firehill(df)

    # new_df["deepsea"] = deepsea(df)

    new_df["hot_rsi"], new_df["mm_rsi"] = mcd(new_df)

    if additional_function != None:
        additional_function(new_df)

    return new_df

