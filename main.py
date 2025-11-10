# backtest.py
import pandas as pd
import matplotlib.pyplot as plt
import config
from data_loader import load_price_panel
from factors import compute_momentum, compute_volatility
from strategy import generate_weekly_signals
from portfolio import compute_positions, backtest_from_weights
from metrics import compute_basic_stats

def main():
    # 1. load price data
    prices = load_price_panel(config.TICKERS, config.START_DATE, config.END_DATE)
    print("price shape:", prices.shape)

    # 2. compute factors
    momentum = compute_momentum(prices, config.MOMENTUM_WINDOW)
    vol = compute_volatility(prices, config.RISK_PARITY_VOL_WINDOW)

    # 3. generate weekly signals
    signals = generate_weekly_signals(prices, momentum, top_k=config.TOP_K, rebalance_freq=config.REBALANCE_FREQ)

    # 4. compute weights
    weights = compute_positions(signals, prices, allocation=config.POSITION_ALLOCATION,
                                vol_window=config.RISK_PARITY_VOL_WINDOW)
    # 5. backtest -> nav
    nav, holdings = backtest_from_weights(weights, prices, config.INITIAL_CAPITAL,
                                          fee_rate=config.FEE_RATE, slippage=config.SLIPPAGE_PCT)

    # 6. metrics
    stats = compute_basic_stats(nav)
    print("Performance:")
    for k,v in stats.items():
        print(f"{k}: {v}")

    # 7. plot
    plt.figure(figsize=(10,6))
    plt.plot(nav / nav.iloc[0], label="Strategy NAV (normalized)")
    # benchmark: equal-weight buy-and-hold of all tickers
    bw = prices.mean(axis=1)
    bench_nav = (1 + bw.pct_change().fillna(0)).cumprod()
    bench_nav = bench_nav / bench_nav.iloc[0]
    plt.plot(bench_nav, label="Benchmark (avg ETF)")
    plt.legend()
    plt.title("Backtest NAV")
    plt.show()

if __name__ == "__main__":
    main()
