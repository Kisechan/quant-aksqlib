import akshare as ak
import pandas as pd
import os

# 确保 data 文件夹存在
os.makedirs("data", exist_ok=True)

def get_daily_stock(symbol="000001", start_date="20220101", end_date="20250922"):
    """
    获取指定股票代码在指定日期范围内的历史日线数据，并保存到 data 文件夹
    :param symbol: 股票代码, e.g., "000001"
    :param start_date: 开始日期, e.g., "20220101"
    :param end_date: 结束日期, e.g., "20250922"
    :return: pandas.DataFrame
    """
    stock_df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
    if stock_df.empty:
        raise ValueError(f"无法获取股票 {symbol} 的数据。请检查股票代码和日期范围。")
    stock_df = stock_df.set_index('日期')
    stock_df.index = pd.to_datetime(stock_df.index)

    # 保存数据到 data 文件夹
    file_path = f"data/stock_{symbol}.csv"
    stock_df.to_csv(file_path, encoding="utf-8-sig")
    print(f"数据已保存到 {file_path}")

    return stock_df