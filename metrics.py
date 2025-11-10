# metrics.py
import numpy as np
import pandas as pd
import config

def compute_basic_stats(nav: pd.Series):
    """
    nav: 净值时间序列（以初始资金为基准或直接为资金曲线）
    返回：字典包括年化收益、年化波动、夏普、最大回撤、CAGR
    """
    # daily returns
    returns = nav.pct_change().fillna(0.0)
    # annualized return (CAGR)
    total_days = (nav.index[-1] - nav.index[0]).days
    years = total_days / 365.25
    if years <= 0:
        ann_return = np.nan
    else:
        ann_return = (nav.iloc[-1] / nav.iloc[0]) ** (1/years) - 1.0
    # annualized vol
    ann_vol = returns.std() * (config.TRADING_DAYS_PER_YEAR ** 0.5)
    # sharpe
    if ann_vol != 0:
        sharpe = (ann_return - config.RISK_FREE_RATE) / ann_vol
    else:
        sharpe = np.nan
    # max drawdown
    rolling_max = nav.cummax()
    drawdown = (nav - rolling_max) / rolling_max
    maxdd = drawdown.min()
    # other metrics
    total_return = nav.iloc[-1] / nav.iloc[0] - 1.0
    stats = {
        "total_return": float(total_return),
        "ann_return": float(ann_return) if not np.isnan(ann_return) else None,
        "ann_vol": float(ann_vol),
        "sharpe": float(sharpe),
        "max_drawdown": float(maxdd),
        "start_value": float(nav.iloc[0]),
        "end_value": float(nav.iloc[-1]),
    }
    return stats
