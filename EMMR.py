import networkx as nx
import matplotlib.pyplot as plt

# Creazione del grafo
G = nx.Graph()
G.add_edges_from([(1, 2), (2, 3), (3, 1)])

# Calcolo delle coordinate dei nodi
pos = nx.spring_layout(G)

# Stampa delle coordinate dei nodi
print("Coordinate dei nodi:")
for node, coordinates in pos.items():
    print(f"Nodo {node}: {coordinates}")

# Disegno del grafo utilizzando le coordinate calcolate
nx.draw(G, pos, with_labels=True)
plt.show()
