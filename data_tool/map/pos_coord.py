#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: SHF
# @Email: 1316478299@qq.com
# @Date: 2020-09-15 16:06:14

import requests


AK = 'sjuGnGH3aYRZCx8lMphRQfhSys5yhYp2'


def Pos2Coord(name):
    '''
        @func: 通过百度地图API将地理名称转换成经纬度
        @note: 官方文档 http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding
        @output:
            lng: 经度
            lat: 纬度
            conf: 打点绝对精度（即坐标点的误差范围）
            comp: 描述地址理解程度。分值范围0-100，分值越大，服务对地址理解程度越高
            level: 能精确理解的地址类型
    '''
    url = 'http://api.map.baidu.com/geocoding/v3/?address=%s&output=json&ak=%s' % (name, AK)
    res = requests.get(url)
    if res.status_code == 200:
        val = res.json()
        # print(val['status'])
        if val['status'] == 0:
            retVal = {'lng': val['result']['location']['lng'], 'lat': val['result']['location']['lat'],
                      'conf': val['result']['confidence'], 'comp': val['result']['comprehension'],
                      'level': val['result']['level']}
        else:
            retVal = None
        return retVal
    else:
        print('无法获取%s经纬度' % name)


def Coord2Pos(lng, lat, town='true'):
    '''
        @func: 通过百度地图API将经纬度转换成地理名称
        @input:
            lng: 经度
            lat: 纬度
            town: 是否获取乡镇级地理位置信息，默认获取。可选参数（true/false）
        @output:
            address:解析后的地理位置名称
            province:省份名称
            city:城市名
            district:县级行政区划名
            town: 乡镇级行政区划
            adcode: 县级行政区划编码
            town_code: 镇级行政区划编码
    '''
    url = 'http://api.map.baidu.com/reverse_geocoding/v3/?output=json&ak=%s&location=%s,%s&extensions_town=%s' % (
    AK, lat, lng, town)
    res = requests.get(url)
    if res.status_code == 200:
        val = res.json()
        if val['status'] == 0:
            val = val['result']
            retVal = {'address': val['formatted_address'], 'province': val['addressComponent']['province'],
                      'city': val['addressComponent']['city'], 'district': val['addressComponent']['district'],
                      'town': val['addressComponent']['town'], 'adcode': val['addressComponent']['adcode'],
                      'town_code': val['addressComponent']['town_code']}
        else:
            retVal = None
        return retVal
    else:
        print('无法获取(%s,%s)的地理信息！' % (lat, lng))


if __name__ == '__main__':
    # 正地理编码
    val1 = Pos2Coord('上海大学宝山校区')
    # {'lng': 121.39903048091482, 'lat': 31.32144004759091, 'conf': 70, 'comp': 100, 'level': '教育'}
    print(val1)

    # 逆地理编码
    val2 = Coord2Pos(121.399030, 31.321440)
    # {'address': '江苏省南京市江宁区苏源大道', 'province': '江苏省', 'city': '南京市', 'district': '江宁区', 'town': '秣陵街道', 'adcode': '320115', 'town_code': '320115011'}
    print(val2)
