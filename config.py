# config.py
TICKERS = ["588750", "588080", "518800", "159205", "159622", "159550"]
START_DATE = "2018-01-01"
END_DATE = None   # None 表示取到最新
REBALANCE_FREQ = "W-FRI"  # 每周五收盘后调仓 (pandas 重采样规则)
MOMENTUM_WINDOW = 60      # 动量窗口（过去 N 个交易日）
TOP_K = 1                 # 持仓 Top-K（可改为2或3）
INITIAL_CAPITAL = 100000.0
FEE_RATE = 0.0003         # 手续费率（买入/卖出都按此）
SLIPPAGE_PCT = 0.0005     # 滑点（按成交额比例）
TRADING_DAYS_PER_YEAR = 252
POSITION_ALLOCATION = "equal"  # "equal" or "risk_parity"
RISK_PARITY_VOL_WINDOW = 60    # 计算波动率窗口，用于风险平价
RISK_FREE_RATE = 0.03          # 年化无风险利率（用于夏普）
