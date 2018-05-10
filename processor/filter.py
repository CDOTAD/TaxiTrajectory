import numpy as np
import math
from filterpy.gh import GHFilter
from shapely.geometry import Point
from shapely.geometry import LineString


# combine the points
# detect the near points by the given min_dis = 20
# input data type trajectory : postgis.LineString
def near_point_combine(trajectory):
    fix_bit = True

    min_dis = 70

    point_num = 0
    point_list = []

    for point in trajectory:

        p = Point(point['x'], point['y'])
        point_list.append(p)

        point_num += 1

    point_correct_list = []

    #print('point_lis',point_list)

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
    #print(point_list)
    if len(point_list) < 2:
        return LineString()

    line_correct = LineString(point_list)
    #print('combine',str(line_correct))
    return line_correct


# return LineString, distance_mean, distance_var, point_num
"""
def trajectory_statis(trajectory):

    point_list=[]
    dis_list=[]
    for point in list(trajectory.coords):
        p = Point(point[0],point[1])
        point_list.append(p)

    for i in range(len(point_list)-1):

        point_now = point_list[i]
        point_next = point_list[i+1]

        dis_list.append(point_now.distance(point_next))

    statistics = np.array(dis_list)

    mean = statistics.mean()
    var = statistics.var()
    n = len(dis_list)

    return LineString(point_list),mean,var,n
"""


# fix the error points
# input data type trajectory : shapely.geometry.LineString
def error_record_fix(trajectory, avg_dis=None, var_dis=None):

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
        if avg_dis is None:
            avg_dis = statistics_array.mean()
        if var_dis is None:
            var_dis = 3*math.sqrt((point_num/(point_num - 1))*statistics_array.var())

        print('avg_dis',avg_dis)
        print('var_dis',var_dis)

        print('dis_array',distance_list)

        error_list =[]

        for i in range(len(distance_list)):

            if distance_list[i] > avg_dis + var_dis:

                error_list.append(i)

        print('error_list',error_list)

        if len(error_list) == 0:
            if avg_dis > 1000:
                return None

        if len(error_list)>1:
            for i in range(len(error_list)-1):

                error_dis_now = error_list[i]
                error_dis_next = error_list[i+1]

                if error_dis_next == error_dis_now + 1:
                    error_index = error_dis_next
                    error_point = point_list[error_index]
                    point_pre = point_list[error_index-1]
                    point_next = point_list[error_index+1]

                    point_correct = Point((point_pre.x + point_next.x)/2,(point_pre.y + point_pre.y)/2)

                    point_list[error_dis_next] = point_correct
        elif len(error_list) == 1:

            if error_list[0] == 0:

                error_point = point_list[0]
                point_1 = point_list[1]
                point_2 = point_list[2]

                point_correct = Point(2*point_1.x - point_2.x, 2*point_1.y - point_2.y)

                point_list[0] = point_correct
            elif error_list[0] == len(point_list) - 1:

                error_point = point_list[-1]
                point_1 = point_list[-2]
                point_2 = point_list[-3]

                point_correct = Point(2*point_1.x - point_2.x, 2*point_1.y - point_2.y)

                point_list[-1] = point_correct


        """
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
            """
    line_correct = LineString(point_list)
    #print('fix',str(line_correct))

    return line_correct


# filt with filterpy.gh_filter
# input trajectory, velocity, avg_dis[selective], var_dis[selective]
def tra_gh_filter(trajectory, v, avg_dis=152.5781, var_dis=327.7119):

    point_list=[]
    for point in list(trajectory.coords):
        point_list.append(Point(point))
    point_num = len(point_list)

    distance_list=[]
    for i in range(point_num-1):
        dis = point_list[i].distance(point_list[i + 1])

        distance_list.append(dis)

    error_list=[]
    for i in range(len(distance_list)):
        if distance_list[i] > avg_dis + 3*var_dis:

            error_list.append(i)

    error_point = []
    if len(error_list) > 1:
        for i in range(len(error_list) - 1):

            error_dis_now = error_list[i]
            error_dis_next = error_list[i + 1]

            if error_dis_next == error_dis_now + 1:
                error_index = error_dis_next
                error_point.append(error_dis_next)
    elif len(error_list) == 1:
        if error_list[0] == point_num - 1:
            error_index = point_num - 1
            error_point.append(error_index)

    x_0 = np.array([point_list[0].x, point_list[0].y])
    dx_0 = np.array(v)

    gh_f_tra = GHFilter(x=x_0, dx=dx_0, dt=10., g=.8, h=.2)
    correct_point = [point_list[0]]
    for i in range(1, len(point_list)):
        if i in error_point:
            gh_f_tra.g = 0
            gh_f_tra.h = 0
        else:
            gh_f_tra.g = .8
            gh_f_tra.h = .2
        gh_f_tra.update(z=np.array([point_list[i].x,point_list[i].y]))

        correct_point.append(gh_f_tra.x)

    line_correct = LineString(correct_point)

    return line_correct























