import akshare as ak

stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
file_path = "data/stock_list.csv"
stock_zh_a_spot_em_df.to_csv(file_path, encoding="utf-8-sig")