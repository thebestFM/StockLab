import csv, requests, json, re
from bs4 import BeautifulSoup
import baostock as bs
import pandas as pd
import numpy as np
import os, sys, io

# 读取stock_id文件
def readStockList(stock_id_file_addr = "PythonExec/stock_id.csv", id_type=1):
    print(f"\"readStockList\":stock_id file reader starts.")
    with open(stock_id_file_addr, 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        stock_list = []
        # 开始读取数据
        for row in spamreader:
            if row[id_type]=='stock_id' or row[id_type]=='chg_stock_id':
                continue
            stock_list.append(row[id_type])

        # 返回一个股票编号表
        print(f"\"readStockList\":stock_id file reader successes.")
        return stock_list



# 爬取页面内容
def xueqiu_api(share_id):
    he = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62"
    }
#     sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

    # 发送API请求
    url = "https://xueqiu.com/S/" + share_id
    r = requests.get(url=url, headers=he)
    r.encoding = "utf8"
    r_dat = r.text

    return r_dat

# 爬取页面内容
def xueqiu_api1(share_id):
    he = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62"
    }
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

    # 发送API请求
    url = "https://xueqiu.com/S/" + share_id
    r = requests.get(url=url, headers=he)
    r.encoding = "utf8"
    r_dat = r.text

    return r_dat

# 提取股票信息
def filterStockInfo(derive_page):
    input_str = derive_page

    start_str = ",\"tableHtml\":\""
    end_str = "\",\"isMF\""

    start_index = input_str.find(start_str) + len(start_str)
    end_index = input_str.find(end_str)

    if start_index < end_index:
        matched_content = input_str[start_index:end_index].strip()
        string_data = matched_content

        # 解码操作
        soup = BeautifulSoup(string_data, 'html.parser')
        val_pairs = soup.find_all('td')

        # 将读取到的数据存入字典
        res_dict = {}
        for val_pair in val_pairs:
            val_pair_content = list(val_pair.strings)

            val_pair_key = val_pair_content[0].replace('：', '')

            # 判断参数项是否为空
            if len(val_pair_content) >= 2:
                res_dict[val_pair_key] = val_pair_content[1]
            else:
                res_dict[val_pair_key] = ""

        res_dict0 = dict({})
        for res_dict_key in res_dict.keys():
            if res_dict[res_dict_key] == '--':
                res_dict[res_dict_key] = ''
        res_dict0['今开'] = res_dict['今开']
        res_dict0['昨收'] = res_dict['昨收']
        res_dict0['最高'] = res_dict['最高']
        res_dict0['最低'] = res_dict['最低']
        res_dict0['成交量'] = res_dict['成交量']
        res_dict0['成交额'] = res_dict['成交额']
        res_dict0['换手率'] = res_dict['换手']
        res_dict0['市盈(TTM)'] = res_dict['市盈率(TTM)']
        res_dict0['市盈率'] = res_dict['市盈率(动)']
        res_dict0['流通值'] = res_dict['流通值']
        res_dict0['流通股'] = res_dict['流通股']
        res_dict0['总市值'] = res_dict['总市值']
        res_dict0['总股本'] = res_dict['总股本']
        res_dict0['52周高'] = res_dict['52周最高']
        res_dict0['52周低'] = res_dict['52周最低']
        return res_dict0
    else: return dict({})

# 获取公司信息
def filterStockEnterprise(derive_page):
    res_dict = {}
    soup = BeautifulSoup(derive_page, 'html.parser')

    val_pair = soup.find('div', class_="stock-name")
    val_contents = list(val_pair.strings)
    val_contents = val_contents[0].split('(')
    res_dict['公司'] = val_contents[0]

    val_pair = soup.find('div', class_="profile-detail")
    val_contents = list(val_pair.strings)
    res_dict['简介'] = val_contents[0]
    if len(val_contents) > 2:
        res_dict['公司网站'] = val_contents[2]
    if len(val_contents) > 4:
        res_dict['公司地址'] = val_contents[4]
    if len(val_contents) > 6:
        res_dict['公司电话'] = val_contents[6]

    return res_dict

