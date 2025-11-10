# data_loader.py
import akshare as ak
import pandas as pd
from typing import List
import config

def fetch_etf_daily(ticker: str, start: str, end: str) -> pd.DataFrame:
    """
    拉取 A 股 ETF 日线，返回 DataFrame，索引为 datetime，包含 ['open','high','low','close','volume']。
    akshare 中科创板/沪深 ETF 代码可能需要补后缀/前缀，但 akshare 的 fund_etf_daily_trading 获取 ETF
    使用场景：这里采用 ak.fund_etf_hist_sina（按 ticker）
    """
    # 对于 A 股ETF，akshare 支持 method: ak.fund_etf_hist_sina
    df = ak.fund_etf_hist_sina(symbol=ticker)  # 返回 date, open, high, low, close, volume, turnover
    df = df.rename(columns={"date":"date","open":"open","high":"high","low":"low","close":"close","volume":"volume"})
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date').sort_index()
    # limit by date
    if start:
        df = df[df.index >= pd.to_datetime(start)]
    if end:
        df = df[df.index <= pd.to_datetime(end)]
    return df[['open','high','low','close','volume']]

def load_price_panel(tickers: List[str], start, end) -> pd.DataFrame:
    """
    返回一个 DataFrame，columns 为 tickers，index 为交易日（并集、前向填充），值为收盘价
    """
    price_dict = {}
    for t in tickers:
        print(f"fetching {t} ...")
        df = fetch_etf_daily(t, start, end)
        if df.empty:
            raise RuntimeError(f"No data for {t}")
        price_dict[t] = df['close'].rename(t)
    # 合并为 panel
    price = pd.concat(price_dict.values(), axis=1, keys=price_dict.keys())
    # 排序索引、前向填充（避免交易日缺失短期缺口）
    price = price.sort_index().ffill().dropna(how='all')
    return price
