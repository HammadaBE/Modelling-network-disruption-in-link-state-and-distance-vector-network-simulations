import os
import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from PIL import  ImageTk 
import PIL.Image
from tkinter import *
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import csv
import utils

class RandomGraphGeneratorGUI:
    def __init__(self, master):
        self.master = master
        master.geometry("1200x900")
        master.title("Random Graph Generator")

        

        # Load the background image
        bg_image = PIL.Image.open('worldNetwork.jpg')
        bg_image = bg_image.resize((1200, 900), PIL.Image.ANTIALIAS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        
        # Create a Label object with the background image
        self.bg_label = tk.Label(master, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1) # Set the Label to fill the entire window
        

        # Create widgets
        self.label1 = tk.Label(master, text="Number of nodes:")
        self.label2 = tk.Label(master, text="Number of edges:")
        #self.label3 = tk.Label(master, text="Maximum number of edges:")
        # self.label4 = tk.Label(master, text="Bellman-Ford time:" )
        # self.label5 = tk.Label(master, text="Djisktra time:" )
        self.entry1 = tk.Entry(master)
        self.entry2 = tk.Entry(master)
        #self.entry3 = tk.Entry(master)
        self.button1 = tk.Button(master, text="Generate Graph", command=self.generate_graph)
        #self.button2 = tk.Button(master, text="Disrupt path", command=self.disrupt_path)
        self.button3 = tk.Button(master, text="Load Graph", command=self.load_graph)
        self.button4 = tk.Button(master, text="Save Graph", command=self.save_graph)
        #self.button5 = tk.Button(master, text="Build Routing Table", command=self.build_routing_table)
        self.fig = plt.figure(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)

        # Pack widgets
        self.label1.place(x=30, y=20)
        self.entry1.place(x=30, y=50)
        self.label2.place(x=200, y=20)
        self.entry2.place(x=200, y=50)
        #self.label3.place(x=400, y=20)
        #self.entry3.place(x=400, y=50)
        self.button1.place(x=600, y=20)
        #self.button2.place(x=700, y=20)
        self.button3.place(x=800, y=20)
        #self.button5.place(x=800, y=50)
        self.canvas.get_tk_widget().place(x=100, y=150)

    def generate_graph(self):
        n_nodes = int(self.entry1.get())
        n_edges = int(self.entry2.get())
        #n_edges_max = int(self.entry3.get())
        #n_edges = random.randint(n_edges_min, n_edges_max)

        G = nx.Graph()

        for i in range(n_nodes):
            G.add_node(i)

        for i in range(n_edges):
            node1 = random.randint(0, n_nodes-1)
            node2 = random.randint(0, n_nodes-1)
            while node1 == node2 or G.has_edge(node1, node2):
                node1 = random.randint(0, n_nodes-1)
                node2 = random.randint(0, n_nodes-1)
            #cost = random.randint(1, 10)
            cost=1
            G.add_edge(node1, node2, weight=cost)

        for node in G.nodes:
            if G.degree(node) == 0:
                connected_node = random.choice(list(G.nodes))
                while connected_node == node:
                    connected_node = random.choice(list(G.nodes))
                cost = random.randint(1, 10)
                G.add_edge(node, connected_node, weight=cost)

        #Store a graph for reusabulity
        #nx.write_gml(G, "mygraph.gml")

        

        # Apply Bellman-Ford and Dijkstra's algorithms
        start_node = 0
        end_node = n_nodes - 1
        start_time = time.time()
        bf_dist = nx.bellman_ford_path(G,target=end_node, source=start_node, weight='weight')
        bf_time = time.time() - start_time

        start_time = time.time()
        djk_dist = nx.dijkstra_path(G,target=end_node, source=start_node, weight='weight')
        djk_time = time.time() - start_time

        # Measure packet arrival time
        packet_speed = 1  # Distance covered by packet per second
        packet_path = nx.shortest_path(G, source=start_node, target=end_node, weight='weight')
        packet_distance = nx.shortest_path_length(G, source=start_node, target=end_node, weight='weight')
        packet_arrival_time = packet_distance / packet_speed

        # Print results
        print("Bellman-Ford distance:", bf_dist)
        print("Bellman-Ford time:", bf_time)
        print("Dijkstra distance:", djk_dist)
        print("Dijkstra time:", djk_time)
        print("Packet path:", packet_path)
        print("Packet arrival time:", packet_arrival_time, "seconds")



        # Draw graph
        self.fig.clear()
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
        nx.draw_networkx_edges(G, pos, edgelist=[(packet_path[i], packet_path[i+1]) for i in range(len(packet_path)-1)],
                               edge_color='r', width=2)
        self.canvas.draw()

        # Add the save graph button after drawing the graph
        self.G = G  # Store the graph object in self.G for later use
        self.button4.place(x=900, y=20)
        # self.label4.place(x=1000, y=20)
        # self.label5.place(x=1000, y=60)
   
        #utils.distance_vector_algorithm_time(G, source=0)
        DVlatency =utils.distance_vector_algorithm_time(G, source=0)
        #utils.link_state_algorithm_time(G, source=0)
        LSlatency=utils.link_state_algorithm_time(G, source=0)


        # Create a new window to show the results
        result_window = Toplevel(self.master)
        result_window.title("Results")

        # Create labels to display the results
        # bf_dist_label = Label(result_window, text="Bellman-Ford distance: " + str(bf_dist))
        bf_time_label = Label(result_window, text="Bellman-Ford time: " + str(bf_time))
        # djk_dist_label = Label(result_window, text="Dijkstra distance: " + str(djk_dist))
        djk_time_label = Label(result_window, text="Dijkstra time: " + str(djk_time))
        path_label = Label(result_window, text="Packet path: " + str(packet_path))
        arrival_time_label = Label(result_window, text="Packet arrival time: " + str(packet_arrival_time) + " seconds")
        DV_time_label = Label(result_window, text="Distance Vector latency: " + str(DVlatency) + " seconds")
        LS_time_label = Label(result_window, text="Link State latency: " + str(LSlatency) + " seconds")

        # Pack the labels in the window
        # bf_dist_label.pack()
        bf_time_label.pack()
        # djk_dist_label.pack()
        djk_time_label.pack()
        path_label.pack()
        arrival_time_label.pack()
        DV_time_label.pack()
        LS_time_label.pack()

        
        # Create a list of data
        data = [
            [n_nodes],
            [n_edges],
            [bf_time],
            [djk_time],
            [packet_path],
            [packet_arrival_time],
            [DVlatency],
            [LSlatency]
        ]

        # Transpose the data to switch rows by columns
        data_transposed = list(zip(*data))

        # Create a new CSV file and write the data to it
        with open('result.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            for row in data_transposed:
                writer.writerow(row)

        # Initialize a routing table dictionary
        routing_table = {}

        # Calculate the shortest paths between each pair of nodes in the graph
        all_shortest_paths = dict(nx.all_pairs_dijkstra_path(G))

        # For each node in the graph, add its routing table entry
        for src in G.nodes():
            routing_table[src] = {}

            # For each destination node in the graph, add the shortest path to the routing table
            for dest in G.nodes():
                if src == dest:
                    continue  # Skip adding the shortest path to itself
                shortest_path = all_shortest_paths[src][dest]
                next_hop = shortest_path[1]
                routing_table[src][dest] = next_hop

        print(routing_table)
        #utils.distance_vector_algorithm(G, source=0)
        
        
    # def disrupt_path(self):
    #     # Get the graph G from the canvas
    #     G_array = self.fig.axes[0].collections[0].get_paths()[0].to_polygons()[0]
    #     n_vertices = len(G_array)
    #     G_array = np.asarray(G_array)
    #     # Create an empty n x n adjacency matrix
    #     A = np.zeros((n_vertices, n_vertices))
    #     # Compute the Euclidean distances between each pair of vertices
    #     for i in range(n_vertices):
    #         for j in range(i+1, n_vertices):
    #             dist = np.linalg.norm(G_array[i] - G_array[j])
    #             A[i,j] = dist
    #             A[j,i] = dist
    #     # Create a graph from the adjacency matrix using the from_numpy_array function
    #     G = nx.from_numpy_array(A, create_using=nx.Graph())
    #     # Choose a random edge to remove
    #     edge = random.choice(list(G.edges()))
    #     # Remove the edge from the graph
    #     G.remove_edge(*edge)
    #     # Recompute shortest path using Dijkstra's algorithm
    #     start_node = 0
    #     end_node = len(G.nodes) - 1
    #     djk_dist = nx.dijkstra_path(G, source=start_node, target=end_node, weight='weight')
    #      # Recompute shortest path using Bellman-Ford algorithm
    #     bf_dist = nx.bellman_ford_path_length(G, source=start_node, weight='weight')
    #     # Print disrupted path distance for both algorithms
    #     print("Disrupted path distance using Dijkstra:", djk_dist)
    #     print("Disrupted path distance using Bellman-Ford:", bf_dist)
    #     # Redraw the graph with updated edge labels
    #     self.fig.clear()
    #     pos = nx.spring_layout(G)
    #     nx.draw(G, pos, with_labels=True)
    #     nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
    #     nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color='r', width=2)
    #     self.canvas.draw()

    

    # def build_routing_table(G):
    #     # Initialize a routing table dictionary
    #     routing_table = {}

    #     # Calculate the shortest paths between each pair of nodes in the graph
    #     all_shortest_paths = dict(nx.all_pairs_dijkstra_path(G))

    #     # For each node in the graph, add its routing table entry
    #     for src in G.nodes():
    #         routing_table[src] = {}

    #         # For each destination node in the graph, add the shortest path to the routing table
    #         for dest in G.nodes():
    #             if src == dest:
    #                 continue  # Skip adding the shortest path to itself
    #             shortest_path = all_shortest_paths[src][dest]
    #             next_hop = shortest_path[1]
    #             routing_table[src][dest] = next_hop

    #     return routing_table

   

    def save_graph(self):
        initial_dir = os.path.expanduser("./savedGraphs")  
        filename = filedialog.asksaveasfilename(defaultextension=".graphml", initialdir=initial_dir)
        if filename:
            nx.readwrite.write_graphml(self.G, filename)
        

    def load_graph(self):
        filename = filedialog.askopenfilename(title="Select graph file", filetypes=[("Graph files", "*.gml;*.graphml;*.json;*.yaml;*.edgelist")])
        if filename:
            G = nx.readwrite.read_graphml(filename)
            self.fig.clear()
            pos = nx.spring_layout(G)
            nx.draw(G, pos, with_labels=True)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
            self.canvas.draw()

    



root = tk.Tk()
app = RandomGraphGeneratorGUI(root)
root.mainloop()



