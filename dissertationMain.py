import os
import networkx as nx
import random
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RandomGraphGeneratorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Random Graph Generator")

        # Create widgets
        self.label1 = tk.Label(master, text="Number of nodes:")
        self.label2 = tk.Label(master, text="Minimum number of edges:")
        self.label3 = tk.Label(master, text="Maximum number of edges:")
        self.entry1 = tk.Entry(master)
        self.entry2 = tk.Entry(master)
        self.entry3 = tk.Entry(master)
        self.button1 = tk.Button(master, text="Generate Graph", command=self.generate_graph)
        self.button2 = tk.Button(master, text="Load Graph", command=self.load_graph)
        self.button3 = tk.Button(master, text="Save Graph", command=self.save_graph)
        self.fig = plt.figure(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)

        # Pack widgets
        self.label1.pack()
        self.entry1.pack()
        self.label2.pack()
        self.entry2.pack()
        self.label3.pack()
        self.entry3.pack()
        self.button1.pack()
        self.button1.pack()
        self.button2.pack()
        self.canvas.get_tk_widget().pack()

    def generate_graph(self):
        n_nodes = int(self.entry1.get())
        n_edges_min = int(self.entry2.get())
        n_edges_max = int(self.entry3.get())
        n_edges = random.randint(n_edges_min, n_edges_max)

        G = nx.Graph()

        for i in range(n_nodes):
            G.add_node(i)

        for i in range(n_edges):
            node1 = random.randint(0, n_nodes-1)
            node2 = random.randint(0, n_nodes-1)
            while node1 == node2 or G.has_edge(node1, node2):
                node1 = random.randint(0, n_nodes-1)
                node2 = random.randint(0, n_nodes-1)
            cost = random.randint(1, 10)
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


        self.fig.clear()
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
        self.canvas.draw()

        #Add the save graph button after drawing the graph
        self.G = G  # Store the graph object in self.G for later use
        self.button3.pack()


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
