from StockGetFunc import *
import sys

if __name__ == '__main__':
    # 开始获取进入数据

    # 获取股票列表
    stock_list = readStockList(id_type=1)

    # 开始爬取并保存数据
    saveStockInfo(stock_list=stock_list, get_derive_page_func=xueqiu_api,
                  filter_info_func=filterStockInfo, file_addr="stock_data.csv")