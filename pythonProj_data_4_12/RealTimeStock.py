import json, re
import requests
from bs4 import BeautifulSoup


# 获取股票行情信息
# 参数为企业界面的元数据信息，来自于xueqiu_api函数的返回值
# 返回值为一个dict，包含企业股票的各种信息，例如下：
'''
返回值示例
{
    '最高': '12.72',         '今开': '12.64',         '涨停': '13.94',       '成交量': '42.65万手',
    '最低': '12.59',         '昨收': '12.67',         '跌停': '11.40',        '成交额': '5.39亿',
    '量比': '0.94',          '换手': '0.22%',         '市盈率(动)': '5.38',    '市盈率(TTM)': '5.38',
    '委比': '68.61%',        '振幅': '1.03%',         '市盈率(静)': '5.38',    '市净率': '0.67',
    '每股收益': '2.35',       '股息(TTM)': '0.28',      '总股本': '194.06亿',   '总市值': '2449.03亿',
    '每股净资产': '18.80',     '股息率(TTM)': '2.26%',   '流通股': '194.06亿',   '流通值': '2448.98亿',
    '52周最高': '16.37',      '52周最低': '10.22',      '货币单位': 'CNY'
}
'''
def get_stock_content(derive_str):
    input_str = derive_str

    start_str = ",\"tableHtml\":\""
    end_str = "\",\"isMF\""

    start_index = input_str.find(start_str) + len(start_str)
    end_index = input_str.find(end_str)

    if start_index < end_index:

        matched_content = input_str[start_index:end_index].strip()
        string_data = matched_content

        # 解码操作
        soup = BeautifulSoup(string_data, 'lxml')
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

        return res_dict

    else:
        print("No match found.")
        return {}


# 获取企业的信息
# 参数为企业界面的元数据信息，来自于xueqiu_api函数的返回值
# 返回值为一个dict，包含企业的 "简介" "公司网站" "公司地址" "公司电话"
def get_comp_info(derive_str):
    soup = BeautifulSoup(derive_str, 'lxml')
    val_pair = soup.find('div', class_="profile-detail")
    res_dict = {}

    val_contents = list(val_pair.strings)
    res_dict = {}
    res_dict['简介'] = val_contents[0]
    res_dict['公司网站'] = val_contents[2]
    res_dict['公司地址'] = val_contents[4]
    res_dict['公司电话'] = val_contents[6]

    return res_dict


# 参数为股票代码，例如 平安银行为 "SZ000001"，返回值为一个字典


# 参数为股票代码
# 返回值为企业界面的所有原始信息str
# 可通过带入参数，get_stock_content、get_comp_info函数获得更多信息
def xueqiu_api(share_id):
    he = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62"
    }

    # 发送API请求
    url = "https://xueqiu.com/S/" + share_id
    r = requests.get(url, headers=he)
    r_dat = r.text

    return r_dat


