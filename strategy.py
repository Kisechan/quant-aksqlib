# strategy.py
import pandas as pd
import numpy as np
import config

def generate_weekly_signals(prices: pd.DataFrame, momentum: pd.DataFrame, top_k: int, rebalance_freq: str = "W-FRI"):
    """
    生成每个 rebalance 日期（默认每周五）应持有的标的布尔矩阵 signals:
      signals.loc[date, ticker] = 1 表示该周持有该ticker
    策略：
      - 在每个 rebalance 点，使用当日的 momentum 值排序，选出 top_k
      - 可扩展：增加 200 日均线过滤等
    """
    if top_k is None:
        top_k = config.TOP_K

    # 取每个周的最后一个交易日作为调仓日
    rebal_dates = momentum.resample(rebalance_freq).last().dropna().index
    # prepare signals as DataFrame of zeros
    signals = pd.DataFrame(0, index=momentum.index, columns=momentum.columns)

    for d in rebal_dates:
        if d not in momentum.index:
            # find previous available trading date
            d = momentum.index[momentum.index.get_loc(d)]
        row = momentum.loc[d]
        # 排序，去掉 NaN
        ranked = row.rank(ascending=False, method='first')
        selected = ranked[ranked <= top_k].index.tolist()
        # fill signals from this date (inclusive) until next rebalance date (exclusive)
        # find next rebal date
        idx = rebal_dates.get_loc(d)
        if idx + 1 < len(rebal_dates):
            end_date = rebal_dates[idx + 1]
        else:
            end_date = momentum.index[-1] + pd.Timedelta(days=1)
        mask = (signals.index >= d) & (signals.index < end_date)
        signals.loc[mask, selected] = 1

    return signals
