from data_tool.map.round_plan import Round_plan
from data_tool.map.pos_coord import Coord2Pos, Pos2Coord


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


if __name__ == '__main__':

    transit_mode = 'Car'

    origin = '上海大学宝山校区'
    destination = '上海迪士尼乐园'
    # approach_path = ['东方明珠', '上海徐家汇地铁站']
    approach_path = ''
    # route_type = '距离优先'
    route_type = ''
    # '距离最短','不走高速','高速优先','躲避拥堵','少收费','躲避拥堵 & 高速优先','躲避拥堵 & 不走高速'
    # '躲避拥堵 & 少收费','躲避拥堵 & 不走高速 & 少收费','不走高速 & 少收费','距离优先'
    if approach_path:
        approach = ''
        for i in approach_path:
            approach = approach + "|" + get_pos1(i)

        waypoints = approach[1:]  # 途径点
    else:
        waypoints = ''

    origin_ln, origin_la, destination_ln, destination_la = get_pos(origin, destination)

    if transit_mode == 'Public transit':
        rount_result = Round_plan(transit_mode)
        stepstr = rount_result.stod(origin_ln, origin_la, destination_ln, destination_la)
        stepstr_list = stepstr.split('/')
        print(origin + "-->" + destination)
        print("total_time: " + stepstr_list[0])
        all_path = list(stepstr_list[1:])
        n = 2
        for b in [all_path[i:i + n] for i in range(0, len(all_path), n)]:
            print(', '.join(b))
    elif transit_mode == 'Car':
        car_res = Round_plan(transit_mode)
        stepstr = car_res.stod(origin_ln, origin_la, destination_ln, destination_la, waypoints, route_type)
        stepstr_list = stepstr.split('/')
        print(origin + "-->" + destination)
        print("total_distance: " + stepstr_list[0])
        print("total_time: " + stepstr_list[1])
        all_path = list(stepstr_list[2:])
        n = 3
        res = []
        for b in [all_path[i:i + n] for i in range(0, len(all_path), n)]:
            print(', '.join(b))
            res.append(', '.join(b))
        print(res)
    elif transit_mode == 'Bike':
        ride_res = Round_plan(transit_mode)
        stepstr = ride_res.stod(origin_ln, origin_la, destination_ln, destination_la)
        stepstr_list = stepstr.split('/')
        print(origin + "-->" + destination)
        print("total_distance: " + stepstr_list[0])
        print("total_time: " + stepstr_list[1])
        all_path = list(stepstr_list[2:])
        n = 5
        for b in [all_path[i:i + n] for i in range(0, len(all_path), n)]:
            print(', '.join(b))
    else:
        walk_res = Round_plan(transit_mode)
        stepstr = walk_res.stod(origin_ln, origin_la, destination_ln, destination_la)
        print(stepstr)








