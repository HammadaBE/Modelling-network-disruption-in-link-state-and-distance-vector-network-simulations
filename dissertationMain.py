import networkx as nx
import random
import matplotlib.pyplot as plt

# Set the number of nodes and edges
n_nodes = random.randint(5, 20)
n_edges = random.randint(n_nodes-1, (n_nodes*(n_nodes-1))/2)

# Create an empty graph
G = nx.Graph()

for i in range(n_nodes):
    G.add_node(i)

# Add random edges to the graph with random weights
for i in range(n_edges):
    node1 = random.randint(0, n_nodes-1)
    node2 = random.randint(0, n_nodes-1)
    while node1 == node2 or G.has_edge(node1, node2):
        node1 = random.randint(0, n_nodes-1)
        node2 = random.randint(0, n_nodes-1)
    cost = random.randint(1, 10)
    G.add_edge(node1, node2, weight=cost)

# Add edges to nodes with no connections
for node in G.nodes:
    if G.degree(node) == 0:
        connected_node = random.choice(list(G.nodes))
        while connected_node == node:
            connected_node = random.choice(list(G.nodes))
        cost = random.randint(1, 10)
        G.add_edge(node, connected_node, weight=cost)

# Print the number of nodes, edges, and the graph
print(f"Number of nodes: {len(G.nodes)}")
print(f"Number of edges: {len(G.edges)}")
print("Graph: ")
print(G.edges(data=True))

# Draw the graph
pos = nx.spring_layout(G)
nx.draw(G, pos)
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
plt.show()
