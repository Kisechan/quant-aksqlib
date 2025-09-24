from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd

def train_model(df, features):
    """
    训练线性回归模型
    :param df: pandas.DataFrame, 包含特征和目标值
    :param features: list, 特征列名
    :return: trained model
    """
    # 将第二天的收盘价作为目标
    df['Target'] = df['收盘'].shift(-1)
    df.dropna(inplace=True)

    X = df[features]
    y = df['Target']

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = LinearRegression()
    model.fit(X_train, y_train)

    # 评估模型
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"模型均方误差 (MSE): {mse}")

    return model

def predict(model, df, features):
    """
    使用训练好的模型进行预测
    :param model: trained model
    :param df: pandas.DataFrame, 需要预测的数据
    :param features: list, 特征列名
    :return: numpy.array, 预测值
    """
    return model.predict(df[features])

