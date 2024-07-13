import random

# Definisco numero di siti
n = 45

# Insieme dei siti da 1 a n
N = list(range(1, n+1))

w_ij = {(i, j): random.randint(0, 10) if i != j else 0 for i in N for j in N}
c_ijkm = {(i, j, k, m): random.randint(0, 10) for i in N for j in N for k in N for m in N}

# Apertura del file di testo in modalità scrittura
with open(f'valori_{n}.txt', 'w') as file:
    # Scrivi i valori di w_ij nel file di testo
    file.write("w_ij: [")
    conta = 0
    for i in N:
        for j in N:
            conta += 1
            file.write(str(w_ij[i, j]) + " ")
            # Vai a capo ogni 30 valori
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
                    # Vai a capo ogni 30 valori
                    if conta % 30 == 0:
                        file.write("\n")
    file.write("] \n")

file.close()