# 获取企业相关新闻（1000数据25s）
# 参数1为股票代码str，例如 平安银行为 "SZ000001"；参数2为限制时间戳（int），表示将获取指定日期后的新闻；参数3、4为（int）所需新闻的每页新闻数与总页数
# 参数2的优先级高于参数3、4限制的获取新闻数量
# 返回值为一个list，包含多个dict，每个dict记录了一条新闻的标题、预览图、发布日期、来源、来源链接等信息
def get_comp_news(share_id, first_news_date=0, news_num_perpage=-1, page_num=-1):
    session = requests.Session()

    url = "https://xueqiu.com/statuses/stock_timeline.json?symbol_id=" + share_id + "&count=20&source=%E8%87%AA%E9%80%89%E8%82%A1%E6%96%B0%E9%97%BB&page=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}

    # 第一步,向雪球网首页发送一条请求,获取cookie
    session.get(url="https://xueqiu.com", headers=headers)
    # 第二步,获取动态加载的新闻数据量的统计
    page_json = session.get(url=url, headers=headers).json()
    maxPage = page_json['maxPage']

    # 第三步，获取内容
    news_list = []
    get_news_total_num = 0
    # 便利获取每一面的数据
    for i in range(1, maxPage + 1):
        news_url = "https://xueqiu.com/statuses/stock_timeline.json?symbol_id=" + share_id + "&count=20&source=%E8%87%AA%E9%80%89%E8%82%A1%E6%96%B0%E9%97%BB&page=" + str(
            i)
        # 第一步,获取每一面动态加载的新闻数据
        page_json = session.get(url=news_url, headers=headers).json()

        # 获取信息内容，并更新可能发生变化的maxRage
        nowpage_news_list = page_json['list']
        maxPage = page_json['maxPage']

        # 获取新闻具体信息
        for nownews in nowpage_news_list:
            nownews_dict = {}
            nownews_dict['标题'] = nownews['rawTitle']
            nownews_dict['预览图'] = nownews['firstImg']
            nownews_dict['发布日期'] = nownews['created_at']  # 时间戳
            nownews_dict['来源'] = nownews['quote_cards'][0]['source']
            nownews_dict['来源链接'] = nownews['quote_cards'][0]['target_url']

            nownew_discription = nownews['text']
            end_index = nownew_discription.find('<a href=\"')
            matched_content = nownew_discription[0:end_index].strip()
            nownews_dict['新闻简讯'] = matched_content

            # 将新闻信息推入新闻列表
            news_list.append(nownews_dict)
            get_news_total_num += 1

            # 判断是否达到限制条件
            if int(first_news_date) > int(nownews_dict['发布日期']):
                return news_list
            elif news_num_perpage * page_num <= get_news_total_num:
                return news_list

    # 获取完成，发布新闻
    return news_list


# 获取热度榜
# 参数1代表榜单长度int，测试时间有限，目前可知100以内可行，具体可行性可根据返回值的长度判断
# 参数2代表热度类型int：0、全球 1、沪深 2、港股 3、美股
# 参数3代表榜单时限int：0、一小时内 1、代表24小时内
# 返回值为一个带有多条字典数据的list，其中每一条字典数据dict代表一个排行榜上的股票，排行从高至低
# 可获取排行榜上企业的“公司名”、“股票代码”、“热度”、“热度增量”、“交易所”
def get_popularity_list(list_length=8, popularity_type=0, list_time=0):
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
        tmp_comp_dict = {}
        tmp_comp_dict['公司名'] = comp['name']
        tmp_comp_dict['股票代码'] = comp['code']
        tmp_comp_dict['热度'] = comp['value']
        tmp_comp_dict['热度增量'] = comp['increment']
        tmp_comp_dict['交易所'] = comp['exchange']
        tmp_comp_dict['stock_type'] = comp['stock_type']
        tmp_comp_dict['type'] = comp['type']

        res_popularity_list.append(tmp_comp_dict)

    # 返回数据
    return res_popularity_list


# 获取7×24新闻(500条数据8-10s)
# 参数1表示下一组数据的特殊标识int，（若无需增获信息，可按默认值，否则已获得最后的数据的next_max_id即为下一组数据的特殊标识符）
# 参数2表示获取该时间戳int的日期之后的新闻（优先度高于后者，且会恰好获得），参数3表示获取新闻条数（应当为10的倍数，否则向上取整）
# 返回值为一个包含多条字典数据的列表list，每条字典dict数据代表一条新闻简讯，包含新闻的“内容”、“链接”（雪球）、“日期”等
def get_week_news(next_max_id=0, first_news_date=0, news_total_num=100, former_session=None):
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
        tmp_new_dict['链接'] = tmp_new['target']
        tmp_new_dict['日期'] = tmp_new['created_at']
        tmp_new_dict['id'] = tmp_new['id']
        tmp_new_dict['next_max_id'] = next_max_id

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
            get_week_news(next_max_id=next_max_id, first_news_date=first_news_date,
                          news_total_num=news_total_num, former_session=session))


# derive_html = xueqiu_api("SZ000001")
# print(get_comp_info(derive_html))
# get_comp_news("SZ000001")

# res = get_comp_news("SZ000001", news_num_perpage=5, page_num=10)
# print(res)

# print(get_popularity_list())

res = get_week_news(news_total_num=5)
print(res)