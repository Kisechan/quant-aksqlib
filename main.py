from src.data_loader import get_daily_stock
from src.features import add_technical_indicators
from src.model import train_model, predict
from src.backtest import plot_results
import pandas as pd

def main():
    # 获取数据
    symbol = "000001" # 平安银行
    try:
        df = get_daily_stock(symbol=symbol, start_date="20220101", end_date="20250923")
        print(f"成功获取 {symbol} 的数据，共 {len(df)} 条记录。")
    except ValueError as e:
        print(e)
        return

    # 特征工程
    df = add_technical_indicators(df)
    print("技术指标计算完成。")

    # 定义用于模型的特征
    features = ['MA5', 'MA10', 'MA20', 'MACD', 'Signal_Line', 'RSI', 'BB_Upper', 'BB_Lower']
    
    # 确保在模型训练前，数据是干净的
    df_model = df.copy()
    df_model.dropna(subset=features, inplace=True)

    # 训练模型
    temp_df_for_training = df_model.copy()
    model = train_model(temp_df_for_training, features)
    print("模型训练完成。")

    # 进行预测
    predict_df = df_model.iloc[:-1]
    predictions = predict(model, predict_df, features)
    print("股价预测完成。")

    # 输出过去五日和未来五日的报价
    past_prices = df_model['收盘'].iloc[-5:]
    future_predictions = predictions[-5:]
    print("过去5个交易日的实际股价：")
    for date, price in zip(past_prices.index, past_prices):
        print(f"{date.date()}: {price:.2f}")

    print("未来5个交易日的预测股价：")
    future_dates = pd.date_range(start=past_prices.index[-1] + pd.Timedelta(days=1), periods=5, freq='B')
    for date, price in zip(future_dates, future_predictions):
        print(f"{date.date()}: {price:.2f}")

    # 结果可视化
    plot_df = predict_df.copy()
    plot_df['Predictions'] = predictions
    plot_results(plot_df, plot_df['Predictions'], past_prices, future_predictions, future_dates)


if __name__ == "__main__":
    main()

