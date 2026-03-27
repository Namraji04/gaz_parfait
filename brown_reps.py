import pandas as pd
import numpy as np
import c_i
from main_eff import calc_simulation_brown

"""

dans brown_reps.py on répete un certain nombre de foix la simulation d'un mouvement brownien en gardant uniquement les positionts et leurs temps associés

"""

N = 300         # nombre de particules
T = 200          # temps

R = 1           # rayon petite partiucle
m = 1           # masse petite particule
Temp = 300                  # Température en Kelvin

R_grosse = 50  # rayon grosse particule

# variables et fichiers pour stocker les données
data_pos = {}
lengths = []
times = {}

rep = 10        # nombre de répetitions



# execution de la simulation
for i in range(rep):
    print(f"C'est la simulation {i+1}/{rep}")
    parts, x_max, y_max = c_i.broooown(N, 10, 10, Temp, R, m, R_grosse)
    
    # execution simulation avec extraction données grosse part
    data = calc_simulation_brown(x_max, y_max, T, N, parts)

    data_pos[f"X{i}"] = [row["X0"] for row in data]
    data_pos[f"Y{i}"] = [row["Y0"] for row in data]
    times[f"X{i}"] = [row["time"] for row in data]
    times[f"Y{i}"] = [row["time"] for row in data]
    lengths.append(len(data))   # number of rows
        

# pour toutes les colonnes de data_pos ai la meme taille
max_len = max(lengths)
for k, v in data_pos.items():
    if len(v) < max_len:
        data_pos[k] = v + [np.nan] * (max_len - len(v))

# pour que toutes les colonnes de times ai la meme taille
max_len = max(lengths)
for k, v in times.items():
    if len(v) < max_len:
        times[k] = v + [np.nan] * (max_len - len(v))


pos_new = pd.DataFrame(data_pos)    
time_new = pd.DataFrame(times)    
# sauvegarde de données sous format excel
pos_new.to_excel("mvt_brown_pos.xlsx", index=False)
time_new.to_excel("mvt_brown_time.xlsx", index=False)
