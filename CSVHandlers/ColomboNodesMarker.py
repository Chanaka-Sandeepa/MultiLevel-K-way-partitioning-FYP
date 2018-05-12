import csv
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


# m= Basemap(projection='mill',
#            llcrnrlat=6.580800891387973,
#            llcrnrlon=79.76853095136596,
#            urcrnrlat=7.20249391391774,
#            urcrnrlon=80.17365180097534,
#            resolution='h')
#
#
# m.drawcoastlines()
# m.drawcountries()
# m.drawstates(color='b')
# m.bluemarble()

# def mark_map(coordinateX, coordinateY):
#
#     xpt, ypt = m(float(coordinateX), float(coordinateY))
#
#     m.plot(xpt, ypt, 'co', markersize = 1)


def read_file(csv_path):
    count = 0
    nodes =[]
    node_coordinates = []
    print("Reading Colombo Nodes data...")
    with open(csv_path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            if(count!=0):
                print(row[0])
                if(row[0] != ""):
                    print(row[0].split(",")[1])
                    coX = row[0].split(",")[1]
                    coY = row[0].split(",")[2]
                    nodeId = row[0].split(",")[0]
                    nodes.append(nodeId)
                    node_coordinates.append((float(coX), float(coY)))
                    # mark_map(coX, coY)


            count += 1
            # if(count >30):
            #     break
            # print(count)
        print(nodes)
        return [node_coordinates, nodes]
        # plt.title('PickMe trips')
        # plt.show()
