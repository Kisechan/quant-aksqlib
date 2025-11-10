# portfolio.py
import pandas as pd
import numpy as np
import config
from typing import Tuple

def compute_positions(signals: pd.DataFrame, prices: pd.DataFrame, allocation: str = "equal",
                      vol_window: int = 0) -> pd.DataFrame:
    """
    根据 signals 计算每日的目标仓位权重 weight_df（每列为每只ETF的资金权重，合计为1或0）
    allocation: "equal" or "risk_parity"
    vol_window: 若 risk_parity, 计算波动率窗口
    """
    weight = signals.copy().astype(float)
    for date in signals.index:
        active = signals.columns[signals.loc[date] == 1].tolist()
        if len(active) == 0:
            weight.loc[date, :] = 0.0
            continue
        if allocation == "equal":
            w = 1.0 / len(active)
            weight.loc[date, active] = w
            weight.loc[date, weight.columns.difference(active)] = 0.0
        elif allocation == "risk_parity":
            # 以当天之前 vol_window 天波动率作为风险度量（用近似：历史日收益std）
            if vol_window is None:
                vol_window = config.RISK_PARITY_VOL_WINDOW
            hist = prices.loc[:date].pct_change().iloc[-vol_window:]
            vols = hist.std() * (config.TRADING_DAYS_PER_YEAR ** 0.5)
            vols = vols.replace(0, np.nan)
            vols = vols[active].fillna(vols.mean())  # 防止全为nan
            inv_vol = 1.0 / vols
            w = inv_vol / inv_vol.sum()
            for t in weight.columns:
                weight.loc[date, t] = float(w.get(t, 0.0) if t in active else 0.0)
        else:
            raise ValueError("Unknown allocation")
    return weight

def backtest_from_weights(weights: pd.DataFrame, prices: pd.DataFrame, initial_cash: float,
                          fee_rate: float, slippage: float) -> Tuple[pd.Series, pd.DataFrame]:
    """
    向量化回测：假设根据 weights 在每个交易日以当日收盘价调整到目标权重（在真实场景应按调仓日成交）
    为简单起见：只在 weights 发生变化的日子进行调仓（即信号变动日）；
    返回：净值序列 (pd.Series) 和每日持仓份额 (DataFrame)
    """
    dates = prices.index
    tickers = prices.columns
    cash = initial_cash
    nav = pd.Series(index=dates, dtype=float)
    holdings_shares = pd.DataFrame(0.0, index=dates, columns=tickers)
    holdings_value = pd.DataFrame(0.0, index=dates, columns=tickers)

    # track previous weights to detect rebalance days
    prev_weight = pd.Series(0.0, index=tickers)

    # start with no positions
    for i, date in enumerate(dates):
        price_today = prices.loc[date]
        target_weight = weights.loc[date]

        # check if weights changed (rebalance day) -> adjust portfolio to target weights
        if not np.allclose(target_weight.fillna(0.0).values, prev_weight.fillna(0.0).values):
            # compute current portfolio value before trade (using previous holdings and today's price)
            if i == 0:
                current_value = cash
            else:
                current_value = holdings_shares.iloc[i-1].fillna(0.0) * price_today
                current_value = current_value.sum()
                cash = 0.0  # we treat everything in holdings for simplicity
            total_portfolio = current_value
            # determine target dollars per ticker
            target_dollars = target_weight * total_portfolio
            # compute required share changes
            target_shares = (target_dollars / price_today).fillna(0.0)
            prev_shares = holdings_shares.iloc[i-1] if i > 0 else pd.Series(0.0, index=tickers)
            trade_shares = target_shares - prev_shares
            # compute trade costs
            trade_values = trade_shares.abs() * price_today
            fees = trade_values.sum() * fee_rate
            slippage_cost = (trade_values.sum() * slippage)
            total_costs = fees + slippage_cost
            # adjust total_portfolio for costs
            total_portfolio_after_costs = total_portfolio - total_costs
            if total_portfolio_after_costs <= 0:
                # rare but guard
                total_portfolio_after_costs = 0.0
            # recompute target_dollars proportional to remaining value
            if total_portfolio > 0:
                scale = total_portfolio_after_costs / total_portfolio
            else:
                scale = 0.0
            target_dollars = target_dollars * scale
            # new target shares
            target_shares = (target_dollars / price_today).fillna(0.0)
            holdings_shares.iloc[i] = target_shares
            holdings_value.iloc[i] = holdings_shares.iloc[i] * price_today
            nav.iloc[i] = holdings_value.iloc[i].sum()
            prev_weight = target_weight.copy()
        else:
            # no rebalance: carry forward shares and mark-to-market
            if i == 0:
                holdings_shares.iloc[i] = 0.0
                holdings_value.iloc[i] = 0.0
                nav.iloc[i] = cash
            else:
                holdings_shares.iloc[i] = holdings_shares.iloc[i-1]
                holdings_value.iloc[i] = holdings_shares.iloc[i] * price_today
                nav.iloc[i] = holdings_value.iloc[i].sum()

    # fill forward nav
    nav = nav.fillna(method='ffill').fillna(initial_cash)
    return nav, holdings_shares
