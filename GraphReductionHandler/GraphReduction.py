from random import choice
from CSVHandlers import CSVReader

node_limit = 5000;
matched_data = []
merged_nodes = []
matched_nodes = [];


def addEdge(G, u, v, w, vertex_coordinate):
    if (G.has_edge(u, v)):
        weight = G.get_edge_data(u, v).get('weight');
        G.remove_edge(u, v)
        G.add_node(u, coorinate=vertex_coordinate)
        G.add_node(v)
        G.add_edge(u, v, weight=weight + w)

    else:
        G.add_node(u, coorinate=vertex_coordinate)
        G.add_node(v)
        G.add_edge(u, v, weight=w)


def merge_nodes(graph, vertex, selected_neighbour, vertex_coordinate):
    new_node = str(vertex) + '+' + str(selected_neighbour)
    n_neighbours = graph.neighbors(selected_neighbour)
    graph.add_node(new_node)
    for n1 in list(n_neighbours):
        if not (n1 == vertex):
            matched_data.append([selected_neighbour, n1, graph.get_edge_data(selected_neighbour, n1)])
            # graph.add_edge(new_node, n1, weight=graph.get_edge_data(selected_neighbour, n1).get("weight", 0))
            addEdge(graph, new_node, n1, graph.get_edge_data(selected_neighbour, n1).get("weight", 0), vertex_coordinate)
            graph.remove_edge(selected_neighbour, n1)

    matched_data.append([vertex, selected_neighbour, graph.get_edge_data(vertex, selected_neighbour)])
    graph.remove_node(selected_neighbour)


    v_neighbours = graph.neighbors(vertex)
    for v in list(v_neighbours):
        if not (selected_neighbour == v):
            if not (v == selected_neighbour):
                matched_data.append([v, vertex, graph.get_edge_data(v, vertex).get("weight")])
                # graph.add_edge(new_node, v, weight=graph.get_edge_data(vertex, v).get("weight", 0))
                addEdge(graph, new_node, v, graph.get_edge_data(vertex, v).get("weight", 0), vertex_coordinate)
                graph.remove_edge(vertex, v)

    graph.remove_node(vertex)
    merged_nodes.append({"merged": [vertex, selected_neighbour], "new_node": new_node})
    # print(new_node)
    # print(matched_nodes)
    # print(merged_nodes)
    return graph

def get_node_coordinates(node_list, node):
    print(node)
    node = node.split('+')[0]
    for n in node_list:
        if n[0] == node:
            return n[1].get('coordinate')

    # print(node)



def random_match(graph):
    print('reducing the graph...')
    count = 0;
    node_list = graph.nodes(data=True)
    initial_node_count = graph.number_of_nodes()
    while (graph.number_of_nodes() > node_limit):
        print(graph.number_of_nodes())
        vertex = choice(list(graph.nodes()))
        if not vertex in matched_nodes:
            if (graph.degree(vertex) > 0):
                neighbours = graph.neighbors(vertex);
                for n in neighbours:
                    n_coordinate = get_node_coordinates(node_list, n)
                    vertex_coordinate = get_node_coordinates(node_list, vertex)
                    if ((n not in matched_nodes) & (
                            CSVReader.getDistanceFromCoordinate(n_coordinate, vertex_coordinate) < 300)):
                        graph = merge_nodes(graph, vertex, n, vertex_coordinate)
                        matched_nodes.append(vertex)
                        matched_nodes.append(n)
                        break;

        count += 1
        if (count > initial_node_count * 4):
            print(graph.number_of_nodes())

            break
        if (graph.number_of_nodes()<= node_limit):
            print(graph.number_of_nodes())
            # Graph.draw_graph(graph)
            # print(graph)
            Reduce.rg = graph
            return Reduce.rg

    # Graph.check_graph(graph)
    # Graph.draw_graph(graph)
    return graph


def get_Reduced_graph():
    return Reduce.rg


class Reduce:
    rg = []
