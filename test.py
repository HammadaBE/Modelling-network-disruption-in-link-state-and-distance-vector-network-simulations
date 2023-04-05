import networkx as nx
import random
import time

# Create a random network topology
def generate_network_topology(n_nodes, n_edges):
    G = nx.Graph()
    nodes = list(range(1, n_nodes + 1))
    G.add_nodes_from(nodes)

    for _ in range(n_edges):
        u = random.choice(nodes)
        v = random.choice(nodes)
        weight = random.randint(1, 10)
        G.add_edge(u, v, weight=weight)

    return G

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

# Example usage
G = generate_network_topology(100, 200)
source = 1

# Calculate the latency for distance-vector and link-state algorithms
start_time = time.perf_counter()
distance_vector_result = distance_vector_algorithm(G, source)
distance_vector_latency = time.perf_counter() - start_time
print("Distance-vector result:", distance_vector_result)
print("Distance-vector latency:", distance_vector_latency)

start_time = time.perf_counter()
link_state_result = link_state_algorithm(G, source)
link_state_latency = time.perf_counter() - start_time
print("Link-state result:", link_state_result)
print("Link-state latency:", link_state_latency)
