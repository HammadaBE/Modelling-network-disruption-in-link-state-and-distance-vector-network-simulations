# as_simulator.py

import threading
import time
import heapq
from collections import defaultdict
import time
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.neighbors = {}  # Neighbors in the format {neighbor_id: cost}
        self.routing_table = {}  # Routing table in the format {destination_id: (next_hop, cost)}

    def add_neighbor(self, neighbor_id, cost):
        self.neighbors[neighbor_id] = cost
        self.routing_table[neighbor_id] = (neighbor_id, cost)

    def distance_vector(self, routing_updates):
        updated = False
        for neighbor_id, neighbor_table in routing_updates.items():
            for dest, (next_hop, cost) in neighbor_table.items():
                new_cost = self.neighbors[neighbor_id] + cost
                if dest not in self.routing_table or new_cost < self.routing_table[dest][1]:
                    self.routing_table[dest] = (neighbor_id, new_cost)
                    updated = True
        return updated

    def link_state(self, graph):
        unvisited = {node: float('inf') for node in graph}
        unvisited[self.node_id] = 0
        previous_nodes = {node: None for node in graph}
        pq = [(0, self.node_id)]

        while pq:
            current_distance, current_node = heapq.heappop(pq)

            if current_distance > unvisited[current_node]:
                continue

            for neighbor, cost in graph[current_node].items():
                distance = current_distance + cost

                if distance < unvisited[neighbor]:
                    unvisited[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))

        # Update the routing table
        for dest, prev_node in previous_nodes.items():
            if prev_node is not None:
                next_hop = dest
                while previous_nodes[next_hop] != self.node_id:
                    next_hop = previous_nodes[next_hop]
                self.routing_table[dest] = (next_hop, unvisited[dest])

class AutonomousSystemSimulator:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node_id):
        node = Node(node_id)
        self.nodes[node_id] = node

    def add_link(self, node1_id, node2_id, cost):
        self.nodes[node1_id].add_neighbor(node2_id, cost)
        self.nodes[node2_id].add_neighbor(node1_id, cost)

    def distance_vector_algorithm(self):
        start_time = time.time()
        converged = False
        while not converged:
            converged = True
            updates = {
                node_id: node.routing_table
                for node_id, node in self.nodes.items()
                if node_id in node.neighbors
            }
            for node in self.nodes.values():
                if node.distance_vector(updates):
                    converged = False
                    print(f"Node {node.node_id} routing table updated (Distance Vector)")
                    print(node.routing_table)
            time.sleep(1)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Distance Vector algorithm converged in {elapsed_time} seconds")

    def link_state_algorithm(self):
        start_time = time.time()
        graph = {node_id: node.neighbors for node_id, node in self.nodes.items()}
        for node in self.nodes.values():
            node.link_state(graph)
            print(f"Node {node.node_id} routing table updated (Link State)")
            print(node.routing_table)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Link State algorithm converged in {elapsed_time} seconds")

    def disrupt_link(self, node1_id, node2_id, cost):
        self.nodes[node1_id].neighbors[node2_id] = cost
        self.nodes[node2_id].neighbors[node1_id] = cost

    def run_algorithm(self, algorithm):
        start_time = time.time()
        if algorithm == 'distance_vector':
            converged = False
            while not converged:
                converged = True
                for node in self.nodes.values():
                    updates = {
                        neighbor_id: self.nodes[neighbor_id].routing_table
                        for neighbor_id in node.neighbors
                    }
                    if node.distance_vector(updates):
                        converged = False
                        print(f"Node {node.node_id} routing table updated (Distance Vector)")
                        print(node.routing_table)
                time.sleep(1)
        elif algorithm == 'link_state':
            graph = {node_id: node.neighbors for node_id, node in self.nodes.items()}
            for node in self.nodes.values():
                node.link_state(graph)
                print(f"Node {node.node_id} routing table updated (Link State)")
                print(node.routing_table)
        else:
            raise ValueError("Invalid algorithm name")
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{algorithm} algorithm converged in {elapsed_time} seconds")

    def create_networkx_graph(self):
        G = nx.Graph()
        G.add_nodes_from(self.nodes.keys())
        for node_id, node in self.nodes.items():
            for neighbor_id, cost in node.neighbors.items():
                G.add_edge(node_id, neighbor_id, weight=cost)
        return G

    def visualize_graph(self, G):
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.show()

import random

def generate_random_node_id(existing_ids):
    while True:
        node_id = chr(random.randint(ord('A'), ord('Z')))
        if node_id not in existing_ids:
            return node_id
        
def get_random_connected_nodes(simulator):
    node_id = random.choice(list(simulator.nodes.keys()))
    connected_node_id = random.choice(list(simulator.nodes[node_id].neighbors.keys()))
    return node_id, connected_node_id
        
if __name__ == '__main__':
    simulator = AutonomousSystemSimulator()


    # Get the number of nodes and edges from the user
    num_nodes = int(input("Enter the number of nodes: "))
    num_edges = int(input("Enter the number of edges: "))

    # Create nodes
    for _ in range(num_nodes):
        node_id = generate_random_node_id(simulator.nodes.keys())
        simulator.add_node(node_id)

    # Add edges between nodes
    node_ids = list(simulator.nodes.keys())
    for _ in range(num_edges):
        node1_id, node2_id = random.sample(node_ids, 2)
        cost = random.randint(1, 10)
        simulator.add_link(node1_id, node2_id, cost)

    # # Create nodes
    # simulator.add_node('A')
    # simulator.add_node('B')
    # simulator.add_node('C')


    # # Add links between nodes
    # simulator.add_link('A', 'B', 1)
    # simulator.add_link('B', 'C', 2)
    # simulator.add_link('A', 'C', 4)

    simulator.run_algorithm('distance_vector')
    simulator.run_algorithm('link_state')

    # Create a NetworkX graph
    G = simulator.create_networkx_graph()

    # Visualize the graph
    simulator.visualize_graph(G)

    # # Disrupt a link
    # simulator.disrupt_link('A', 'B', float('inf'))

    

    

    # Disrupt a link after the first packet is sent
    time.sleep(2)  # Wait 2 seconds to simulate the first packet being sent
    # Select random connected nodes to be disconnected
    node1_id, node2_id = get_random_connected_nodes(simulator)

    # Disrupt the link between the nodes
    simulator.disrupt_link(node1_id, node2_id, float('100'))  # Set the cost to 100 to simulate link failure
    print(f"Disrupted link between {node1_id} and {node2_id}")

    # print("Disrupting link between A and B")
    # simulator.disrupt_link('A', 'B', float('20'))  # Set the cost to 20 to simulate link failure

    # Run the algorithms again to measure the time it takes to redefine the paths
    simulator.run_algorithm('distance_vector')
    simulator.run_algorithm('link_state')

    # Create a new NetworkX graph with the disrupted link
    G_disrupted = simulator.create_networkx_graph()

    # Visualize the disrupted graph
    simulator.visualize_graph(G_disrupted)

    # # Run the Distance Vector algorithm
    # print("Running Distance Vector algorithm")
    # simulator.distance_vector_algorithm()

    # # Run the Link State algorithm 
    # print("Running Link State algorithm")
    # simulator.link_state_algorithm()
