import akshare as ak
import requests

print("AKShare 导入成功！")
print("requests 版本：", requests.__version__)

print("开始获取 A 股数据...")

try:
    stock = ak.stock_zh_a_spot_em()

    print("获取成功！")
    print("数据量：", len(stock))
    print(stock.head())

except Exception as e:
    print("获取失败！")
    print(type(e).__name__)
    print(e)