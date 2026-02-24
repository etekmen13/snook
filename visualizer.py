import networkx as nx
import matplotlib.pyplot as plt
import numpy as np



def create_graph(graph):
    np_matrix =np.array(graph.nieghbors)
    G=nx.from_numpy_array(np_matrix)
    return G


G1 = nx.complete_graph(3)
G2 = nx.complete_graph(4) 

G = nx.cartesian_product(G1, G2)

def visualize_graph(graph):

    coloring = nx.coloring.greedy_color(graph, strategy="largest_first")
    
    unique_colors = list(set(coloring.values()))

    color_map = plt.cm.get_cmap('tab20', len(unique_colors))

    node_colors = [color_map(unique_colors.index(coloring[node])) for node in G.nodes()]

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(graph, seed=42)
    nx.draw(graph, pos, with_labels=True, node_color=node_colors, node_size=500, font_size=10)

    plt.show()

visualize_graph(G)