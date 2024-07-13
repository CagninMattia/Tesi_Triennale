from pulp import LpVariable, LpProblem, LpMinimize, lpSum
import random
import networkx as nx
import matplotlib.pyplot as plt
import re

# Parametri del problema
n = 5
p = 2

# Insieme dei siti da 1 a n
N = list(range(1, n+1))

# Dichiarazione delle variabili
# Inizializza le strutture dati per w_ij e c_ijkm
w_ij = {}
c_ijkm = {}

with open('valori.txt', 'r') as file:
    lines = file.readlines()
content = '\n'.join(lines)
# Processa w_ij
# Utilizza espressioni regolari per trovare la stringa w_ij: [ seguita da una serie di numeri e poi ]
pattern = r'w_ij:\s*\[([\d\s,]+)\]'
matches = re.findall(pattern, content)

if matches:
    # Trovato almeno un match
    numbers = matches[0].split()
    iterator = iter(numbers)  # Creazione di un iteratore per numbers
    w_ij = {(i, j): int(next(iterator)) for i in N for j in N}
    print("Valori w_ij:", w_ij)
else:
    print("Stringa 'w_ij: [' non trovata nel file.")
# Processa c_ijkm
pattern_c_ijkm = r'c_ijkm:\s*\[([\d\s,]+)\]'
matches_c_ijkm = re.findall(pattern_c_ijkm, content)

if matches_c_ijkm:
    # Trovato almeno un match per c_ijkm
    numbers_c_ijkm = matches_c_ijkm[0].split()
    iterator_c_ijkm = iter(numbers_c_ijkm)  # Creazione di un iteratore per numbers_c_ijkm
    c_ijkm = {(i, j, k, m): int(next(iterator_c_ijkm)) for i in N for j in N for k in N for m in N}
    print("Valori c_ijkm:", c_ijkm)
else:
    print("Stringa 'c_ijkm: [' non trovata nel file.")

x_ik = {(i, k): LpVariable(cat='Binary', name=f'x_{i}_{k}') for i in N for k in N}
S_i = {i: LpVariable(name=f'S_{i}') for i in N}
C_ijkm = {(i, j, k, m): (w_ij[i, j] * c_ijkm[i, j, k, m]) + (w_ij[j, i] * c_ijkm[j, i, m, k]) for i in N for j in N for k in N for m in N}

# Definizione del problema
prob = LpProblem("EMMR", LpMinimize)

# Vincolo (2)
prob += lpSum(x_ik[k, k] for k in N) == p

# Vincolo (3)
for i in N:
    for k in N:
        if i != k:
            prob += x_ik[i, k] <= x_ik[k, k]

# Vincolo (4)
for i in N:
    prob += lpSum(x_ik[i, k] for k in N) == 1

# Vincolo (5) - Le variabili x_ik sono binarie quindi non serve definire nulla

# Vincolo (6)
for i in N:
    for k in N:
        prob += S_i[i] >= lpSum((C_ijkm[i, j, k, m] * (x_ik[i, k] + x_ik[j, m] - 1)) for j in N if j > i for m in N)

# Vincolo (7)
for i in N:
    prob += S_i[i] >= 0

# Funzione obiettivo
prob += lpSum(S_i[i] for i in N)

# Risoluzione del problema
prob.solve()

# Stampa dei risultati
print("Valore della soluzione ottima:", prob.objective.value())
"""
print("Valori delle variabili x_ik:")
for i in N:
    for k in N:
        print(f"x_{i}_{k} =", x_ik[i, k].value())

print("Valori delle variabili w_ij:")
for i in N:
    for j in N:
        print(w_ij[i, j])

print("Valori delle variabili c_ijkm:")
for i in N:
    for j in N:
        for k in N:
            for m in N:
                print(c_ijkm[i, j, k, m])
"""
# Creazione del grafo
G = nx.Graph()

# Aggiunta dei nodi al grafo
for node in N:
    G.add_node(node)
"""
# Aggiunta degli archi casuali tra i nodi
for i in N:
    for j in N:
        if i != j:
            G.add_edge(i, j, color='black')
"""
# Ottieni gli indici dei nodi che sono hub dalla soluzione ottima
hub_nodes = []
for i in N:
    if any(x_ik[i, i].value() == 1 for k in N):
        hub_nodes.append(i)

# Aggiunta degli archi casuali tra i nodi
for i in hub_nodes:
    for j in hub_nodes:
        if i != j:
            G.add_edge(i, j, color='black')

# Aggiunta delle linee rosse tra gli hub e gli altri nodi se x_ij = 1 nella soluzione ottima
for node in hub_nodes:
    for other_node in N:
        if node != other_node:
            if x_ik[node, other_node].value() == 1 or x_ik[other_node, node].value() == 1:
                G.add_edge(node, other_node, color='red')

# Disegno del grafo
pos = nx.spring_layout(G)
edge_colors = [G[u][v]['color'] for u, v in G.edges()]

nx.draw_networkx_nodes(G, pos, node_color='blue')  # Nodi blu
nx.draw_networkx_edges(G, pos, edge_color=edge_colors)  # Archi colorati
nx.draw_networkx_nodes(G, pos, nodelist=hub_nodes, node_color='red')  # Hub rossi

# Etichette per i nodi
node_labels = {node: str(node) for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels=node_labels, font_color='white')

plt.axis('off')
plt.show()

# Apertura del file di testo in modalità scrittura
with open('valori.txt', 'w') as file:
    # Scrivi i valori di w_ij nel file di testo
    file.write("w_ij: [")
    conta = 0
    for i in N:
        for j in N:
            conta += 1
            file.write(str(w_ij[i, j]) + " ")
            # Vai a capo ogni 10 valori
            if conta % 30 == 0:
                file.write("\n")
    file.write("] \n")


    # Scrivi i valori di c_ijkm nel file di testo
    file.write("\n\nc_ijkm: [")
    conta = 0
    for i in N:
        for j in N:
            for k in N:
                for m in N:
                    conta += 1
                    file.write(str(c_ijkm[i, j, k, m]) + " ")
                    # Vai a capo ogni 10 valori
                    if conta % 30 == 0:
                        file.write("\n")
    file.write("] \n")

file.close()