from StockGetFunc import *
import sys

if __name__ == '__main__':
    # 开始获取进入数据

    # 获取股票列表
    stock_list = readStockList(id_type=2)

    # 开始爬取并保存数据
    saveStockPrice(stock_list=stock_list, date_start=sys.argv[1], date_end=sys.argv[2])