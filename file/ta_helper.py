# pip install ta==0.11
import ta
import numpy as np
import pandas as pd

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

