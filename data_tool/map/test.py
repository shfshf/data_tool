import requests
from pos_coord import Coord2Pos, Pos2Coord


def get_pos(origin0, destination0):
    origin1 = Pos2Coord(origin0)
    origin_lng = origin1['lng']
    origin_lat = origin1['lat']
    origin_ln = str(round(origin_lat, 6))
    origin_la = str(round(origin_lng, 6))

    destination1 = Pos2Coord(destination0)
    destination_lng = destination1['lng']
    destination_lat = destination1['lat']
    destination_ln = str(round(destination_lat, 6))
    destination_la = str(round(destination_lng, 6))

    return origin_ln, origin_la, destination_ln, destination_la


def get_pos1(origin):
    origin1 = Pos2Coord(origin)
    origin_lng = origin1['lng']
    origin_lat = origin1['lat']
    ln = str(round(origin_lat, 3))
    la = str(round(origin_lng, 3))
    pos = ln + "," + la

    return pos


origin = '上海大学宝山校区'
destination = '上海迪士尼乐园'
approach_path = ['东方明珠', '上海徐家汇地铁站']

route_type = '躲避拥堵'

origin_ln, origin_la, destination_ln, destination_la = get_pos(origin, destination)
origin = origin_ln + "," + origin_la
destination = destination_ln + "," + destination_la
approach = ''

print(approach_path)
for i in approach_path:
    approach = approach + "|" + get_pos1(i)
    print(approach)

waypoints = approach[1:]  # 途径点
print(waypoints)
#
if route_type == '距离最短':
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
    tactics = '0'

# origin = '40.01116,116.339303'
# destination = '39.936404,116.452562'
AK = 'sjuGnGH3aYRZCx8lMphRQfhSys5yhYp2'
# # 驾车
url = 'http://api.map.baidu.com/direction/v2/driving?origin=%s&destination=%s&ak=%s&waypoints=%s&tactics=%s' % (origin, destination, AK, waypoints, tactics)
# real_url = url + "origin="+slat+","+slng+"&destination="+dlat+","+dlng+"&ak="+ak
print(url)
r = requests.get(url)
print(r.status_code)

r_js = r.json()
# 返回js数据
print(r_js['status'])
routes_ = r_js['result']['routes'][0]
dis_ = routes_['distance']
time_ = routes_['duration']

print('总行程距离为：' + str(dis_) + '米，总时间为：' + str(time_) + '秒')
