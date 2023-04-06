# as_simulator.py

import threading
import time
import heapq
from collections import defaultdict
import time

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

if __name__ == '__main__':
    simulator = AutonomousSystemSimulator()

    # Create nodes
    simulator.add_node('A')
    simulator.add_node('B')
    simulator.add_node('C')


    # Add links between nodes
    simulator.add_link('A', 'B', 1)
    simulator.add_link('B', 'C', 2)
    simulator.add_link('A', 'C', 4)

    # Run the Distance Vector algorithm
    print("Running Distance Vector algorithm")
    simulator.distance_vector_algorithm()

    # Run the Link State algorithm 
    print("Running Link State algorithm")
    simulator.link_state_algorithm()
