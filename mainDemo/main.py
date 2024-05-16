import baostock as bs
import pandas as pd
import csv

# 登陆系统
lg = bs.login()

# 显示登陆返回信息
if lg.error_code != 0:
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)


def get_stock_info(stock_id, start_date, end_date):
    #### 获取沪深A股历史K线数据 ####
    # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
    # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
    # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
    rs = bs.query_history_k_data_plus(stock_id,
                                      "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                      start_date=start_date, end_date=end_date,
                                      frequency="d", adjustflag="3")

    if rs.error_msg != "success":
        print('query_history_k_data_plus respond error_code:' + rs.error_code)
        print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    return result


# get_stock_info("sz.300493", '2017-07-01', '2017-12-31')

def save_all_stock_info():
    header = ["datetime", "ts_code", "open", "high", "low", "close", "pre_close", "change", "pct_chg", "vol", "amount"]

    with open('stock_data.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        start_date = "2018-01-01"
        end_date = "2023-04-20"

        # read stock_id_list
        df = pd.read_csv(r"C:/Users/Fm/Desktop/code/Py/pythonProj_data_4_12/stock_id.csv", sep=',', header='infer',
                         encoding="gbk")

        stock_id_list = df['chg_stock_id'].tolist()

        procedure_level = 0.0

        for stock_id in stock_id_list:
            stock_info = get_stock_info(stock_id, start_date, end_date)
            stock_id = stock_id[3:9] + "." + stock_id[0:2].upper()

            # stock_info_list.append(stock_info)
            for i in range(stock_info.shape[0]):
                stock_info_list = [stock_info.at[i, 'date'].replace('-', '/'), stock_id, stock_info.at[i, 'open'],
                                   stock_info.at[i, 'high'],
                                   stock_info.at[i, 'low'], stock_info.at[i, 'close'], stock_info.at[i, 'preclose'],
                                   float(stock_info.at[i, 'close']) - float(stock_info.at[i, 'preclose']),
                                   stock_info.at[i, 'pctChg'],
                                   stock_info.at[i, 'volume'], stock_info.at[i, 'amount']]

                if stock_info.at[i, 'volume'] == '' or stock_info.at[i, 'amount'] == '' or \
                        float(stock_info.at[i, 'volume']) == 0.0 or float(stock_info.at[i, 'amount']) == 0.0:
                    continue
                else:
                    writer.writerow(stock_info_list)

            procedure_level += 1.0
            print(f'process: {100.0 * (procedure_level / float(len(stock_id_list)))}%\tStock Saved: {stock_id}')

    #     result = pd.DataFrame(stock_info_list, columns=100)
    #
    # #### 结果集输出到csv文件 ####
    # result.to_csv("C:/Users/Fm/Desktop/code/Py/pythonProj_data_4_12/result.csv", index=False)
    # print(result.columns)
    # print(result.info)


save_all_stock_info()

# 登出系统
bs.logout()

# 读取csv文件并按datetime列升序排列
df = pd.read_csv('stock_data.csv')
df = df.sort_values(['datetime', 'ts_code'], ascending=[True, True])

# 将排序后的数据写回到csv文件中
df.to_csv('stock_data.csv', index=False)
