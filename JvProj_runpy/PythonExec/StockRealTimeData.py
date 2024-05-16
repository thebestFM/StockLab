from StockGetFunc import *
import sys

if __name__ == '__main__':
    # 开始获取进入数据

    # 开始爬取并保存数据
    get_stock_short_info(sys.argv[1])