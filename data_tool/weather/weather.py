import os
import datetime

import requests
import json
from requests import ConnectionError, HTTPError, TooManyRedirects, Timeout
from data_tool.rule_date.date_parser import time_extract
# from normalization import text_to_date


KEY = os.getenv("SENIVERSE_KEY", "")  # API key  ("SqaphYs862YmgEz3U")
API = "https://api.seniverse.com/v3/weather/daily.json"  # API URL
UNIT = "c"  # 温度单位
LANGUAGE = "zh-Hans"  # 查询结果的返回语言


one_day_timedelta = datetime.timedelta(days=1)


def fetch_weather(location: str, start=0, days=15) -> dict:
    result = requests.get(
        API,
        params={
            "key": KEY,
            "location": location,
            "language": LANGUAGE,
            "unit": UNIT,
            "start": start,
            "days": days,
        },
        timeout=2,
    )
    return result.json()

# use normalization
# def get_weather_by_date(location: str, date: datetime.date) -> dict:
#     day_timedelta = date - datetime.datetime.today().date()
#     day = day_timedelta // one_day_timedelta
#
#     return get_weather_by_day(location, day)


def get_weather_by_date(location: str, date: datetime.date) -> dict:
    day_timedelta = date - datetime.datetime.today().date()
    day = day_timedelta // one_day_timedelta
    # print(day)
    return get_weather_by_day(location, day)


def get_weather_by_day(location: str, day=1) -> dict:
    result = fetch_weather(location)
    # print(result)
    normal_result = {
        "location": result["results"][0]["location"],
        "result": result["results"][0]["daily"][day],
    }

    return normal_result


def get_text_weather_date(address: str, date_time, raw_date_time: str) -> str:
    try:
        result = get_weather_by_date(address, date_time)
    except (ConnectionError, HTTPError, TooManyRedirects, Timeout) as e:
        text_message = "{}".format(e)
    else:
        text_message_tpl = "{} {} ({}) 的天气 情况为：白天：{}；夜晚：{}；气温：{}-{} 度"
        text_message = text_message_tpl.format(
            result["location"]["name"],
            raw_date_time,
            result["result"]["date"],
            result["result"]["text_day"],
            result["result"]["text_night"],
            result["result"]["high"],
            result["result"]["low"],
        )

    return text_message


if __name__ == "__main__":
    # simple test cases

    default_location = "上海"
    result = fetch_weather(default_location)
    print(json.dumps(result, ensure_ascii=False))

    default_location = "北京"
    result = get_weather_by_day(default_location)
    print(json.dumps(result, ensure_ascii=False))

    # 提取时间
    time_ex = time_extract("明天下午")
    time = "".join(time_ex).split(" ")[0]
    # time type str to datetime.date
    time_date_type = datetime.datetime.strptime(time, '%Y-%m-%d')  # str to datetime.datetime
    time_date = datetime.datetime.date(time_date_type)  # str to datetime.datetime to datetime.date
    print(time_date)
    # time_date = text_to_date("明天")
    weather_data = get_text_weather_date("上海", time_date, "sb")

    print(weather_data)
