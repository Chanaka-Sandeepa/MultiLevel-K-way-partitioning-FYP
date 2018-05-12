from random import choice
from Utils import MapMarker
import networkx as nx
from scipy import spatial

edge_cut =[]
partition_weights = []
partitioned_graphs =[]
parts = 0


def calculate_gain(node, graph, graphA, graphB):
    gain = 0
    neighbours = graph.neighbors(node)
    for n in neighbours:
        if graphA.has_node(n):
            gain = gain + graph.get_edge_data(node, n).get('weight')
        else:
            gain = gain - graph.get_edge_data(node, n).get('weight')

    return gain


def get_max_gain(gains):
    max_gain = -1000
    max_gain_node = []
    for g in gains:
        if(g.get('gain') > max_gain):
            max_gain = g.get('gain')
            max_gain_node = g
    gains.remove(max_gain_node)
    return max_gain_node

def is_in_gains(node, gains):
    for g in gains:
        if g.get("node") == node:
            return True
    return False

def get_initial_edge_cut(vertex, graph):
    cut= 0
    neighbours = graph.neighbors(vertex)
    for n in neighbours:
        cut = cut + graph.get_edge_data(vertex, n).get('weight')
    return cut

def recursive_bisection(graph, partition_count):
    count= 0
    local_edge_cut = 0
    partition_count += 1
    total_graph_weight = graph.size(weight='weight')

    vertex = choice(list(graph.nodes()))
    while(graph.degree(vertex)==0):
        vertex = choice(list(graph.nodes()))
    # vertex = 5216959120
    local_edge_cut = get_initial_edge_cut(vertex, graph)
    # print(local_edge_cut)
    graphA = nx.Graph()
    graphA.add_node(vertex)
    graphB = graph.copy()
    graphB.remove_node(vertex)

    gains = []
    neighbours = graph.neighbors(vertex)
    # print(vertex)
    for n in neighbours:
        if n not in graphA:
            if not is_in_gains(n, gains):
                gains.append({"node":n, "gain":calculate_gain(n, graph, graphA, graphB)})

    # print(gains)
    while (graphA.size(weight='weight') < total_graph_weight/2):
        max_gain_entry = get_max_gain(gains)
        local_edge_cut = local_edge_cut - max_gain_entry.get("gain")
        # print(local_edge_cut)
        max_gain_vertex = max_gain_entry.get("node")
        print(graphA.size(weight='weight'), total_graph_weight/2)
        graphA.add_node(max_gain_vertex)
        graphB.remove_node(max_gain_vertex)
        m_neighbours = graph.neighbors(max_gain_vertex)
        for n in m_neighbours:
            if n not in graphA:
                if not is_in_gains(n, gains):
                    gains.append({"node": n, "gain": calculate_gain(n, graph, graphA, graphB)})
            else:
                graphA.add_edge(n, max_gain_vertex,
                                weight=graph.get_edge_data(n, max_gain_vertex).get('weight'))

        # print(gains)
        count += 1
        if count > (graph.number_of_nodes() * 2):
            edge_cut.append({local_edge_cut})
            print(edge_cut)
            break
        elif len(gains) == 0:
            local_count = 0
            vertex = choice(list(graphB.nodes()))
            while (graphB.degree(vertex) == 0):
                local_count += 1
                vertex = choice(list(graphB.nodes()))
                print(vertex)
                if(local_count < 800):
                    print('vghv', len(partitioned_graphs))
                    return partitioned_graphs

            neighbours = graphB.neighbors(vertex)
            # print(vertex)
            for n in neighbours:
                if n not in graphA:
                    if not is_in_gains(n, gains):
                        gains.append({"node": n, "gain": calculate_gain(n, graph, graphA, graphB)})

    edge_cut.append(local_edge_cut)
    partition_weights.append({graphA.size(weight='weight'), graphB.size(weight="weight")})
    # print(edge_cut)

    # Graph.draw_graph(graphB)
    # print(partition_count)
    if(partition_count< 3):
        recursive_bisection(graphA, partition_count)
        recursive_bisection(graphB, partition_count)
    elif(partition_count == 3):
        partitioned_graphs.append(graphA)
        partitioned_graphs.append(graphB)
    else:
        # print(partitioned_graphs)
        print('vghv',len(partitioned_graphs))
        return partitioned_graphs

    print("partition weights", partition_weights)
    print("edge cut sum", sum(edge_cut))
    return partitioned_graphs

def calculatePartitionAvgCoordinate(original_graph, partitioned_graphs):
    print("calculating partition mean coordinate")
    node_list = original_graph.nodes(data=True)
    partition_mean_list = []
    count = 0
    for partition in partitioned_graphs:
        local_coordinateX = 0
        local_coordinateY = 0
        node_count = 0
        for node in partition:
            # if node_count > 1000:
            #     break
            coordinate = MapMarker.get_node_coordinates(node_list, str(node))
            if coordinate is not None:
                coordinateX = coordinate.split(",")[0]
                coordinateY = coordinate.split(",")[1]
                print(coordinateX, coordinateY)
                local_coordinateX = local_coordinateX + float(coordinateX)
                local_coordinateY = local_coordinateY + float(coordinateY)
                node_count += 1
            count =+ 1
        partition_meanX = local_coordinateX/node_count
        partition_meanY = local_coordinateY/node_count
        partition_mean_list.append((partition_meanX, partition_meanY))
    return partition_mean_list

def refinePartitionedGraphs(partitionedGraphs, original_graph):
    print("refining partitioned graphs")
    node_list = original_graph.nodes(data=True)
    partition_mean_list = calculatePartitionAvgCoordinate(original_graph, partitioned_graphs)[0:7]
    tree = spatial.KDTree(partition_mean_list)
    for partition in reversed(partitionedGraphs):
        current_graph_index = partitionedGraphs.index(partition)
        count = 0
        print("refining partition :", partitionedGraphs.index(partition))
        for node in list(partition):
            count += 1
            # if count > 1000:
            #     break
            str_coordinate = MapMarker.get_node_coordinates(node_list, str(node))
            if str_coordinate is not None:
                coordinate = str_coordinate.split(",")
                cor_tuple = [((float(coordinate[0]), float(coordinate[1])))]
                # print(cor_tuple)
                # print(partition_mean_list)
                matching_graph_index = tree.query(cor_tuple)[1][0]
                # print(tree.query(cor_tuple)[1][0])
                if matching_graph_index != current_graph_index:
                    # print("before adding", partitioned_graphs[matching_graph_index].number_of_nodes())
                    partitioned_graphs[matching_graph_index].add_node(node, coordinate=str_coordinate)
                    # print("after adding", partitioned_graphs[matching_graph_index].number_of_nodes())
                    partition.remove_node(node)
        # if current_graph_index == 1:
        #     break

    print(partitionedGraphs)
    return partitionedGraphs


