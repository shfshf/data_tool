# -*- coding: utf-8 -*-

#日期识别
import re
from datetime import datetime, timedelta
# from dateutil.parser import parse
import jieba.posseg as psg
import jieba
import pkg_resources
import os


UTIL_CN_NUM = {
    '零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4,
    '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
    '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
}

UTIL_CN_UNIT = {'十': 10, '百': 100, '千': 1000, '万': 10000}


def get_lastweek(day=1):
    d = datetime.now()
    dayscount = timedelta(days=d.isoweekday())
    dayto = d - dayscount
    sixdays = timedelta(days=7 - day)
    dayfrom = dayto - sixdays
    date_from = datetime(dayfrom.year, dayfrom.month, dayfrom.day, 0, 0, 0)
    return str(date_from)[0:4] + '年' + str(date_from)[5:7] + '月' + str(date_from)[8:10] + '日'


def get_nextweek(day=1):
    d = datetime.now()
    dayscount = timedelta(days=d.isoweekday())
    dayto = d - dayscount
    sixdays = timedelta(days=-7 - day)
    dayfrom = dayto - sixdays
    date_from = datetime(dayfrom.year, dayfrom.month, dayfrom.day, 0, 0, 0)
    return str(date_from)[0:4] + '年' + str(date_from)[5:7] + '月' + str(date_from)[8:10] + '日'


def get_week(day=1):
    d = datetime.now()
    dayscount = timedelta(days=d.isoweekday())
    dayto = d - dayscount
    sixdays = timedelta(days=-day)
    dayfrom = dayto - sixdays
    date_from = datetime(dayfrom.year, dayfrom.month, dayfrom.day, 0, 0, 0)
    return str(date_from)[0:4] + '年' + str(date_from)[5:7] + '月' + str(date_from)[8:10] + '日'


def cn2dig(src):
    """
        除了年份之外的其余时间的解析
        :param src: 除了年份的其余时间(从列表的头到倒数第二个字，即假设有"月"这个字，则清洗掉"月")
        :return rsl: 返回相应的除了年份的其余时间的阿拉伯数字
    """
    if src == "":
        # 如果src为空，那么直接返回None，又进行一次清洗
        return None
    m = re.match("\d+", src)
    if m:
        # 如果m是数字则直接返回该数字
        return int(m.group(0))
    rsl = 0
    unit = 1
    for item in src[::-1]:
        # 从后向前遍历src
        if item in UTIL_CN_UNIT.keys():
            # 如果item在UTIL_CN_UTIL中，则unit为这个字转换过来的阿拉伯数字
            # 即假设src为"三十"，那么第一个item为"十"，对应的unit为10
            unit = UTIL_CN_UNIT[item]
        elif item in UTIL_CN_NUM.keys():
            # 如果item不在UTIL_CN_UTIL而在UTIL_CN_NUM中，则转换为相应的阿拉伯数字并且与unit相乘
            # 就假设刚刚那个"三十"，第二个字为"三"，对应的num为3，rsl就为30
            num = UTIL_CN_NUM[item]
            rsl += num * unit
        else:
            # 如果都不在，那么就不是数字，就直接返回None
            return None
    if rsl < unit:
        # 如果出现"十五"这种情况，那么是先执行上面的elif，即rsl = 5，再执行if，即unit = 10，
        # 这时候rsl < unit，那么执行相加操作
        rsl += unit
    return rsl


def year2dig(year):
    """
    解析年份这个维度，主要是将中文或者阿拉伯数字统一转换为阿拉伯数字的年份
    :param year: 传入的年份(从列表的头到倒数第二个字，即假设有"年"这个字，则清洗掉"年")
    :return: 所表达的年份的阿拉伯数字或者None
    """
    res = ''
    for item in year:
        # 循环遍历这个年份的每一个字符
        if item in UTIL_CN_NUM.keys():
            # 如果这个字在UTIL_CN_NUM中，则转换为相应的阿拉伯数字
            res = res + str(UTIL_CN_NUM[item])
        else:
            # 否则直接相加
            # 这里已经是经历了多方面清洗后的结果了，基本到这里不会在item中出现异常的字符
            res = res + item
    m = re.match("\d+", res)
    if m:
        # 当m开头为数字时，执行下面操作，否则返回None
        if len(m.group(0)) == 2:
            # 这里是假设输入的话为"我要住到21年..."之类的，那么year就只有2个字符，即这里m == 21，
            # 那么就通过当前年份除100的整数部分再乘100最后加上这个数字获得最终年份
            # 即int(2020 / 100) * 100 + int("21")
            return int(datetime.today().year/100)*100 + int(m.group(0))
        else:
            # 否则直接返回该年份
            return int(m.group(0))
    else:
        return None