# 保存信息
def saveStockInfo(stock_list, get_derive_page_func, filter_info_func, file_addr):
    listToSave = []

    # 计数器
    counter = 0
    print("\"saveStockInfo\":Stock info getting starts.")

    for stock_id in stock_list:
        counter += 1
        print(f"process:{counter}/{len(stock_list)}")

        derive_page = get_derive_page_func(stock_id)
        tmp_stock_info = filter_info_func(derive_page)

        tmp_stock_info1 = {'股票代码': stock_id}
        tmp_stock_info1.update(tmp_stock_info)
        listToSave.append(tmp_stock_info1)

    print("\"saveStockInfo\":Stock info getting successes.")

    # 开始写入数据
    print("\"saveStockInfo\":Stock info saving starts.")
    with open(file_addr, 'w', newline='', encoding="utf8") as csvfile:
        if len(listToSave) == 0:
            return False

        # 获取文件头key
        file_header = listToSave[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=file_header)

        # 写入字段名，当做表头
        writer.writeheader()
        counter = 0
        # 多行写入
        for oneof_listToSave in listToSave:
            counter += 1
            print(f"process:{counter}/{len(listToSave)}")
            writer.writerow(oneof_listToSave)

        print("\"saveStockInfo\":Stock info saving successes.")
    # 写入完毕
    return True

# datafrmae处理函数
'''
    Dataframe数值转为二维列表
    is_del_duplicates用来判断是否删除dataframe中重复的行（重复行中只保留第一次出现的）
    具体可以根据自己的需要修改 drop_duplicates()中的参数
'''
def dataframe_to_list(df, is_del_duplicates):
    if not is_del_duplicates:  # 不删除的情况
        # 返回值是一个二维列表
        return df.values.tolist()
    else:  # 删除重复行的情况
        return df.drop_duplicates().values.tolist()

# 获取股票企业新闻 news_number为20的倍数
def saveStockNews(stock_list, news_number=20, file_addr='stock_news_about.csv'):
    counter = 0
    print("\"saveStockNews\":Stock news getting starts.")

    # 初始化返回数组
    news_list = []
    session = requests.Session()
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}


    # 第一步,向雪球网首页发送一条请求,获取cookie
    session.get(url="https://xueqiu.com", headers=headers)

    # 获取新闻作业
    for stock_id in stock_list:
        counter += 1
        print(f"process:{counter}/{len(stock_list)}")

        url = "https://xueqiu.com/statuses/stock_timeline.json?symbol_id=" + stock_id + "&count=20&source=%E8%87%AA%E9%80%89%E8%82%A1%E6%96%B0%E9%97%BB&page=1"

        # 第二步,获取动态加载的新闻数据量的统计
        page_json = {}
        while True:
            try:
                page_session = session.get(url=url, headers=headers)
                page_json = page_session.json()

                if 'maxPage' in page_json:
                    break
                else: session.get(url="https://xueqiu.com", headers=headers)
            except BaseException as e:
                print(f'\nInvalid JSON\nPage:{page_session}\nURL:{url}')
                session.get(url="https://xueqiu.com", headers=headers)
                continue
        
        maxPage = page_json['maxPage']
        # print(f'stock_id:{stock_id}\nmaxPage:{maxPage}')

        # 第三步，获取内容
        get_news_total_num = 0
        # 便利获取每一面的数据
        for i in range(1, maxPage + 1):
            # 判断是否超过时间
            if news_number <= get_news_total_num:
                break
            
            news_url = "https://xueqiu.com/statuses/stock_timeline.json?symbol_id=" + stock_id + "&count=20&source=%E8%87%AA%E9%80%89%E8%82%A1%E6%96%B0%E9%97%BB&page=" + str(
                i)
            # 第一步,获取每一面动态加载的新闻数据
            page_json = {}
            while True:
                try:
                    page_session = session.get(url=news_url, headers=headers)
                    page_json = page_session.json()

                    if 'list' in page_json:
                        break
                    else: session.get(url="https://xueqiu.com", headers=headers)
                except BaseException as e:
                    print(f'\nInvalid JSON\nPage:{page_session}\nURL:{news_url}')
                    session.get(url="https://xueqiu.com", headers=headers)
                    continue
            # print(page_json)

            # 获取信息内容，并更新可能发生变化的maxRage
            nowpage_news_list = page_json['list']
            # print(f'stock_id:{stock_id}\nnowpage_news_list{nowpage_news_list}')
            maxPage = page_json['maxPage']

            # 获取新闻具体信息
            for nownews in nowpage_news_list:
                nownews_dict = {}
                nownews_dict['股票代码'] = stock_id
                nownews_dict['标题'] = nownews['rawTitle']
                nownews_dict['预览图'] = nownews['firstImg']
                nownews_dict['发布日期'] = nownews['created_at']  # 时间戳
                if nownews['quote_cards'] == None:
                    nownews_dict['来源'] = '雪球新闻'
                    nownews_dict['来源链接'] = "https://xueqiu.com"+ nownews['target']
                else:
                    nownews_dict['来源'] = nownews['quote_cards'][0]['source']
                    nownews_dict['来源链接'] = nownews['quote_cards'][0]['target_url']

                nownew_discription = nownews['text']
                end_index = nownew_discription.find('<a href=\"')
                matched_content = nownew_discription[0:end_index].strip()
                nownews_dict['新闻简讯'] = matched_content

                # 将新闻信息推入新闻列表
                news_list.append(nownews_dict)
                get_news_total_num += 1

    
    print("\"saveStockNews\":Stock news getting successes.")

    # 保存数据
    # print("正在保存文件!");
    # 开始写入数据
    with open(file_addr, 'w', newline='', encoding="utf8") as csvfile:
        print("\"saveStockNews\":Stock info saving starts.")

        if len(news_list) == 0:
            print(f"No stock news got!\nlen={len(news_list)}")
            return False

        # 获取文件头key
        file_header = news_list[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=file_header)

        # 写入字段名，当做表头
        writer.writeheader()
        counter = 0
        # 多行写入
        for stock_one_news in news_list:
            counter += 1
            print(f"process:{counter}/{len(news_list)}")
            writer.writerow(stock_one_news)

        print("\"saveStockNews\":Stock info saving successes.")
        return True

