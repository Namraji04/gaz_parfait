from itertools import combinations
import numpy as np
import pandas as pd
from part import Particule
import random as rd
import c_i

N = 100
T = 10

R = 1
m = 1
Temp = 400                  # Température en Kelvin
g = 98  # Gravité

def grav(p):
    p.v[1] -= g * dt
    p.r = p.r + p.v * dt


parts, dt, x_max, y_max = c_i.equilibre_homog(N, R, 50, 100, m, Temp)




# variables et fichiers pour stocker les données
data = []
data_columns = []
for i in range(N):
    data_columns.extend([f"X{i}", f"Y{i}"])

with open("params.txt", "w") as f:
    f.write(f"{x_max} {y_max} {dt} {T} {N}")
    for p in parts:
        f.write(f" {p.R}")


def coll_paroi(p):
    r_new = p.r + p.v * dt

    # Collision avec une paroi verticale
    if r_new[0] < p.R:  # Collision avec la paroi de gauche
        r_new[0] = p.R
        p.v[0] *= -1
        
    elif r_new[0] > x_max - p.R: # Collision avec la paroi de droite
        r_new[0] = x_max - p.R
        p.v[0] *= -1
        
    # Collision avec une paroi horizontale 
    if r_new[1] < p.R: # Collision avec la paroi du bas
        r_new[1] = p.R
        p.v[1] *= -1
        
    elif r_new[1] > y_max - p.R: # Collision avec la paroi du haut
        r_new[1] = y_max - p.R
        p.v[1] *= -1

    p.r = r_new



def coll_part(p1, p2):
    dr = p2.r - p1.r 
    norme_dr = np.linalg.norm(dr)

    if norme_dr <= p1.R + p2.R:
        # il y collision
        vcm = (p1.m * p1.v + p2.m * p2.v)/(p1.m + p2.m)

        u1 = p1.v - vcm
        u2 = p2.v - vcm

        n = dr/norme_dr

        u1n = u1 @ n
        u2n = u2 @ n

        p1.v -= 2*u1n*n
        p2.v -= 2*u2n*n


        overlap = (p1.R + p2.R) - norme_dr
        if overlap > 0:
            w1 = p2.m / (p1.m + p2.m)
            w2 = p1.m / (p1.m + p2.m)
            p1.r -= w1 * overlap * n
            p2.r += w2 * overlap * n        

# execution de la simulation
t = 0
while t <= T:
    row = {}
    for i in range(N):
        grav(parts[i])
        coll_paroi(parts[i])

    for a, b in combinations(parts, 2):
        coll_part(a, b)


    for i in range(N):
        row[f"X{i}"] = parts[i].r[0]
        row[f"Y{i}"] = parts[i].r[1]


    data.append(row)

    t += dt

#print("\033[H\033[J", end="")
print("creation d'excel chef")
# sauvegarde de données de positions
pd.DataFrame(data).to_excel("data.xlsx", index=False)

