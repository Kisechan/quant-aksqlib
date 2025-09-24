import os
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rcParams

# 确保 figure 文件夹存在
os.makedirs("figure", exist_ok=True)

# 设置 Matplotlib 支持中文
rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为黑体
rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

def plot_results(df, predictions, past_prices, future_predictions, future_dates):
    """
    绘制实际股价和预测股价的对比图，并保存到 figure 文件夹
    :param df: pandas.DataFrame, 包含'收盘'价
    :param predictions: numpy.array, 预测值
    :param past_prices: pandas.Series, 过去5个交易日的实际股价
    :param future_predictions: numpy.array, 未来5个交易日的预测股价
    :param future_dates: pandas.DatetimeIndex, 未来5个交易日的日期
    """
    plt.figure(figsize=(14, 7))

    # 绘制实际收盘价
    plt.plot(df.index, df['收盘'], label='实际收盘价', color='blue')

    # 绘制预测收盘价
    pred_series = pd.Series(predictions, index=df.index[:len(predictions)])
    plt.plot(pred_series.index, pred_series, label='预测收盘价', color='red', linestyle='--')

    # 标注过去5个交易日的实际股价
    for date, price in past_prices.items():
        plt.text(date, price, f'{price:.2f}', color='blue', fontsize=9, ha='center')

    # 标注未来5个交易日的预测股价
    for date, price in zip(future_dates, future_predictions):
        plt.text(date, price, f'{price:.2f}', color='red', fontsize=9, ha='center')

    # 设置显示范围
    start_date = past_prices.index[0]
    end_date = future_dates[-1]
    plt.xlim(start_date, end_date)

    plt.title('股价预测 vs 实际股价')
    plt.xlabel('日期')
    plt.ylabel('收盘价')
    plt.legend()
    plt.grid(True)

    # 保存图片到 figure 文件夹
    file_path = "figure/predicted_vs_actual.png"
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    print(f"图表已保存到 {file_path}")

    plt.close()

