import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import curve_fit
import math


"""

dans brown_coef.py on vérifie le caractère brownien de la trajectoire de la grosse particule en calculant les distribution des deplacements pour differents
pas de temps. Et en affichant la variance d'une distribution en fonction du pas de temps choisi

"""


# fonction modèle
def gauss(x, A, mu, sigma):
    return A / sigma * np.exp(-(x-mu)**2 / (2*sigma**2))

#Importation du fichier
filename_pos = "mvt_brown_pos.xlsx"
filename_time = "mvt_brown_time.xlsx"
df = pd.read_excel(filename_pos)
time = pd.read_excel(filename_time)
df = df.astype("float64")



vars = []
d_temps = []


# ici on calcul étant donné un pas de temps les positions de la particule pour chaque incrémentation du pas de temps
def resample_positions_with_time_df(pos_df: pd.DataFrame, time_df: pd.DataFrame, dt_uniform: float):
    # Build per-column time arrays + find common end time
    t_end = np.inf
    t_col_map = {}

    for col in pos_df.columns:
        t_col = time_df[col].to_numpy(dtype=float)
        x_col = pos_df[col].to_numpy(dtype=float)

        # on enlève les cellules vides
        mask = np.isfinite(t_col) & np.isfinite(x_col)
        t_col = t_col[mask]
        x_col = x_col[mask]

        if t_col.size < 2:
            raise ValueError(f"{col} trop petite")

        # l'orgine des temps est fixé à 0 s
        t_col = t_col - t_col[0]

        t_col_map[col] = (t_col, x_col)
        t_end = min(t_end, t_col[-1])   # on sauvegarde le temps a la fin pour chaque colone et on garde le plus petit

    # création de la nouvelle liste de temps avec le pas de temps constant
    # on s'arrète a t_end pour toutes les colonnes
    t_new = np.arange(0.0, t_end + 1e-12, dt_uniform)


    out = {"t": t_new}

    # calcule des position pour chaque pas de temps par interpolation
    for col in pos_df.columns:
        t_col, x_col = t_col_map[col]
        out[col] = np.interp(t_new, t_col, x_col)

    return pd.DataFrame(out)



for d in range(30,200):
    delta = []
    dt_uniform = d*0.001 # on fixe notre pas de temps
    data = resample_positions_with_time_df(df, time, dt_uniform) 
    data.iloc[:, 1:]    # on s'interesse uniquement au positions

    # on calcul les incrémentation pour chaque colonne avec le saut de temps approprié
    for col_name in data.columns:
        for i in range(0, data[col_name].size - d, 1):
            temp = data.loc[i+d, col_name]
            temp1 = data.loc[i, col_name]
            delta.append(temp - temp1)

    # creation de l'histogramme
    data_hist = np.array(delta)
    data_hist = data_hist[np.isfinite(data_hist)]
    n_bins = d*100                     
    counts, bin_edges = np.histogram(data_hist, bins=n_bins)

    # curve fit à la gaussienne
    bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])  # on prend le centre des bins pour les valeurs de x
    p_opt, p_cov = curve_fit(
        gauss,
        bin_centers,
        counts,
        p0=[counts.max(), data_hist.mean(), data_hist.std()]
    )

    # extraction des paramètres de la gaussienne
    mu = p_opt[1]
    sigma = p_opt[2]

    var = pow(sigma, 2)
    # on garde à chaque foix la variance et le pas de temps utilisé
    vars.append(var)
    d_temps.append(dt_uniform)


    # on affiche pour un pas de temps au choix la gaussienne
    if d==50:
        x_fit = np.linspace(bin_centers.min(), bin_centers.max(), 1000)
        plt.hist(data_hist, bins=n_bins)
        plt.plot(x_fit, gauss(x_fit, *p_opt), 'r')
        plt.axvline(x = mu + sigma, color='purple', linestyle='--', linewidth=2)
        plt.axvline(x = mu -sigma, color='purple', linestyle='--', linewidth=2)

        plt.xlabel('Déplacements')
        plt.ylabel('Ocurrences')
        plt.title('Histogram des déplacements pour dt = 0.05 s')
        plt.show()

   

def lin(x, a):
    return a*x


# regression linéaire variance en fonction du pas de temps
# coef_dir, ord_origine = np.polyfit(d_temps, vars, 1)
p_opt, p_cov = curve_fit(lin, d_temps, vars, 10000)
coef_dir = p_opt[0]
ord_origine = 0

plt.scatter(d_temps, vars, label="Data")

x_line = np.linspace(0, max(d_temps), 100)
y_line = coef_dir * x_line + ord_origine
plt.xlabel('dt')
plt.ylabel('variance')
plt.title('variance en fonction du pas de temps')
plt.xlim(0, max(d_temps))
plt.plot(x_line, y_line, color="red", label="Linear fit")
plt.legend()
plt.show()

print("slope =", coef_dir)
print("intercept =", ord_origine)

