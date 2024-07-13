from pulp import LpVariable, LpProblem, LpMinimize, lpSum
import random

# Parametri del problema
n = 5
p = 2

# Insieme dei siti da 1 a n
N = list(range(1, n+1))

# Dichiarazione delle variabili
w_ij = {(i, j): random.randint(0, 10) if i != j else 0 for i in N for j in N}
c_ijkm = {(i, j, k, m): random.randint(0, 10) for i in N for j in N for k in N for m in N}
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
