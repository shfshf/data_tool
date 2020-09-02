'''
查询两站之间的火车票信息

输入参数： <date> <from> <to>

12306 api:
'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2020-09-21&leftTicketDTO.from_station=NJH&leftTicketDTO.to_station=SZH&purpose_codes=ADULT'

'''
import requests
import re
import json


# 获取12306城市名和城市代码数据
def get_station():
    # 关闭https证书验证警告
    requests.packages.urllib3.disable_warnings()

    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9142'
    r = requests.get(url, verify=False)
    pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
    result = re.findall(pattern, r.text)
    station = dict(result)
    return station


# 城市名代码查询字典
# key：城市名 value：城市代码
stations_dict = get_station()
# 反转k，v形成新的字典
code_dict = {v: k for k, v in stations_dict.items()}


def query_train_info(url):
    '''
    查询火车票信息：
    返回 信息查询列表
    '''

    info_list = []
    try:

        # 获取返回的json数据里的data字段的result结果
        raw_trains = url.json()['data']['result']

        for raw_train in raw_trains:
            # 循环遍历每辆列车的信息
            data_list = raw_train.split('|')

            # 车次号码
            train_no = data_list[3]
            # 出发站
            from_station_code = data_list[6]
            from_station_name = code_dict[from_station_code]
            # 终点站
            to_station_code = data_list[7]
            to_station_name = code_dict[to_station_code]
            # 出发时间
            start_time = data_list[8]
            # 到达时间
            arrive_time = data_list[9]
            # 总耗时
            time_fucked_up = data_list[10]
            # 一等座
            first_class_seat = data_list[31] or '--'
            # 二等座
            second_class_seat = data_list[30]or '--'
            # 软卧
            soft_sleep = data_list[23]or '--'
            # 硬卧
            hard_sleep = data_list[28]or '--'
            # 硬座
            hard_seat = data_list[29]or '--'
            # 无座
            no_seat = data_list[26]or '--'

            # 打印查询结果
            info = ('车次:{}，出发站:{}，目的地:{}，出发时间:{}，到达时间:{}，消耗时间{}小时,\n座位情况： 一等座：「{}」 \t二等座：「{}」\t软卧：「{}」\t硬卧：「{}」\t硬座：「{}」\t无座：「{}」'.format(
                train_no, from_station_name, to_station_name, start_time, arrive_time, time_fucked_up, first_class_seat,
                second_class_seat, soft_sleep, hard_sleep, hard_seat, no_seat))

            info_list.append(info)

        return info_list
    except:
        return ' 输出信息有误，请重新输入'


def query_url(date, from_station, to_station):
    # api url 构造
    # 基于 mac 系统 cookie 有效
    url = (
        'https://kyfw.12306.cn/otn/leftTicket/query?'
        'leftTicketDTO.train_date={}&'
        'leftTicketDTO.from_station={}&'
        'leftTicketDTO.to_station={}&'
        'purpose_codes=ADULT'
    ).format(date, stations_dict[from_station], stations_dict[to_station])
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'Cookie': '_uab_collina=159885825689025795678935; JSESSIONID=A238DA197465C7903808F983656FEB74; route=6f50b51faa11b987e576cdb301e545c4; BIGipServerpool_passport=233636362.50215.0000; RAIL_EXPIRATION=1599153754431; RAIL_DEVICEID=dLy55zK-ebBmfVMHwTObsJzOcrN0RynsdloGOkOt--aLkrIjpADFB5flrAYQ_MTUTFFv1pksVKJKQExuocoQj2HLTX41MKuMitV3iqi5XTF_wK0fVLAs6-L83f4plVJ2EJ4uAk4sIVEN1CkcvD3qgWodu6neFIVh; _jc_save_fromStation=%u4E0A%u6D77%2CSHH; _jc_save_toStation=%u5317%u4EAC%2CBJP; _jc_save_toDate=2020-08-31; _jc_save_wfdc_flag=dc; _jc_save_fromDate=2020-09-01; BIGipServerotn=1257243146.64545.0000'}
    resp = requests.get(url, headers=headers)  # 请求的结果为响应
    # 设置响应的编码格式，不然会发生乱码
    resp.encoding = 'utf-8'
    # print(resp.text)
    info_list = query_train_info(resp)
    return info_list


if __name__ == '__main__':

    date = '2020-09-19'
    from_station = '北京'
    to_station = '上海'
    info_list = query_url(date, from_station, to_station)
    for info in info_list:
        print(info, '\n', '=' * len(info))

