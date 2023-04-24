 
import random
import time
import networkx as nx
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import csv


# Distance-vector algorithm (basic implementation)
def distance_vector_algorithm(G, source):
    distance = {node: float('inf') for node in G.nodes}
    distance[source] = 0

    for _ in range(len(G.nodes) - 1):
        for u, v, data in G.edges(data=True):
            weight = data['weight']
            if distance[u] + weight < distance[v]:
                distance[v] = distance[u] + weight
            if distance[v] + weight < distance[u]:
                distance[u] = distance[v] + weight

    return distance

# Link-state algorithm (basic implementation)
def link_state_algorithm(G, source):
    distance = {node: float('inf') for node in G.nodes}
    distance[source] = 0
    unvisited_nodes = list(G.nodes)

    while unvisited_nodes:
        current_node = min(unvisited_nodes, key=lambda node: distance[node])
        unvisited_nodes.remove(current_node)

        for neighbor in G.neighbors(current_node):
            weight = G[current_node][neighbor]['weight']
            new_distance = distance[current_node] + weight
            if new_distance < distance[neighbor]:
                distance[neighbor] = new_distance

    return distance



 # Calculate the latency for distance-vector and link-state algorithms
def distance_vector_algorithm_time(G, source):
        start_time = time.perf_counter()
        distance_vector_result = distance_vector_algorithm(G, source)
        distance_vector_latency = time.perf_counter() - start_time
        print("Distance-vector result:", distance_vector_result)
        print("Distance-vector latency:", distance_vector_latency)
        return distance_vector_latency

def link_state_algorithm_time(G,source):
    start_time = time.perf_counter()
    link_state_result = link_state_algorithm(G, source)
    link_state_latency = time.perf_counter() - start_time
    print("Link-state result:", link_state_result)
    print("Link-state latency:", link_state_latency)
    return link_state_latency

