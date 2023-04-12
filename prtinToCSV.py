import csv
import os

def printToCSV(num_nodes, num_edges, distance_vector_elapsed, distance_vector_convergence, link_state_elapsed, link_state_convergence, output_file='results.csv'):
    file_exists = os.path.isfile(output_file)

    with open(output_file, 'a', newline='') as f:
        writer = csv.writer(f)

        # Write the header row if the file doesn't exist
        if not file_exists:
            writer.writerow(['Number of Nodes', 'Number of Edges', 'Distance Vector Latency', 'Distance Vector Convergence', 'Link-State Latency', 'Link-State Convergence'])

        # Write the data row
        writer.writerow([num_nodes, num_edges, distance_vector_elapsed, distance_vector_convergence, link_state_elapsed, link_state_convergence])

    print(f"Results have been appended to {output_file}")
