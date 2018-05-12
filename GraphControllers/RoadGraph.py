import json
import networkx as nx
from CSVHandlers import CSVReader
from scipy import spatial

# m= Basemap(projection='mill',
#            llcrnrlat=6.580800891387973,
#            llcrnrlon=79.76853095136596,
#            urcrnrlat=7.20249391391774,
#            urcrnrlon=80.17365180097534,
#            resolution='h')
# xs = []
# ys = []
#
# def mark_map(coordinate1, coordinate2):
#     # print(coordinate1)
#     # print(coordinate2)
#
#     xpt, ypt = m(float(coordinate1[0]), float(coordinate1[1]))
#     xs.append(xpt)
#     ys.append(ypt)
#     m.plot(xpt, ypt, 'co', markersize = 5)
#
#     xpt, ypt = m(float(coordinate2[0]), float(coordinate2[1]))
#     xs.append(xpt)
#     ys.append(ypt)
#     m.plot(xpt, ypt, 'co', markersize=5)

def addEdge(G, u, v, w):
    if (G.has_edge(u, v)):
        weight = G.get_edge_data(u, v).get('weight');
        G.remove_edge(u, v)
        G.add_edge(u, v, weight=weight + w)
    else:
        G.add_edge(u, v, weight=w)

def create_road_graph(roads):
    print("Creating roads graph...")
    G = nx.Graph()
    count = 0

    for road in roads:
        # print(road)

        for i in range(len(road)-1):
            # print(road)
            # print(road[i+1])
            # print(str(road[i+1]))
            cor = (str(road[i]).replace("[", "").replace("]", ""))
            cor_node = CSVReader.getNodeFromCoordinate(cor.replace(" ", ""))
            cor_next = (str(road[i+1]).replace("[", "").replace("]", ""))
            cor_next_node = CSVReader.getNodeFromCoordinate(cor_next.replace(" ", ""))
            # print(CSVReader.getDistanceFromCoordinate(cor.replace(' ', ''), cor_next.replace(' ', '')))
            print(cor_node, cor_next_node)
            # mark_map(cor.split(","), cor_next.split(","))
            # G.add_edge(str(road[i]).replace("[","").replace("]",""),str(road[i+1]).replace("[","").replace("]",""), weight =0)
            if(cor_next_node != 0 and cor_node != 0 and cor_next_node != cor_node):
                G.add_node(cor_node, coordinate=cor.replace(" ", ""))
                G.add_node(cor_next_node, coordinate=cor_next.replace(" ", ""))
                G.add_edge(cor_node,cor_next_node, weight =0)
        # addEdge(G, road[0], road[1], 1)

    # Graph.draw_graph(G)
    # m.plot(xs, ys, color='red', linewidth= 1)
    # plt.legend(loc=4)
    # plt.title('Western')
    # plt.show()
    print("road graph nodes :-", G.number_of_nodes())


    gs = nx.connected_component_subgraphs(G)

    c =0
    for a in gs:
        c += 1
    print('sub in roadG', c)

    return G


def create_minimized_road_graph(roads, node_list, colombo_cor_list):
    print("Creating minimized roads graph...")
    G = nx.Graph()
    road_cor_list = []
    tree = spatial.KDTree(colombo_cor_list)

    road_count = 0
    for road in roads:
        # print(road)
        road_count += 1
        # if road_count > 100:
        #     break
        for i in range(len(road)-1):
            # print(road)
            # print(road[i+1])
            # print(str(road[i+1]))
            cor = (str(road[i]).replace("[", "").replace("]", "")).split(",")
            cor_next = (str(road[i+1]).replace("[", "").replace("]", "")).split(",")
            print((float(cor[0]), float(cor[1])))
            cor_tuple = (float(cor[0]), float(cor[1]))
            cor_next_tuple = (float(cor_next[0]), float(cor_next[1]))
            print(tree.query(cor_tuple))
            cor_index = tree.query(cor_tuple)[1]
            cor_next_index = tree.query(cor_next_tuple)[1]
            nearestStartNode = node_list[cor_index]
            nearestDestNode= node_list[cor_next_index]
            G.add_node(nearestStartNode, coordinate=str(colombo_cor_list[cor_index][0]) + "," +str(colombo_cor_list[cor_index][1]))
            G.add_node(nearestDestNode, coordinate=str(colombo_cor_list[cor_next_index][0]) + "," +str(colombo_cor_list[cor_next_index][1]))
            G.add_edge(nearestStartNode, nearestDestNode, weight=0)
            # mark_map(cor.split(","), cor_next.split(","))
            # G.add_edge(str(road[i]).replace("[","").replace("]",""),str(road[i+1]).replace("[","").replace("]",""), weight =0)
             # addEdge(G, road[0], road[1], 1)
    print("minnimized road graph nodes :-", G.number_of_nodes())


    gs = nx.connected_component_subgraphs(G)
    c =0
    for a in gs:
        c += 1
    print('sub in minimized roadG', c)

    return G

def read_json_file(file, node_list, cor_list):
    print("Reading road json files...")
    count = 0
    with open(file) as data_file:
        data = json.load(data_file)
    # pprint(data)
    features = data["features"]
    roads = []
    for f in features:
        if('geometry' in f) and (f["geometry"]["type"] != 'Point'):
            # print(f["geometry"]["type"])
            roads.append(f["geometry"]["coordinates"])
        # print(roads)
        # if(count >50):
        #     break
        count += 1


    return create_minimized_road_graph(roads, node_list, cor_list)
    # print(mpl_toolkits.__file__)


def get_colombo_map():
    print("dad")