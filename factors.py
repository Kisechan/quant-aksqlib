# factors.py
import pandas as pd
import numpy as np
import config

def compute_momentum(prices: pd.DataFrame, window: int) -> pd.DataFrame:
    """
    计算过去 window 天的总收益（简单收益），返回与 prices 对齐的 DataFrame（每日对应每只ETF的动量）
    使用 (P_t / P_{t-window} - 1)
    """
    mom = prices / prices.shift(window) - 1.0
    return mom

def compute_volatility(prices: pd.DataFrame, window: int) -> pd.DataFrame:
    """
    用对数收益计算滑动波动率（年化）
    """
    lr = np.log(prices / prices.shift(1))
    vol = lr.rolling(window=window).std() * (config.TRADING_DAYS_PER_YEAR ** 0.5)
    return vol
