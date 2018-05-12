import networkx as nx
import matplotlib.pyplot as plt2
from CSVHandlers import CSVReader
from scipy import spatial

def addEdge(G, u, v, w):
    print(u, v, w)
    if (G.has_edge(u, v)):
        weight = G.get_edge_data(u, v).get('weight');
        G.remove_edge(u, v)
        G.add_edge(u, v, weight=weight + w)
    else:
        G.add_edge(u, v, weight=w)


class Graph:
    def create_graph(trips):
        print("Creating trips graph...")
        G = nx.Graph()

        for trip in trips:
            if(trip.get("pickup") != trip.get("drop")):
                G.add_node(trip.get("pickup"), coordinate=trip.get("pick_cor"))
                G.add_node(trip.get("drop"), coordinate=trip.get("drop_cor"))
                addEdge(G, trip.get("pickup"), trip.get("drop"), trip.get("weight"))
                # addEdge(G, trip[0], trip[1], 1)

        # print(G.get_edge_data('a','b'))
        # draw_graph(G)
        # check_graph(G)
        print("trip graph nodes :-", G.number_of_nodes())
        # check_graph(G)
        Graph.draw_graph(G)
        return G

    def draw_graph(G):
        edge_labels = dict([((u, v,), d['weight'])
                            for u, v, d in G.edges(data=True)])
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, cmap=plt2.get_cmap('jet'),
                               node_color='r', node_size=100)
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        nx.draw_networkx_edges(G, pos, edge_color='b', arrows=False)
        print(G.number_of_nodes())
        plt2.show()

    # check the nodes with multiple edges
    def check_graph(G):
        print('Checking the graph...')
        count_1 = 0
        count_2 = 0
        count_3 = 0
        count_4 = 0
        count_5 = 0

        edges = G.edges(data=True)
        nodes = G.nodes()
        # for n in nodes:
        #     print(n)

        for e in edges:
            # print(e)
            weight = e[2].get('weight')
            if (weight == 1):
                count_1 += 1
            elif (weight == 2):
                count_2 += 1
            elif (weight == 3):
                count_3 += 1
            elif (weight == 4):
                count_4 += 1
            elif (weight == 5):
                count_5 += 1

        print('weight_1:', count_1)
        print('weight_2:', count_2)
        print('weight_3:', count_3)
        print('weight_4:', count_4)
        print('weight_5:', count_5)
        print('nodes', G.number_of_nodes())

    def combine_graphs(g1, g2):
        for e in g1.edges(data= True):
            g2.add_edge(e[0],e[1], weight= e[2].get('weight'))

        return g2

    def getNearestNode(road_nodes, trip_core):
        min_distance = 1000
        nearest_node = None
        for node in road_nodes:
            dist = CSVReader.getDistanceFromCoordinate(node[1].get('coordinate'), trip_core)
            if not dist == 0:
                if(min_distance> dist):
                    nearest_node = node

        print(nearest_node)
        return nearest_node



    def combineWithNearestRoadGraphNodes(road_graph, trip_data):
        print("combining into road graph...")
        node_list = road_graph.nodes(data=True)
        cor_list = []
        c = 0

        for node in node_list:
            coordinate = node[1].get('coordinate').split(",")
            cor_list.append((float(coordinate[0]), float(coordinate[1])))
  
        print(cor_list)
        tree = spatial.KDTree(cor_list)

        for trip in trip_data:
            start = trip.get("pick_cor").split(",")
            dest = trip.get("drop_cor").split(",")
            start_tuple = [(float(start[0]), float(start[1]))]
            dest_tuple = [(float(dest[0]), float(dest[1]))]
            nearestStartNode= node_list[tree.query(start_tuple)[1][0]][0]
            nearestDestNode= node_list[tree.query(dest_tuple)[1][0]][0]
            addEdge(road_graph, nearestStartNode, nearestDestNode, trip.get("weight"))
            print(tree.query(start_tuple)[1][0])
        print(road_graph.number_of_nodes())
        return road_graph