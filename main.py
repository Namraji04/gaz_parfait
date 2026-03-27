from itertools import combinations
import numpy as np
import pandas as pd
from part import Particule
import random as rd
import c_i
import collision

N = 200
T = 10

R = 1
m = 1
Temp = 10000                  # Température en Kelvin

parts, dt, x_max, y_max = c_i.broooown(N, R, 100, 50, m, Temp)


# variables et fichiers pour stocker les données
data_pos = []
data_v_par = []

with open("params.txt", "w") as f:
    f.write(f"{x_max} {y_max} {dt} {T} {N}")
    for p in parts:
        f.write(f" {p.R}")



# execution de la simulation
t = 0
while t <= T:

    # affichage de la progression du calcul
    # if int(t)%5 == 1:
        # print("\033[H\033[J", end="")
    print(t)

    # verification des collisions
    for i in range(N):
        collision.coll_paroi(parts[i], data_v_par, dt, x_max, y_max)

    for a, b in combinations(parts, 2):
        collision.coll_part(a, b)


    # sauvegarde des positions dans data
    row = {}
    for i in range(N):
        row[f"X{i}"] = parts[i].r[0]
        row[f"Y{i}"] = parts[i].r[1]
    data_pos.append(row)

    t += dt

print("\033[H\033[J", end="")
print("creation des excels chef")

# sauvegarde de données de positions sous format excel
pd.DataFrame(data_pos).to_excel("data.xlsx", index=False)
pd.DataFrame(data_v_par).to_excel("data_press.xlsx", index=False)
