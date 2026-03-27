import numpy as np



def coll_paroi(p, data_speed, dt, x_max, y_max):
    r_new = p.r + p.v * dt

    # Collision avec une paroi verticale
    if r_new[0] < p.R:  # Collision avec la paroi de gauche
        n_v = np.linalg.norm(p.v)
        data_speed.append(n_v)
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
    overlap = (p1.R + p2.R) - norme_dr

    # if norme_dr <= p1.R + p2.R:
    if overlap >= 0:
        # il y collision
        vcm = (p1.m * p1.v + p2.m * p2.v)/(p1.m + p2.m)

        u1 = p1.v - vcm
        u2 = p2.v - vcm

        n = dr/norme_dr

        u1n = u1 @ n
        u2n = u2 @ n

        # on change les vitesses
        p1.v -= 2*u1n*n
        p2.v -= 2*u2n*n

        # on change les positions (pour eviter qu'ils se chevauchent)
        w1 = p2.m / (p1.m + p2.m)
        w2 = p1.m / (p1.m + p2.m)
        p1.r -= w1 * overlap * n
        p2.r += w2 * overlap * n  



