import pandas as pd

def add_technical_indicators(df):
    """
    为DataFrame添加技术指标
    :param df: pandas.DataFrame, 包含'收盘'价
    :return: pandas.DataFrame
    """
    # 计算移动平均线
    df['MA5'] = df['收盘'].rolling(window=5).mean()
    df['MA10'] = df['收盘'].rolling(window=10).mean()
    df['MA20'] = df['收盘'].rolling(window=20).mean()

    # 计算MACD
    df['EMA12'] = df['收盘'].ewm(span=12, adjust=False).mean()
    df['EMA26'] = df['收盘'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # 计算RSI
    delta = df['收盘'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    # 避免除以零
    rs = gain / loss
    rs[loss == 0] = 0  # 或者可以设置为一个较大的数，表示强劲的上涨
    df['RSI'] = 100 - (100 / (1 + rs))


    # 计算布林带
    df['BB_Middle'] = df['收盘'].rolling(window=20).mean()
    df['BB_Std'] = df['收盘'].rolling(window=20).std()
    df['BB_Upper'] = df['BB_Middle'] + (df['BB_Std'] * 2)
    df['BB_Lower'] = df['BB_Middle'] - (df['BB_Std'] * 2)
    
    # 计算每日收益率
    df['Return'] = df['收盘'].pct_change()

    df.dropna(inplace=True)
    return df

