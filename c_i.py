import numpy as np
import random as rd
from part import Particule

"""

dans c_i.py on définit les différents condition initiales. On distingue broooown dans le cas du mouvement brownien
ou une particule doite etre pus grosse. Ou encore equilibre homogene, 
dans le cas général ou l'on veut démarer la simulation à l'équilibre

"""

def broooown(N, rayons_boite_x, rayons_boite_y, Temp, R, m, R_grosse = 15, m_grosse = 50):

    x_max, y_max = rayons_boite_x*R_grosse, rayons_boite_y*R_grosse
    k_B = 100             # Constante de Boltzman

    # creation des partiucles
    print("Creation des particules")

    parts = []
    positions = np.zeros((N,2))
    rayons = np.zeros(N)

    sigma = np.sqrt(k_B * Temp / m)
    v_x = np.random.normal(0, sigma, N)
    v_y = np.random.normal(0, sigma, N)

    for i in range(N):
        
        p = Particule()
        
        # La grosse en premier 
        if i == 0:
            p.R = R_grosse
            p.m = m if m_grosse is None else m_grosse
            
            a = np.array([x_max / 2.0, y_max / 2.0], dtype=float)
            
            p.r = a
            p.v = np.array([0.0, 0.0], dtype=float)
            
            positions[0] = a
            rayons[0] = p.R
            
        #Le reste
        else:
            p.R = R
            p.m = m
            
            a = np.array([rd.uniform(p.R, x_max - p.R), rd.uniform(p.R, y_max - p.R)], dtype=float)
            
            dists = [np.linalg.norm(a - positions[j]) - p.R - rayons[j] for j in range(i)]

            m_min = min(dists)
            
            while m_min <= 0:
                a = np.array([rd.uniform(p.R, x_max - p.R), rd.uniform(p.R, y_max - p.R)], dtype=float)
                dists = [np.linalg.norm(a - positions[j]) - p.R - rayons[j] for j in range(i)]
                
                m_min = min(dists)
                
            positions[i] = a
            rayons[i] = p.R
            
            p.r = a
            p.v = np.array([v_x[i], v_y[i]], dtype=float)
            
        parts.append(p)
        
    
    return parts, x_max, y_max



def equilibre_homog(N, R, rayons_boite_x, rayons_boite_y, m, Temp):

    x_max, y_max = rayons_boite_x*R, rayons_boite_y*R
    k_B = 100              # Constante de Boltzman

    # creation des partiucles
    print("creation des particules")

    parts = []
    positions = np.zeros((N,2))

    sigma = np.sqrt(k_B * Temp / m)
    v_x = np.random.normal(0, sigma, N)
    v_y = np.random.normal(0, sigma, N)

    for i in range(N):
        
        p = Particule()
        
        p.R = R
        
        if i==0:
            a = np.array([rd.uniform(p.R, x_max - p.R), rd.uniform(p.R, y_max - p.R)])
            positions[0] = a
            p.r = a
        else:
            a = np.array([rd.uniform(p.R, x_max - p.R), rd.uniform(p.R, y_max - p.R)])
            m = [np.linalg.norm(a - q) for q in positions]
            m_min = min(m)
            
            while m_min <= 2*p.R:
                a = np.array([rd.uniform(p.R, x_max - p.R), rd.uniform(p.R, y_max - p.R)])
                m = [np.linalg.norm(a - q) for q in positions]
                m_min = min(m)
                
            positions[i] = a
            p.r = a
        
        p.v = np.array([v_x[i], v_y[i]])
        
        parts.append(p)

    # on calcul le pas de temps par rapport au rayon et la vitesse moyenne
    n_vitesses = [np.linalg.norm(p.v) for p in parts]
    n_v_mean = np.mean(n_vitesses)
    n_v_sigma = np.std(n_vitesses)
    v_repr = n_v_mean + n_v_sigma
    dt = R/(2*v_repr)

    return parts, dt, x_max, y_max



# autre fonction a faire encore
def debug_simu(N, rayons_boite_x, rayons_boite_y,  R_grosse = 15, m_grosse = 50):
    # creation des partiucles
 
    x_max = rayons_boite_x
    y_max = rayons_boite_y

    parts = []

    for i in range(N):
        p = Particule()


        if i==0:
            p.r = np.array([53.69995712, 34.09581237])
            p.v = np.array([57.43773096, -113.77224581])
            p.R = 1
            p.m = 1
            parts.append(p)

        if i==1:
            p.r = np.array([50., 25.])
            p.v = np.array([0.0, 0.0])
            p.R = R_grosse
            p.m = m_grosse
            parts.append(p)

    dt = 0.01

    return parts, dt, x_max, y_max


