import requests
import json
import re


class Round_plan():
    """一个关于调用百度地图API全方式路径规划功能的类"""
    def __init__(self, transit_mode):
        self.transit_mode = transit_mode

    def stod(self, slat, slng, dlat, dlng, waypoints='', route_type=''):  # 输入：起点纬度、起点经度、终点纬度、终点经度
        self.slat=slat
        self.slng=slng
        self.dlat=dlat
        self.dlng=dlng
        self.waypoints=waypoints  # 途经点
        self.route_type=route_type  # 路线类型名
        if self.transit_mode == 'Car':
            a = "driving"
        elif self.transit_mode == 'Public transit':
            a = "transit"
        elif self.transit_mode == "E-bike":
            a = "riding"
        elif self.transit_mode == "Bike":
            a = "riding"
        elif self.transit_mode == "Walk":
            a = "walking"
        else:
            a = "driving"  # 默认是驾车模式
        if self.route_type == '距离最短':
            tactics = '2'
        elif route_type == '不走高速':
            tactics = '3'
        elif route_type == '高速优先':
            tactics = '4'
        elif route_type == '躲避拥堵':
            tactics = '5'
        elif route_type == '少收费':
            tactics = '6'
        elif route_type == '躲避拥堵 & 高速优先':
            tactics = '7'
        elif route_type == '躲避拥堵 & 不走高速':
            tactics = '8'
        elif route_type == '躲避拥堵 & 少收费':
            tactics = '9'
        elif route_type == '躲避拥堵 & 不走高速 & 少收费':
            tactics = '10'
        elif route_type == '不走高速 & 少收费':
            tactics = '11'
        elif route_type == '距离优先':
            tactics = '12'
        else:
            tactics = '0'  # 默认路线类型名
        url = "http://api.map.baidu.com/direction/v2/" + a + "?"   # API地址
        ak = 'sjuGnGH3aYRZCx8lMphRQfhSys5yhYp2'  # 秘钥
        if self.transit_mode == "E-bike":
            # 完整的请求代码
            real_url = url + "origin="+slat+","+slng+"&destination="+dlat+","+dlng+"&ak="+ak+"&riding_type="+"1"
        elif self.transit_mode == "Car":
            real_url = url + "origin=" + slat + "," + slng + "&destination=" + dlat + "," + dlng + "&ak=" + ak + \
                       "&waypoints=" + waypoints + "&tactics=" + tactics
        else:
            real_url = url + "origin="+slat+","+slng+"&destination="+dlat+","+dlng+"&ak="+ak
        req = requests.get(real_url)
        data = json.loads(req.text)  # 将数据保存在数组data中
        # print(data['result']["routes"][0])
        try:  # 防止某几条数据报错导致请求终止
            if self.transit_mode == 'Car':
                total_duration = round(data['result']["routes"][0]["duration"]/60, 2)
                total_distance = round(data['result']["routes"][0]["distance"]/1000, 2)
                stepstr = str(total_distance) + "km" + "/" + str(total_duration) + "min"  # 获取该条数据总行程时间
                steps = data['result']['routes'][0]['steps']  # 获取该条路径的所有步骤
                for step in steps:
                    step_direction = step["direction"]  # 进入道路的角度
                    step_distance = step["distance"]  # 每一步的距离信息
                    step_road = step["road_name"]  # 分段道路名称
                    stepstr = stepstr + "/" + str(step_direction) + "/" + str(step_road) + "/" + str(step_distance) + "m"
            elif self.transit_mode == 'Public transit':
                 total_duration = round(data['result']["routes"][0]["duration"]/60, 2)
                 stepstr = str(total_duration)+"min"
                 # print("total_time: " + stepstr)
                 steps = data['result']["routes"][0]['steps']  # 获取该条路径的所有步骤
                 for step in steps:
                    step_tructions = step[0]["instructions"]  # 每一步的介绍包括乘坐公交车或地铁线路名
                    step_duration = step[0]["duration"]   # 每一步所花费的时间
                    # print(step_tructions, step_duration, str(round(step_duration/60, 2))+"min")
                    stepstr = stepstr+"/"+step_tructions+"/"+str(round(step_duration/60, 2))+"min"
            elif self.transit_mode == 'Bike':
                total_duration = round(data['result']["routes"][0]["duration"] / 60, 2)
                total_distance = round(data['result']["routes"][0]["distance"] / 1000, 2)
                stepstr = str(total_distance) + "km" + "/" + str(total_duration) + "min"  # 获取该条数据总行程时间
                steps = data['result']['routes'][0]['steps']  # 获取该条路径的所有步骤
                for step in steps:
                    # step_direction = step["direction"]  # 当前道路方向角
                    step_distance = step["distance"]  # 每一步的距离信息
                    step_duration = step["duration"]  # 每一步的耗时
                    # bug for step["instructions"] include html
                    step_instructions = step["instructions"]  # 每一步的描述
                    pattern = re.compile(r'<[^>]+>', re.S)
                    step_instruction = pattern.sub('', str(step_instructions))
                    step_name = step["name"]  # 该路段道路名称
                    step_path = step["turn_type"]  # 行驶转向方向
                    stepstr = stepstr + "/" + str(step_distance) + "m" + "/" + str(round(step_duration/60, 2)) + "min"\
                              + "/" + step_instruction + "/" + str(step_name) + "/" + str(step_path)
            else:
                total_duration = round(data['result']["routes"][0]["duration"] / 60, 2)
                total_distance = round(data['result']["routes"][0]["distance"] / 1000, 2)
                stepstr = str(total_distance) + "km" + "/" + str(total_duration) + "min"  # 获取该条数据总行程时间

        except:
             stepstr = None
        req.close()
        return stepstr   #  返回数据为总时长/第一步/第一步耗时/第二步/第二步耗时/...