# 保存股票价格
def saveStockPrice(stock_list, date_start, date_end, file_addr='stock_price.csv'):

    stock_price_list = []
    counter = 0

    print("\"saveStockPrice\":Stock price getting starts.")
    # 遍历查询信息
    for stock_id in stock_list:
        counter += 1
        print(f"process:{counter}/{len(stock_list)}")

        # 登陆系统
        sys.stdout = open(os.devnull, 'w')
        # 登陆系统
        lg = bs.login()
        # 打开print的输出
        sys.stdout = sys.__stdout__
        # 显示登陆返回信息
        if lg.error_code != '0':
            print('login respond error_code:' + lg.error_code)
            print('login respond error_msg:' + lg.error_msg)
            return False
        rs = bs.query_history_k_data_plus(stock_id,
                                          "code,date,open,close,high,low,volume",
                                          start_date=date_start, end_date=date_end,
                                          frequency="d", adjustflag="3")

        # 判断是否出现问题
        if rs.error_code != '0':
            print('query_history_k_data_plus respond error_code:' + rs.error_code)
            print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)
            continue
        else:
            # 转换为结果集
            data_list = []
            while (rs.error_code == '0') & rs.next():
                # 获取一条记录，将记录合并在一起
                data_list.append(rs.get_row_data())
            result = pd.DataFrame(data_list, columns=rs.fields)

            # 开始将dataframe转为dict list
            stock_price_dict_keys = result.columns.tolist()
            res_list = dataframe_to_list(result, False)
            for stock_info in res_list:
                stock_info_dict = {}
                for i in range(len(stock_price_dict_keys)):
                    if i == 0:
                        stock_info_dict['code'] = stock_id[0:2].upper()+stock_id[3:9]
                    elif i == 1:
                        stock_info_dict[stock_price_dict_keys[i]] = stock_info[i].replace('-', '/')
                    else:
                        stock_info_dict[stock_price_dict_keys[i]] = stock_info[i]
                stock_price_list.append(stock_info_dict)

    stock_price_list = sorted(stock_price_list, key=lambda x: x["date"], reverse=False)
    print("\"saveStockPrice\":Stock price getting ends.")

    # 登陆系统
    sys.stdout = open(os.devnull, 'w')
    # 登出系统
    bs.logout()
    # 打开print的输出
    sys.stdout = sys.__stdout__

    # 存进文件中stock_price_list
    # 开始写入数据
    with open(file_addr, 'w', newline='', encoding="utf8") as csvfile:
        print("\"saveStockPrice\":Stock price saving starts.")
        if len(stock_price_list) == 0:
            return False

        # 获取文件头key
        file_header = stock_price_list[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=file_header)

        # 写入字段名，当做表头
        writer.writeheader()

        last_stock_id = "none"
        last_data_date = "none"
        counter = 0
        # 多行写入
        for stock_price_item in stock_price_list:
            counter += 1
            print(f"process:{counter}/{len(stock_price_list)}")

            if last_stock_id == stock_price_item['code'] and last_data_date == stock_price_item['date']:
                continue
            else:
                writer.writerow(stock_price_item)
                last_stock_id = stock_price_item['code']
                last_data_date = stock_price_item['date']

        print("\"saveStockPrice\":Stock price saving successes.")
    return True

