import csv
import urllib.request
import requests
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

# def read_colombo_nodes(file):
#     count = 0
#     col_nodes = []
#     with open(file, newline='') as csvfile:
#         spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#         for row in spamreader:
#             row_data = row[0].split(",")
#             col_nodes.append({"node":row_data[0], "coordinates":row_data[1]+", "+row_data[2]})
#     print(col_nodes)
#     return col_nodes

m= Basemap(projection='mill',
           llcrnrlat=6.580800891387973,
           llcrnrlon=79.76853095136596,
           urcrnrlat=7.20249391391774,
           urcrnrlon=80.17365180097534,
           resolution='h')


m.drawcoastlines()
m.drawcountries()
# m.drawstates(color='b')
# m.bluemarble()

def mark_map(coordinate1, coordinate2):
    xs = []
    ys = []

    # print(coordinate1, coordinate2)

    xpt, ypt = m(float(coordinate1[0]), float(coordinate1[1]))
    xs.append(xpt)
    ys.append(ypt)
    m.plot(xpt, ypt, 'co', markersize = 5)

    xpt, ypt = m(float(coordinate2[0]), float(coordinate2[1]))
    xs.append(xpt)
    ys.append(ypt)
    m.plot(xpt, ypt, 'co', markersize=5)

    m.plot(xs, ys, color='red', linewidth=1)

# def read_node_data(node_file):
#     count = 0
#     nodes = []
#     print("Reading colombo node data...")
#     with open(node_file, newline='') as csvfile:
#         spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#         for row in spamreader:
#             print(row)
#             count += 1
#             if (count > 1000):
#                 break
#             print(count)
#         print(nodes)
#         return nodes

# def getNodeFromCoordinate(coordinates):
#     url = 'http://localhost:5000/nearest/v1/driving/'+coordinates
#     # print(url)
#     # contents = urllib.request.urlopen(url).read()
#     # print(contents.json())
#     resp = requests.get(url=url)
#     return resp.json().get("waypoints")[0].get("nodes")[0]
#
# def getDistanceFromCoordinate(origin, dest):
#     if (origin is None) or (dest is None):
#         return 0
#     else:
#         url = 'http://localhost:5000/route/v1/driving/'+origin+';'+dest
#         # print(url)
#         # contents = urllib.request.urlopen(url).read()
#         # print(contents.json())
#         resp = requests.get(url=url)
#         if resp.json().get('routes') is None:
#             return 0
#         else:
#             # print(resp.json())
#             return resp.json().get('routes')[0].get('legs')[0].get('distance')


def read_file(csv_path):
    count = 0
    trips =[]
    print("Reading pickme trip data...")
    with open(csv_path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            if(count!=0):
                # print(row)

                if( ((row[0].split(","))[5]).replace('"','') != ""):
                    pickup = ((row[0].replace('"','')).split(","))[3:5]
                    # pickup = row[0].split(",")[3:5]
                    dropoff = ((row[0].replace('"','')).split(","))[5:7]
                    # dropoff = row[0].split(",")[2:4]
                    # print(pickup)
                    # print(dropoff)
                    pickup_node = str(float("{0:.7f}".format(float(pickup[1]))))+","+str(float("{0:.7f}".format(float(pickup[0]))))
                    drop_node = str(float("{0:.7f}".format(float(dropoff[1]))))+","+str(float("{0:.7f}".format(float(dropoff[0]))))
            #         pick_nodeId = getNodeFromCoordinate(pickup_node)
            #         drop_nodeId = getNodeFromCoordinate(pickup_node)
            #         if(pick_nodeId != 0 and drop_nodeId != 0):
                    print(pickup_node, drop_node)
                    # trips.append({"pickup":getNodeFromCoordinate(pickup_node), "drop":getNodeFromCoordinate(drop_node), "pick_cor":pickup_node, "drop_cor":drop_node, "weight":1})
                    trips.append({"pickup":0, "drop":0, "pick_cor":pickup_node, "drop_cor":drop_node, "weight":1})
                    # print(getRouteFromCoordinate(pickup_node, drop_node))
                    # trips.append({"pickup":str(pickup_node), "drop":str(drop_node), "weight":1})
                    # break
                    # getNodeFromCoordinate(pickup_node
                    # mark_map(pickup_node.split(','), drop_node.split(','))
            count += 1
            if(count >1000):
                break
            print(count)
        # print(xs, ys)
        # m.plot(xs, ys, color='red', linewidth= 1)
        # plt.legend(loc=4)
        # plt.title('PickMe trips')
        # plt.show()
        print(trips)
        return trips