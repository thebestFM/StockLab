import requests, json, re, csv

session = requests.Session()
stocks = []
# 第一步,向雪球网首页发送一条请求,获取cookie
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
session.get(url="https://www.xueqiu.com/", headers=headers)

for page_num in range(1, 169):

    # 转换获url
    url = "https://stock.xueqiu.com/v5/stock/screener/quote/list.json?page=" + str(page_num) + "&size=30&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz"

    # 第二步,获取动态加载的新闻数据量的统计
    print(f"爬取进度:{page_num}")
    page_json = session.get(url=url, headers=headers).json()
    # 第三步,记录详细信息
    if not ('list' in page_json['data']):
        break
    stock_derive_list = page_json['data']['list']
    for stock_derive in stock_derive_list:
        stock_dict = {}
        stock_dict['comp_name'] = stock_derive['name']
        stock_dict['stock_id'] = stock_derive['symbol']
        stocks.append(stock_dict)

with open('stock_id.csv', 'w', encoding='gbk', newline='') as f:
    writer = csv.writer(f)
    header = ['comp_name', 'stock_id', 'chg_stock_id']
    writer.writerow(header)

    for i in stocks:
        if i['stock_id'][0:2] == 'SH':
            chg_stock_id = 'sh.' + i['stock_id'][2:8]
        elif i['stock_id'][0:2] == 'SZ':
            chg_stock_id = 'sz.' + i['stock_id'][2:8]
        data = [i['comp_name'], i['stock_id'], chg_stock_id]

        # write the data
        writer.writerow(data)