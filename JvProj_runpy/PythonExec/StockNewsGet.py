from StockGetFunc import *
import sys

if __name__ == '__main__':
    news_get_len = 100

    # 开始获取进入数据
    if len(sys.argv) > 1:
        news_get_len = int(sys.argv[1])
    # 开始爬取并保存数据
    saveWeekNews(news_total_num=news_get_len)