def parse_datetime(msg):
    """
        将每个提取到的文本日期串进行时间转换

        实现方式:
            通过正则表达式将日期串进行切割，分成'年''月''日''时''分''秒'等具体维度，然后针对每个子维度单独再进行识别
        :param msg: 初步清洗后的每一个有关时间的句子
        :return: 如果时间可以通过parse解析，那么返回解析后的时间
                 如果不能够解析，那么返回自行处理后的时间
                 否则返回None
    """
    # 获取年月日时分秒
    tmptime = datetime.today().strftime('%Y{y}%m{m}%d{d}%H{h}%M{m}%S{s}').\
        format(y='年', m='月', d='日', h='时', M='分', s='秒')
    # print('msg:',msg)
    if msg is None or len(msg) == 0:
        # 如果之前清洗失误或者其他原因造成的句子为空，则返回None
        return None

    m = re.match(
        r"([0-9零一二两三四五六七八九十]+年)?([0-9一二两三四五六七八九十]+月)?"
        r"([0-9一二两三四五六七八九十]+[号日])?([上中下午晚早]+)?"
        r"([0-9零一二两三四五六七八九十百]+[点:\.时])?([0-9零一二三四五六七八九十百]+分?)?"
        r"([0-9零一二三四五六七八九十百]+秒)?", msg)
    # print('m.group:',m.group(0),m.group(1),m.group(2),m.group(3),m.group(4),m.group(5))
    if m.group(0) is not None:
        res = {
            "year": m.group(1) if m.group(1) is not None else str(tmptime[0:5]),
            "month": m.group(2) if m.group(2) is not None else str(tmptime[5:8]),
            "day": m.group(3) if m.group(3) is not None else str(tmptime[8:11]),
            "noon": m.group(4),  # 上中下午晚早
            "hour": m.group(5) if m.group(5) is not None else '00',
            "minute": m.group(6) if m.group(6) is not None else '00',
            "second": m.group(7) if m.group(7) is not None else '00',
        }
        # print("匹配",res)
        params = {}
        for name in res:
            if res[name] is not None and len(res[name]) != 0:
                tmp = None
                if name == 'year':
                    # 如果是年份，tmp就进入year2dig
                    tmp = year2dig(res[name][:-1])
                else:
                    # 否则就是其他时间，那么进入cn2dig
                    tmp = cn2dig(res[name][:-1])
                if tmp is not None:
                    # 当tmp之中存在阿拉伯数字的时候，params就为该tmp
                    params[name] = int(tmp)
        # 使用今天的时间格式，然后将数字全部替换为params[]中的内容
        target_date = datetime.today().replace(**params)
        # print('target_date:',target_date)
        is_pm = m.group(4)
        if is_pm is not None:
            # 如果文字中有"中午"、"下午"、"晚上"二字
            if is_pm == u'下午' or is_pm == u'晚上' or is_pm == '中午':
                hour = target_date.time().hour  # 获取刚刚解析的时间的小时
                if hour < 12:
                    # 如果小时小于12，那么替换为24小时制
                    target_date = target_date.replace(hour=hour + 12)
        return target_date.strftime('%Y-%m-%d %H:%M:%S')
        # return target_date.strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}').format(y='年', m='月', d='日', h='时', f='分', s='秒')    # 汉字形式
    else:
        return None


def check_time_valid(word):
    """
        对拼接字符串近一步处理，以进行有效性判断
        :param word: time_res中的每一项(每一项切割出来的时间)
        :return: 清洗后的句子
    """
    # match()匹配成功返回对象，否则返回None，
    # match是全匹配，即从头到尾，而$是匹配最后，从match源码来看，如果str是存在非数字的情况会直接返回None
    # 这里的意思就是清洗掉长度小于等于6的纯数字(小于等于6的意思是指非准确日期，比如2020)
    # print('check:',word)
    m = re.match("\d+$", word)
    if m:
        # 当正则表达式匹配成功时，判断句子的长度是否小于等于6，如果小于等于6，则返回None
        if len(word) <= 6:
            return None
    # 将"号"和"日"替换为"日",个人理解，这里是号和日后面莫名其妙跟了一串数字的情况
    word1 = re.sub('[号|日]\d+$', '日', word)
    # print('word1:',word1)
    if word1 != word:
        # 如果清洗出来的句子与原句子不同，则递归调用
        return check_time_valid(word1)
    else:
        # 如果清洗出来的句子与原句子相同，则返回任意一个句子
        return word1


