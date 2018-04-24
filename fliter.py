import numpy as np
import math
from shapely.geometry import Point
from shapely.geometry import LineString


# combine the points
# detect the near points by the given min_dis = 20
# input data type trajectory : postgis.LineString
def near_point_combine(trajectory):
    fix_bit = True

    min_dis = 20

    point_num = 0
    point_list = []

    for point in trajectory:

        p = Point(point['x'], point['y'])
        point_list.append(p)

        point_num += 1

    point_correct_list = []

    while fix_bit is True:

        if len(point_list) < 2:
            break

        for i in range(int(len(point_list)/2)):

            point_now = point_list[2*i]
            point_next = point_list[2*i+1]

            dis = point_now.distance(point_next)

            if dis < min_dis:

                point_correct = Point((point_now.x + point_next.x)/2, (point_now.y + point_next.y)/2)
                point_correct_list.append(point_correct)

            else:

                point_correct_list.append(point_now)
                point_correct_list.append(point_next)

        if len(point_list) == len(point_correct_list):

            fix_bit = False

        else:

            point_list = point_correct_list
            point_correct_list = []
    if len(point_list) < 2:
        return LineString()

    line_correct = LineString(point_list)
    #print('combine',str(line_correct))
    return line_correct


# fix the error points
# input data type trajectory : shapely.geometry.LineString
def error_record_fix(trajectory):

    point_list = []
    point_num = 0

    distance_list= []

    for point in list(trajectory.coords):
        p = Point(point[0],point[1])
        point_list.append(p)

        point_num += 1

    if point_num > 2:
        for i in range(point_num - 1):

            dis = point_list[i].distance(point_list[i+1])

            distance_list.append(dis)

        statistics_array = np.array(distance_list)

        avg_dis = statistics_array.mean()
        var_dis = 3*math.sqrt(statistics_array.var())

        for i in range(1,point_num - 1):
            point_now = point_list[i]
            point_pre = point_list[i-1]
            point_next = point_list[i+1]

            dis_pre = point_now.distance(point_pre)
            dis_next = point_now.distance(point_next)

            # the ith point has a problem
            if dis_pre > avg_dis + var_dis and dis_next > avg_dis + var_dis:

                point_correct = Point((point_pre.x + point_next.x)/2,(point_pre.y + point_next.y)/2)

                point_list[i] = point_correct
            # the (i-1)th point has a problem
            elif dis_pre > avg_dis + var_dis:

                point_correct = Point(2*point_now.x - point_next.x, 2*point_now.y - point_next.y)

                point_list[i-1] = point_correct
            # the (i+1)th point has a problem
            elif dis_next > avg_dis + var_dis:

                point_correct = Point(2*point_now.x - point_pre.x,2*point_now.y - point_pre.y)

                point_list[i+1] = point_correct

    line_correct = LineString(point_list)
    #print('fix',str(line_correct))

    return line_correct














