import numpy as np
import pandas as pd


def realized_vol(df: pd.DataFrame, look_back_period=252):
    df['log_ret'] = np.log(df['close'] / df['close'].shift(1))
    variance = (df['log_ret'] * df['log_ret']).rolling(window=look_back_period).sum() * 252 / (look_back_period - 1)
    return np.sqrt(variance.dropna())


def ewma_vol(df: pd.DataFrame, look_back_period=252):
    weights = [0.94 ** (x - 1) * 0.06 / (1 - 0.94 ** 252) for x in range(1, 253)]
    weights.reverse()
    weights = np.array(weights)

    def calc_ewma(x):
        return np.array(x).dot(weights)

    df["log_ret"] = np.log(df['close'] / df['pre_close']).shift(1)
    df['daily_vol'] = np.sqrt(df['log_ret'] * df['log_ret'] * 252)
    df['ewma_vol'] = df['daily_vol'].rolling(window=look_back_period).apply(calc_ewma)
    return df['ewma_vol'].dropna()


def realized_vol_parkinson(df: pd.DataFrame, look_back_period=252):
    df['hol'] = np.power(np.log(df['high'] / df['low']), 2)
    variance = 1 / (4 * np.log(2)) * df['hol'].rolling(window=look_back_period).sum() * 252 / (look_back_period - 1)
    return np.sqrt(variance).dropna()


def realized_vol_garman_klass(df: pd.DataFrame, look_back_period=252):
    df['hol'] = np.power(np.log(df['high'] / df['low']), 2)
    df['log_ret'] = np.power(np.log(df['close'] / df['pre_close']), 2)
    variance = (.5 * df['hol'] - (2 * np.log(2) - 1) * df['log_ret']).rolling(window=look_back_period).sum() \
               * 252 / (look_back_period - 1)
    return np.sqrt(variance).dropna()


def realized_vol_rogers_satchell(df: pd.DataFrame, look_back_period=252):
    df['hoc'] = np.log(df['high'] / df['close'])
    df['hoo'] = np.log(df['high'] / df['open'])
    df['loc'] = np.log(df['low'] / df['close'])
    df['loo'] = np.log(df['low'] / df['open'])
    variance = (df['hoc'] * df['hoo'] + df['loc'] * df['loo']).rolling(window=look_back_period).sum() \
               * 252 / (look_back_period - 1)
    return np.sqrt(variance).dropna()


def realized_vol_yang_zhang(df: pd.DataFrame, look_back_period=252):
    df['hoo'] = np.log(df['high'] / df['open'])
    df['loo'] = np.log(df['low'] / df['open'])
    df['coo'] = np.log(df['close'] / df['open'])
    df['ooc'] = np.log(df['open'] / df['pre_close'])
    df['coc'] = np.log(df['close'] / df['pre_close'])
    df['rs'] = df['hoo'] * (df['hoo'] - df['coo']) + df['loo'] * (df['loo'] - df['coo'])
    df['oc_sqr'] = df['ooc'] ** 2
    df['cc_sqr'] = df['coc'] ** 2

    close_vol = df['cc_sqr'].rolling(window=look_back_period).sum() * 252 / (look_back_period - 1)
    open_vol = df['oc_sqr'].rolling(window=look_back_period).sum() * 252 / (look_back_period - 1)
    rs = df['rs'].rolling(window=look_back_period).sum() * 252 / (look_back_period - 1)
    k = 0.34 / (1.34 + (look_back_period + 1) / (look_back_period - 1))
    variance = open_vol + k * close_vol + (1 - k) * rs
    return np.sqrt(variance)
