from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

xs =[]
ys= []

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

def draw_on_map():
    print(xs, ys)
    m.plot(xs, ys, color='red', linewidth= 1)
    # plt.legend(loc=4)
    plt.title('PickMe trips')
    plt.show()