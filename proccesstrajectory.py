
class Point:

    def __init__(self,lon,lat):

        self.lon = lon
        self.lat = lat

    def __str__(self):

        return 'Point({x},{y})'.format(x=self.lon,y=self.lat)




class Polygon:

    def __init__(self,point_set):

        self.boundary_set = point_set

    # 点在多边形上或者内部
    def contain_point(self,other_point):
        outer_product=[]

        for i in range(len(self.boundary_set) - 1):

            A = self.boundary_set[i]
            B = self.boundary_set[i+1]

            outer_product.append((B.lon - A.lon)*(other_point.lat-A.lat) - (B.lat - A.lat)*(other_point.lon - A.lon))

        A = self.boundary_set[-1]
        B = self.boundary_set[0]

        outer_product.append((B.lon - A.lon) * (other_point.lat - A.lat) - (B.lat - A.lat) * (other_point.lon - A.lon))

        all_less_zero = True
        all_greater_zero = True

        for item in outer_product:

            if item > 0:

                all_less_zero = False

            elif item < 0:

                all_greater_zero = False

        if all_greater_zero or all_less_zero:

            return True

        return False


# file columns traID, carID, occupy, time1, time2, longitude, latitude, speed, angle
# separate occupied taxi trajectory and empty taxi trajectory
# sort occupied taxi trajectory into occupy_file
# sort empty taxi trajectory into empty_file
def process_tra(file_name, occupy_file, empty_file):
    out_occupy = open(occupy_file,'w')
    out_empty = open(empty_file,'w')

    column = dict()

    taxi_trajectory = dict()

    taxi_occupy = dict()

    row = 0

    occupy_tra_num = 0
    empty_tra_num = 0

    with open(file_name,'r') as in_file:

        for line in in_file:
            row += 1

            line = line[:-1]

            data = line.split(',')

            if 1 == row:

                column_str = ""

                for i in range(len(data)):
                    column_str += data[i]+','

                    column[data[i]] = i

                column_str = column_str[:-1]
                column_str += '\n'

                out_occupy.writelines(column_str)
                out_empty.writelines(column_str)

                continue

            taxiID = int(data[column['carID']])
            occupy = int(data[column['occupy']])

            if occupy > 0:
                occupy = 1

            # this taxiID has not been recorded before add it into the record dict
            if taxiID not in taxi_occupy.keys():
                taxi_occupy[taxiID] = occupy

                taxi_trajectory[taxiID] = [line]

            # occupy bit changing means an occupied trajectory or empty trajecotry is end and store these record
            if occupy != taxi_occupy[taxiID]:
                # an occupied reocrd
                if taxi_occupy[taxiID] > 0:

                    if len(taxi_trajectory[taxiID])>0:

                        occupy_tra_num += 1

                        for tra in taxi_trajectory[taxiID]:

                            print(str(occupy_tra_num)+','+tra+'\n')

                            out_occupy.writelines(str(occupy_tra_num)+','+tra+'\n')

                        taxi_trajectory[taxiID]=[]
                        taxi_occupy[taxiID]=occupy
                # an empty record
                else:

                    if len(taxi_trajectory[taxiID])>0:

                        empty_tra_num += 1

                        for tra in taxi_trajectory[taxiID]:

                            print(str(empty_tra_num)+','+tra+'\n')

                            out_empty.writelines(str(empty_tra_num)+','+tra+'\n')

                        taxi_trajectory[taxiID]=[]
                        taxi_occupy[taxiID]=occupy
            else:
                taxi_trajectory[taxiID].append(line)
    # there might be records left in the dict
    for taxiID, trajectory in taxi_trajectory.items():

        if len(trajectory) > 0:
            # an occupied record
            if taxi_occupy[taxiID]>0:

                occupy_tra_num += 1

                for tra in trajectory:
                    print(str(occupy_tra_num)+','+tra+'\n')

                    out_occupy.writelines(str(occupy_tra_num)+','+tra+'\n')
            # an empty record
            else:

                empty_tra_num += 1

                for tra in trajectory:
                    print(str(empty_tra_num) + ',' + tra + '\n')

                    out_empty.writelines(str(empty_tra_num) + ',' + tra + '\n')

    out_occupy.close()
    out_empty.close()

    return occupy_tra_num,empty_tra_num


# file columns traID, carID, occupy, time1, time2, longitude, latitude, speed, angle
# clip the trajectory that contained by the given poly_bound
def process_polyon_tra(file_name, out_file, poly_bound):

    out = open(out_file,'w')
    admin_poly = Polygon(poly_bound)

    column_dict = dict()

    row = 0

    with open(file_name,'r') as in_file:

        for line in in_file:

            lines = line[:-1]
            lines = lines.split(',')

            row += 1

            if row == 1:

                for i in range(len(lines)):

                    column_dict[lines[i]]=i

                continue

            tra_point = Point(float(lines[column_dict['longitude']]), float(lines[column_dict['latitude']]))
            if admin_poly.contain_point(tra_point):

                out.writelines(line)

    out.close()

    return


if __name__ == '__main__':

    print('process big file')