# 时间提取
def time_extract(text):
    """
        思路:
            通过jieba分词将带有时间信息的词进行切分，记录连续时间信息的词。
            使用了词性标注，提取"m(数字)"和"t(时间)"词性的词。

        规则约束:
            对句子进行解析，提取其中所有能表示日期时间的词，并进行上下文拼接

        :param text: 每一个请求文本
        :return: 解析出来后最终的句子
    """
    time_res = []
    word = ''
    keyDate = {'今天': 0, '明天': 1, '后天': 2, '昨天': -1, '前天': -2}
    timedic = ['时', '分', '到']
    tmptext = []
    path = pkg_resources.resource_filename(    # 包的路径
        __name__, "dict.txt"
    )
    jieba.load_userdict(path)  # 自定义分词词典
    for k, v in psg.cut(text):  # k: 词语, v: 词性
        tmptext.append([k, v])
    for i in range(len(tmptext)):
        k, v = tmptext[i][0], tmptext[i][1]
        if k in keyDate:  # 今天、明天、后天、昨天、前天具体时间提取计算
            # 日期的转换，timedelta提取任意延迟天数的信息
            word = (datetime.today() + timedelta(days=keyDate.get(k, 0))).\
                strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
        elif k == '到':  # 时间段提取
            if word != '':
                time_res.append(word)   # 如果word不为空时, 列表中添加相应的词语
                word = ''
        elif word != '':
            if v in ['m', 't']:
                try:
                    if tmptext[i + 1][0] in timedic:
                        word = word + k + tmptext[i + 1][0]
                    else:
                        word = word + k
                except:  # 当词性为数字或时间时，添加至word中
                    word = word + k
            elif k not in timedic:
                # 当词性不为数字或时间时，将word放入time_res，同时清空word
                time_res.append(word)
                word = ''
        elif v in ['m', 't']:
            # 当k不存在于key_date中，且word为空时，如果词性是数字或时间时，word为该词语
            word = k
    if word != '':
        # word中可能存放的值:
        #   1. 通过词性标注后获得的时间跨度后的时间
        #   2. 非key_date中的时间或数字
        # 即只有k不存在于key_date，word不为空，词性不为数字或时间时，word才为空，进入不了这个if语句
        time_res.append(word)
    tmp_time_res = []
    for i in range(len(time_res)):
        if time_res[i][:2] in ['上周', '下周']:
            if time_res[i][2:3] in UTIL_CN_NUM.keys():
                day = UTIL_CN_NUM[time_res[i][2:3]]
                if time_res[i][:2] == '上周':
                    tmp_time_res.append(get_lastweek(day) + time_res[i][3:])
                else:
                    tmp_time_res.append(get_nextweek(day) + time_res[i][3:])
        elif time_res[i][:1] == '周':
            if time_res[i][1:2] in UTIL_CN_NUM.keys():
                day = UTIL_CN_NUM[time_res[i][1:2]]
                if time_res[i][:1] == '周':
                    tmp_time_res.append(get_week(day) + time_res[i][2:])
        else:
            tmp_time_res.append(time_res[i])
    time_res = tmp_time_res
    try:
        # print("匹配字符串：", time_res)
        # filter() 函数用于过滤序列，过滤掉不符合条件的元素，返回由符合条件元素组成的新列表
        result = list(filter(lambda x: x is not None, [check_time_valid(w) for w in time_res]))
        final_res = [parse_datetime(w) for w in result]
        return [x for x in final_res if x is not None]
    except:
        return None


if __name__ == '__main__':
    ll = ['我要住到明天下午三点', '预定28号的房间', '我要从26号下午4点住到11月2号', '我要预订今天到30号的房间',
          '我要预订到1号到3号的房间', "9月27号上午10点",  "明天下午3点",
          "今天5点", "今天晚上5点", "5点",  "上周一下午5点", "下周二下午5点",
          "周二下午5点",  '前天上午10点', '今天上午11点', "今天下午3点",
          '后天上午11点', '后天下午3点', '前天中午12点',  '今天中午12点',
          '明天中午12点', '后天中午12点', "这周三中午12点",
          '昨天下午3点', '昨天上午11点', '昨天中午12点',
          ]
    l = ["今晚5点", "星期三", "这周三", "这周六", "这周日", "周末", "星期日"]
    for text in l:
        print(text, time_extract(text), sep=': ')