# 获取热度榜
# 参数1代表榜单长度int，测试时间有限，目前可知100以内可行，具体可行性可根据返回值的长度判断
# 参数2代表热度类型int：0、全球 1、沪深 2、港股 3、美股
# 参数3代表榜单时限int：0、一小时内 1、代表24小时内
# 返回值为一个带有多条字典数据的list，其中每一条字典数据dict代表一个排行榜上的股票，排行从高至低
# 可获取排行榜上企业的“公司名”、“股票代码”、“热度”、“热度增量”、“交易所”
def saveHeatList(list_length=100, popularity_type=0, list_time=0, file_addr='stock_heat.csv'):
    print("\"saveHeatList\":Stock heat getting starts.")
    counter = 0
    session = requests.Session()

    # 转换获url
    popularity_type_translator = [10, 12, 13, 11]
    list_time_translator = [[10, 10], [12, 22], [13, 23], [11, 21]]
    url = "https://stock.xueqiu.com/v5/stock/hot_stock/list.json?size=" + str(list_length) + \
          "&_type=" + str(popularity_type_translator[popularity_type]) + \
          "&type=" + str(list_time_translator[popularity_type][list_time])
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}

    # 第一步,向雪球网首页发送一条请求,获取cookie
    session.get(url="https://xueqiu.com", headers=headers)
    # 第二步,获取动态加载的新闻数据量的统计
    page_json = session.get(url=url, headers=headers).json()
    # 第三步,记录详细信息
    tmp_comp_list = page_json['data']['items']
    res_popularity_list = []
    for comp in tmp_comp_list:
        counter += 1
        print(f"process:{counter}/{len(tmp_comp_list)}")
        
        tmp_comp_dict = {}
        tmp_comp_dict['公司名'] = comp['name']
        tmp_comp_dict['股票代码'] = comp['code']
        tmp_comp_dict['交易所'] = comp['exchange']
        tmp_comp_dict['热度'] = comp['value']
        tmp_comp_dict['热度变化量'] = comp['increment']

        res_popularity_list.append(tmp_comp_dict)

    print("\"saveHeatList\":Stock heat getting successes.")

    # 保存数据数据
    # 开始写入数据
    with open(file_addr, 'w', newline='', encoding="utf8") as csvfile:
        print("\"saveHeatList\":Stock heat saving starts.")

        if len(res_popularity_list) == 0:
            return False

        # 获取文件头key
        file_header = res_popularity_list[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=file_header)

        # 写入字段名，当做表头
        writer.writeheader()
        # 多行写入
        writer.writerows(res_popularity_list)
        # print("文件写入完毕!")

    print("\"saveHeatList\":Stock heat saving successes.")
    return True


