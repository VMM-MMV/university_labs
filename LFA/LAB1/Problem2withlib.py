import networkx as nx
import matplotlib.pyplot as plt

data = {
    'S': ['A'],
    'A': ['S', 'B'],
    'B': ['C', 'B'],
    'C': ['A',]
}

G = nx.DiGraph()

for node, neighbors in data.items():
    G.add_edges_from((node, neighbor) for neighbor in neighbors)

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='gray', arrowsize=20)
plt.show()
