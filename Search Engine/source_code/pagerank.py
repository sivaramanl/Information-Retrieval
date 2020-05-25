# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 20:01:19 2020

@author: Sivaraman Lakshmipathy
"""

import os
import math
from logger_handler import *
from persistence_handler import *

#Class to represent the nodes in the web graph
class graph_node:

    def __init__(self, identifier):
        self.identifier = identifier
        self.score = -1
        self.iter_score = -1
        self.out_degree = 0
        self.adjList = []

    def get_score(self):
        return self.score

    def update_iter_score(self, new_score):
        self.iter_score = new_score

    def update_score(self, new_score=None):
        if new_score is not None:
            self.score = new_score
        else:
            self.score = self.iter_score

    def update_out_degree(self, update_val=1):
        self.out_degree += update_val

    def get_out_degree(self):
        return self.out_degree

    def update_adjacency_list(self, neighbour):
        self.adjList.append(neighbour)

    def get_adjacency_list(self):
        return self.adjList

#Graph to represent the web graph
class graph:

    def __init__(self):
        self.nodes = {}
        self.edge_size = 0

    def get_size(self):
        return len(self.nodes)

    def get_edge_size(self):
        return self.edge_size

    def get_node_score(self, identifier):
        if identifier in self.nodes:
            return self.nodes[identifier].get_score()
        return 0

    def add_node(self, identifier):
        new_node = graph_node(identifier)
        self.nodes[identifier] = new_node
        return new_node

    def add_edge(self, source, destination):
        if source not in self.nodes:
            source_node = self.add_node(source)
        else:
            source_node = self.nodes[source]
        if destination not in self.nodes:
            destination_node = self.add_node(destination)
        else:
            destination_node = self.nodes[destination]

        if source not in destination_node.adjList:
            source_node.update_out_degree()
            destination_node.update_adjacency_list(source)
            self.edge_size += 1

    def pretty_print(self):
        custom_logger().log_message("Graph pretty print:\n", logger_handler.log_level_INFO)
        for node in self.nodes.values():
            custom_logger().log_message(node.identifier + ":" + str(node.get_score()) + "\n", logger_handler.log_level_INFO)

#Class to represent the PageRank algorith and perform power iteration to calculate the ranking scores for the nodes in the web graph
class pagerank:
    pickle_file_name = os.path.dirname(os.getcwd()) + os.path.sep + "data" + os.path.sep + "network_graph"

    def __init__(self, graph_obj=None, epsilon=0.15):
        if graph_obj is not None:
            custom_logger().log_message("Initializing PageRank algorithm", logger_handler.log_level_INFO)
            self.graph = graph_obj
            self.epsilon = epsilon
            self.alpha = 1 - self.epsilon
            self.beta = self.epsilon / self.graph.get_size()
            self.initialize_scores()
            self.number_of_iterations = int(math.log(self.graph.get_edge_size()))
            if self.number_of_iterations < 10:
                self.number_of_iterations = 10
            custom_logger().log_message("Number of edges:" + str(self.graph.get_edge_size()), logger_handler.log_level_DEBUG)
            custom_logger().log_message("Number of iterations:" + str(self.number_of_iterations), logger_handler.log_level_DEBUG)
            self.run()

    def initialize_scores(self):
        #Initial pagerank scores
        initial_score = 1/self.graph.get_size()
        custom_logger().log_message("Initial score:" + str(initial_score), logger_handler.log_level_DEBUG)
        for node in self.graph.nodes.values():
            node.update_score(initial_score)

    def run(self):
        for iter in range(self.number_of_iterations):
            for id, node in self.graph.nodes.items():
                score_sum = 0
                for neighbour in node.get_adjacency_list():
                    neighbour_node = self.graph.nodes[neighbour]
                    score_sum += neighbour_node.get_score() / neighbour_node.get_out_degree()
                new_score = self.alpha * score_sum + self.beta
                node.update_iter_score(new_score)

            for node in self.graph.nodes.values():
                node.update_score()
        self.pickle_graph()
        custom_logger().log_message("PageRank calculations completed.", logger_handler.log_level_INFO)

    def pickle_graph(self):
        pickle_handler.pickle_object(self.pickle_file_name, self.graph)

    def unpickle_graph(self):
        return pickle_handler.unpickle_object(self.pickle_file_name)