# 获取7*24新闻
def getWeekNews(next_max_id=0, first_news_date=0, news_total_num=100, former_session=None):
    session = former_session
    if former_session == None:
        session = requests.Session()

    # 转换获url
    url = "https://xueqiu.com/statuses/livenews/list.json?since_id=-1&count=15"
    if next_max_id != "" and next_max_id != 0 and next_max_id != None:
        url += ("&max_id=" + str(next_max_id))

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}

    if former_session == None:
        # 第一步,向雪球网首页发送一条请求,获取cookie
        session.get(url="https://xueqiu.com", headers=headers)
    else: session = former_session
    # 第二步,获取动态加载的新闻数据量的统计
    page_json = session.get(url=url, headers=headers).json()

    # 更新下一组数据id
    next_max_id = page_json['next_max_id']
    # 保存一组数据,检查数据是否异常
    if not 'items' in page_json or len(page_json['items']) == 0:
        return
    tmp_new_list = page_json['items']
    res_new_list = []

    # 得到数据的全部信息
    for tmp_new in tmp_new_list:
        tmp_new_dict = {}
        tmp_new_dict['内容'] = tmp_new['text']
        tmp_new_dict['日期'] = tmp_new['created_at']
        tmp_new_dict['链接'] = tmp_new['target']
        # tmp_new_dict['id'] = tmp_new['id']
        # tmp_new_dict['next_max_id'] = next_max_id

        # 判断退出 or 保存数据
        if tmp_new_dict['日期'] <= first_news_date:
            return res_new_list
        else:
            res_new_list.append(tmp_new_dict)

    # 判断是否达到数量限制
    news_total_num -= len(tmp_new_list)
    if news_total_num <= 0:
        return res_new_list
    return (res_new_list +
            getWeekNews(next_max_id=next_max_id, first_news_date=first_news_date,
                          news_total_num=news_total_num, former_session=session))

# 保存7*24新闻
def saveWeekNews(news_total_num=100, file_addr='stock_news.csv'):
    print("\"saveWeekNews\":Stock week news getting starts.")
    # 获取新闻
    week_news_list = getWeekNews(news_total_num=news_total_num)

    print("\"saveWeekNews\":Stock week news getting successes.")

    # 保存新闻
    print("\"saveWeekNews\":Stock week news saving starts.")
    # 开始写入数据
    with open(file_addr, 'w', newline='', encoding="utf8") as csvfile:
        if week_news_list==None or len(week_news_list) == 0:
            print("\"saveWeekNews\":No stock week news saved.")
            return False

        # 获取文件头key
        file_header = week_news_list[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=file_header)

        # 写入字段名，当做表头
        writer.writeheader()
        # 多行写入
        writer.writerows(week_news_list)
        print("\"saveWeekNews\":Stock week news saving successes.")
    return True

# 获取股票的简略信息
# 参数为企业界面的元数据信息，来自于xueqiu_api函数的返回值
# 返回值为一个dict，包含股票的 "当前值" "变化量" "变化百分比"
def get_stock_short_info(stock_id):
    print("start")
    derive_str = xueqiu_api1(stock_id)

#     print("\"get_stock_short_info\":start")
    soup = BeautifulSoup(derive_str, 'lxml')

    res_dict = {}
    tmp_val_container = soup.find('div', class_="stock-current")

    res_dict['当前值'] = tmp_val_container.text
    tmp_val_container = soup.find('div', class_="stock-change")
    tmp_vals = tmp_val_container.text.split(' ')
    res_dict['变化量'] = tmp_vals[0]
    res_dict['变化百分比'] = tmp_vals[-1]

    print(f"{res_dict['当前值']},{res_dict['变化量']},{res_dict['变化百分比']}")

    return res_dict

# stock_list = readStockList(id_type=2)
# saveStockInfo(stock_list=stock_list, get_derive_page_func=xueqiu_api,
#               filter_info_func=filterStockInfo, file_addr="stock_data.csv")
# saveStockInfo(stock_list=stock_list, get_derive_page_func=xueqiu_api, filter_info_func=filterStockEnterprise, file_addr="stock_enterprise.csv")
# saveStockPrice(stock_list=stock_list, date_start='2022-4-23', date_end='2023-04-22')
# saveStockNews(stock_list=stock_list)
# saveHeatList(list_length=100)
