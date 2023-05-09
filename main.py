########################
### Author: Matrix.L ###
###       ICT        ###
########################

# package
import matplotlib.pyplot as plt
import networkx as nx
from TLE import tle
from skyfield.api import EarthSatellite
from skyfield.api import load, wgs84
import datetime
from timefunction import calculate_time
from def_class import sat_rise_down
from threading import Thread, Lock

# load all starlink satellite
# it is my function
satellites = tle.load_tle()
# This is location of Beijing
bluffton = wgs84.latlon(+39.9042, +116.4074)
# get the start_time and end_time
# it is my function
t0, t1 = calculate_time.calculate_start_end_time(1800)
# record rise, culminate, set of every satellite
sat_squence = []
# parallel index
num = 0


def task(squence_mutex, num_mutex, list_size):
    global num
    global thread_num
    # record information into sat_squence
    list_start = 0
    list_end = 0
    # Lock, get the data need to handle
    num_mutex.acquire()
    list_start = num
    step = (int)(list_size / thread_num)
    list_end = list_start + step
    list_end = list_end if list_end < list_size else list_size
    num = list_end
    num_mutex.release()
    for sat in satellites[list_start:list_end]:
        # refer to https://rhodesmill.org/skyfield/earth-satellites.html
        # it is pretty useful
        t, events = sat.find_events(bluffton, t0, t1, altitude_degrees=20.0)
        event_names = 'rise', 'culminate', 'set'
        sat_name = sat.name
        index = 0
        # create a class which record the satellite's name, rise_time, cul_time, set_time
        # it is my class
        sat = sat_rise_down.sat_rise_down()
        sat.name = sat_name
        # record pre satellite
        len_event = len(events)
        while(index < len_event):
            ti = t[index]
            event = events[index]
            utc_str = ti.utc_strftime('%Y %m %d %H:%M:%S')
            record_time = datetime.datetime.strptime(
                utc_str, '%Y %m %d %H:%M:%S')
            if(index % 3 == 0):
                sat = sat_rise_down.sat_rise_down()
                sat.name = sat_name
                sat.rise = utc_str
            if(index % 3 == 1):
                sat.culminate = utc_str
            if(index % 3 == 2):
                sat.down = utc_str
                squence_mutex.acquire()
                sat_squence.append(sat)
                squence_mutex.release()
            index += 1


squence_mutex = Lock()
num_mutex = Lock()
thread_list = []
sat_list_size = len(satellites)
# parallel start
thread_num = 3
for i in range(thread_num):
    t = Thread(target=task, args=(squence_mutex, num_mutex, sat_list_size))
    thread_list.append(t)
    t.start()
# parallel wait
for t in thread_list:
    t.join()
# release the memory
del thread_list
del satellites

# Sort the sat_squeue by rise time
sat_squence.sort(key=lambda x: x.rise)

# create graph
DG = nx.DiGraph()
# sats_len = len(sat_squence)
sats_len = 4
edges = []
# print(sats_len)
for index1 in range(sats_len):
    for index2 in range(index1 + 1, sats_len):
        sat1_rise_time = sat_squence[index1].rise
        sat1_set_time = sat_squence[index1].down
        sat2_rise_time = sat_squence[index2].rise
        sat2_set_time = sat_squence[index2].down
        time_difference_1 = calculate_time.time_difference_seconds(
            sat2_rise_time, sat1_set_time)
        time_difference_2 = calculate_time.time_difference_seconds(
            sat1_set_time, sat2_set_time)
        if(not (time_difference_1 > 10 and time_difference_1 < 3600)):
            break
        if(time_difference_1 > 10 and time_difference_1 < 3600):
            if(time_difference_2 > 0 and time_difference_2 < 3600):
                cost = 1800-calculate_time.time_difference_seconds(
                    sat2_rise_time, sat2_set_time)
                DG.add_edge(sat_squence[index1].name,
                            sat_squence[index2].name, weight=cost)


# pos = nx.spring_layout(DG)
# nx.draw_networkx_nodes(DG, pos, cmap=plt.get_cmap('jet'))
# nx.draw_networkx_labels(DG, pos)
# labels = nx.get_edge_attributes(DG, 'weight')
# nx.draw_networkx_edge_labels(DG, pos, edge_labels=labels)
# plt.savefig('picture.png')
pos = nx.spring_layout(DG)
nx.draw_networkx_nodes(DG, pos, cmap=plt.get_cmap('jet'))
nx.draw_networkx_labels(DG, pos)
nx.draw_networkx_edges(DG, pos, arrows=True)
# labels = nx.get_edge_attributes(DG, 'weight')
# nx.draw_networkx_edge_labels(DG, pos, edge_labels=labels)
plt.savefig('picture.png')

print(DG.number_of_nodes())
print(DG.number_of_edges())
