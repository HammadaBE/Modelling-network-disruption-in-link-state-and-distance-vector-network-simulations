
import threading
import time
import heapq
from collections import defaultdict
import time
import networkx as nx
import matplotlib.pyplot as plt
import socket
import logging

logging.basicConfig(filename='packet_log.txt', level=logging.INFO)

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
        self.emulator_host = '127.0.0.1'
        self.emulator_port = 12345

    def add_node(self, node_id):
        node = Node(node_id)
        self.nodes[node_id] = node

    def add_link(self, node1_id, node2_id, cost):
        self.nodes[node1_id].add_neighbor(node2_id, cost)
        self.nodes[node2_id].add_neighbor(node1_id, cost)

    def disrupt_link(self, node1_id, node2_id, cost):
        self.nodes[node1_id].neighbors[node2_id] = cost
        self.nodes[node2_id].neighbors[node1_id] = cost

    def run_algorithm(self, algorithm):
        print(f"Running {algorithm} algorithm...")
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
                        logging.info(f"Node {node.node_id} routing table updated (Distance Vector)")
                        logging.info(node.routing_table)
                time.sleep(1)
        elif algorithm == 'link_state':
            graph = {node_id: node.neighbors for node_id, node in self.nodes.items()}
            for node in self.nodes.values():
                node.link_state(graph)
                logging.info(f"Node {node.node_id} routing table updated (Link State)")
                logging.info(node.routing_table)
        else:
            raise ValueError("Invalid algorithm name")
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f"{algorithm} algorithm converged in {elapsed_time} seconds")

    def create_networkx_graph(self,num_nodes,num_edges):
        
        # Create nodes
        for _ in range(num_nodes):
            node_id = generate_random_node_id(self.nodes.keys())
            self.add_node(node_id)

        # Add edges between nodes
        node_ids = list(self.nodes.keys())
        for _ in range(num_edges):
            node1_id, node2_id = random.sample(node_ids, 2)
            cost = random.randint(1, 10)
            self.add_link(node1_id, node2_id, cost)  

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
        
        

    def send_packet(self, source_node_id, dest_node_id, data):
        current_node_id = source_node_id
        path_taken = [current_node_id]
        total_cost = 0

        while current_node_id != dest_node_id:
            next_hop_id = self.nodes[current_node_id].routing_table[dest_node_id][0]
            cost = self.nodes[current_node_id].neighbors[next_hop_id]
            total_cost += cost

            # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            #     client_socket.connect((self.emulator_host, self.emulator_port))
            #     client_socket.sendall(f"{current_node_id} -> {next_hop_id}".encode())
            #     response = client_socket.recv(1024)
            #     logging.info(response.decode())

            # Log the transmission step without using sockets
            logging.info(f"{current_node_id} -> {next_hop_id}")

            path_taken.append(next_hop_id)
            current_node_id = next_hop_id

        logging.info(f"Packet with data '{data}' sent from {source_node_id} to {dest_node_id} via path {path_taken} with total cost {total_cost}")

    def comparingAlgo(self, source_node_id, dest_node_id, data):
        results = {}
        for algorithm in ['distance_vector', 'link_state']:

            print(f"Running {algorithm} algorithm...")
            # Run the algorithm and get the convergence time
            convergence_time = self.run_algorithm(algorithm)

            # Measure the time before sending the packet
            start_time = time.time()

            # Call the send_packet method
            self.send_packet(source_node_id, dest_node_id, data)

            # Measure the time after sending the packet
            end_time = time.time()

            # Calculate the time difference and print the result
            elapsed_time = end_time - start_time

            results[algorithm] = {
            'elapsed_time': elapsed_time,
            'convergence_time': convergence_time
            }
            print(f"{algorithm} algorithm took {elapsed_time} seconds to send a packet from {source_node_id} to {dest_node_id} after converging in {convergence_time} seconds")
            logging.info(f"{algorithm} algorithm took {elapsed_time} seconds to send a packet from {source_node_id} to {dest_node_id} after converging in {convergence_time} seconds")

        return results
    
import random

def generate_random_node_id(existing_ids):
    while True:
        node_id = random.randint(1,2000)
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

    # Send a packet from node 1 to node 2
    source_node_id = 1
    dest_node_id = 2
    data = "Hello, world!"
    simulator.send_packet(source_node_id, dest_node_id, data)

    # Disrupt a link after the first packet is sent
    time.sleep(2)  # Wait 2 seconds to simulate the first packet being sent

    # Select random connected nodes to be disconnected
    node1_id, node2_id = get_random_connected_nodes(simulator)

    # Disrupt the link between the nodes
    simulator.disrupt_link(node1_id, node2_id, float('inf'))  # Set the cost to infinity to simulate link failure
    logging.info(f"Disrupted link between {node1_id} and {node2_id}")

    # Run the algorithms again to measure the time it takes to redefine the paths
    simulator.run_algorithm('distance_vector')
    simulator.run_algorithm('link_state')

    # Create a new NetworkX graph with the disrupted link
    G_disrupted = simulator.create_networkx_graph()

    # Visualize the disrupted graph
    simulator.visualize_graph(G_disrupted)

    # Send another packet from node 1 to node 2 after the link has been disrupted
    simulator.send_packet(source_node_id, dest_node_id, data)
