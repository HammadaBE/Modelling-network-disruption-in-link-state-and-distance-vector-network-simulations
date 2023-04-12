import os
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from PIL import  ImageTk 
import PIL.Image
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import csv
import as_simulator as as_sim
import prtinToCSV as printer


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
        self.toolbar = NavigationToolbar2Tk(self.canvas, root) 

    

    
    global simulator
    simulator = as_sim.AutonomousSystemSimulator()

    
    

    def generate_graph(self):

       
        n_nodes = int(self.entry1.get())
        n_edges = int(self.entry2.get())
        
        G=simulator.create_networkx_graph(n_nodes,n_edges)
        simulator.visualize_graph(G)
        
        
        self.toolbar.update()
        self.canvas.draw()
        
        first_node = list(G.nodes)[0]  # Get the first node
        last_node = list(G.nodes)[-1]  # Get the last node

        results=simulator.comparingAlgo(first_node,last_node,"Hello World")
        distance_vector_elapsed = results['distance_vector']['elapsed_time']
        distance_vector_convergence = results['distance_vector']['convergence_time']
        link_state_elapsed = results['link_state']['elapsed_time']
        link_state_convergence = results['link_state']['convergence_time']
        
        # Call the print_results function to save the data to a CSV file
        printer.printToCSV(n_nodes, n_edges, distance_vector_elapsed, distance_vector_convergence,link_state_elapsed,link_state_convergence)

   

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
# set minimum window size value
root.minsize(1200,900)
# set maximum window size value
root.maxsize(1200,900) 
root.mainloop()



