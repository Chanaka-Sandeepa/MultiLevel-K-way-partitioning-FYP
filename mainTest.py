import networkx as nx
from CSVHandlers import ColomboNodesMarker
from GraphControllers import RoadGraph
from CSVHandlers import CSVReader
from GraphControllers.Graph import Graph
from PartitionHandler import Partition
from Utils import MapMarker

if __name__ == '__main__':

    # Creating initial graphs
    # colNodes = ColomboNodesMarker.read_file("Colombo_Nodes.csv")
    # node_list = colNodes[1]
    # node_coordinates = colNodes[0]

############################################
    # road_graph = RoadGraph.read_json_file('Resources/RoadJsons/export_colombo_district.geojson', node_list, node_coordinates)
    # nx.write_graphml(road_graph, "Test_Graphs/minimizedDistrictRoadGraph.graphml")
    # road_graph = nx.read_graphml("Test_Graphs/minimizedDistrictRoadGraph.graphml")
############################################

    # trip_data = CSVReader.read_file('Resources/Datasets/PickmeTrips.csv')
    # ## # trips= [['a','b'],['c','d'],['e','f'],['g','h'],['i','j'],['a','e'],['c','h']]
    # trip_graph = Graph.create_graph(trip_data)
    # nx.write_graphml(trip_graph, "Test_Graphs/TripGraph1.graphml")
    # trip_graph = nx.read_graphml("Test_Graphs/TripGraph1.graphml")
    # road_graph = nx.read_graphml("fullRoadGraph.graphml")
    # Graph.draw_graph(trip_graph)
    # combinedFullGraph = Graph.combineWithNearestRoadGraphNodes(road_graph, trip_data)


###########################################################
    # nx.write_graphml(combinedFullGraph, "Test_Graphs/CombinedMinimizedGraph.graphml")
############################################################

    # nx.write_graphml(trip_graph, "Test_Graphs/TripGraph1.graphml")
    # print("Combining graphs...")
    # cg = Graph.combine_graphs(road_graph, trip_graph)
    # nx.write_graphml(cg, "combinedFullGraph.graphml")
    #
    # # combined_graph = nx.compose(road_graph, trip_graph)
    # nx.write_graphml(cg, "testCombinedGraph2.graphml")

    # Graph.draw_graph(trip_graph)
    # Graph.draw_graph(trip_graph)
    # print("Drawing combined graph...")
    # print("road graph nodes :-", road_graph.number_of_nodes())
    # print("trip graph nodes :-", trip_graph.number_of_nodes())
    # print("combined graph nodes :-", cg.number_of_nodes())
    #
    # Graph.draw_graph(trip_graph)

######################################################################
    # # Partitioning graphs
    # g = nx.read_graphml("fullRoadGraph.graphml")
    # print(g.nodes(data=True))
    # g = GraphReduction.random_match(g)
    # g = TripGraphReduction.random_match(trip_graph)
    # print(g.nodes(data=True))
    # nx.write_graphml(g, "reducedFullCombinedGraph2.graphml")
    # g = nx.read_graphml("testReducedRoadGraph2.graphml")

    # Graph.draw_graph(trip_graph)

    # gs = nx.connected_component_subgraphs(g)
    # c =0
    # for a in gs:
    #     c += 1
    # print('sub in reducedG', c)
    # print('nodes in reducedG', g.number_of_nodes())
####################################################################



    # g = GraphReduction.random_match(trip_graph)
    g = nx.read_graphml("Test_Graphs/CombinedMinimizedGraph.graphml")

    # # gs = nx.connected_component_subgraphs(g)
    # # c =0
    # # for a in gs:
    # #     c += 1
    # # print('sub in reducedG', c)
    # nx.write_graphml(g, "testReducedRoadGraph2.graphml")



    ##############################################################
    orig_graph = nx.read_graphml("Test_Graphs/CombinedMinimizedGraph.graphml")
    partitioned_graphs = Partition.recursive_bisection(g, 0)
    for p in partitioned_graphs:
        print(p.number_of_nodes())
        # Graph.draw_graph(p)

    partition_means_list = Partition.calculatePartitionAvgCoordinate(orig_graph, partitioned_graphs)
    refined_graphs = Partition.refinePartitionedGraphs(partitioned_graphs, orig_graph)
    # MapMarker.initiate_artitions(refined_graphs, orig_graph)
####################################################################




    # Graph.draw_graph(trip_graph)

    # cg = Graph.combine_graphs(road_graph, trip_graph)
    # Graph.check_graph(road_graph)
    # print(trip_graph.nodes(data=True))
    #
    # gs = nx.connected_component_subgraphs(cg)
    # c =0
    # for a in gs:
    #     c += 1
    # print('sub in reducedG', c)

    # col_nodes = ColomboNodesMarker.read_file('Colombo_Nodes.csv')