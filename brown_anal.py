from main_eff import calc_simulation_brown
import c_i

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


"""

dans brown_anal.py on calcul et on affiche la trajectoire totale d'une particule qui suit un mouvement brownien

"""


N = 300
T = 100

R = 1
m = 1
Temp = 300                  # Température en Kelvin

R_grosse = 100

# initialisation du système
parts, x_max, y_max = c_i.broooown(N, 10, 10, Temp, R, m, R_grosse)


# calcul de la simulaiton
data = calc_simulation_brown(x_max, y_max, T, N, parts)
df = pd.DataFrame(data)

# trajectoire de la particule centrale
x = df["X0"].to_numpy()
y = df["Y0"].to_numpy()

# déplacement par rapport à la position initiale
dx = x - x[0]
dy = y - y[0]
r = np.sqrt(dx**2 + dy**2)

# Mouvement Brownien    
plt.figure(figsize=(7,7))
plt.plot(x, y)
plt.scatter([x[0]], [y[0]], marker="o")      # départ
plt.scatter([x[-1]], [y[-1]], marker="x")    # arrivée
plt.xlabel("x")
plt.ylabel("y")
plt.title("Trajectoire de la particule centrale (X0,Y0)")
plt.show()

