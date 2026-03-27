import anim
import heapq
from math import sqrt
import itertools
import numpy as np
import pandas as pd
from part import Particule
import sys
import c_i


"""

main_eff.py est la partie du code qui calcul la simulation de manière efficace. 
Elle basée sur le principe où l'on prédit la prochain collision qui aura lieu dans le système et où l'on avance la simulation collision par collision.
Pour cela une liste de 'Event' est créé qui garde toutes le collision potentiel et qui donne celle qui arrive en première.

"""




class Event:
    def __init__(self, temps, indices, coll):
        self.items = list(indices)
        self.t = temps.copy()
        self.coll_count = coll.copy()

    def show(self):
        print(f"{self.items}, {self.t}")




counter = itertools.count()
events = []

def push_event(event: Event):
    heapq.heappush(events, (event.t, next(counter), event))

def pop_event():
    _, _, event = heapq.heappop(events)
    return event



# cette fonction est appelé lorsqu'une collision particule/paroi a lieu
def coll_paroi_eff(i,t, coll_count, parts, N, y_max, x_max):
    # extraire pos et vitesse particule
    vy = parts[i].v[1]
    vx = parts[i].v[0]

    ry = parts[i].r[1]
    rx = parts[i].r[0]

    ev = None
    # collision paroi
    if vy < 0:
        t_col = (parts[i].R - ry)/vy
        ev1 = Event(t_col+t, [i, -3], [parts[i].colls, 0])
        ev = ev1
        push_event(ev)
    elif vy > 0:
        t_col = (y_max - parts[i].R - ry)/vy
        ev1 = Event(t_col+t, [i, -4], [parts[i].colls, 0])
        ev = ev1
        push_event(ev)

    if vx < 0:
        t_col = (parts[i].R - rx)/vx
        ev = Event(t_col+t, [i, -1], [parts[i].colls, 0])
        push_event(ev)
    elif vx > 0:
        t_col = (x_max - parts[i].R - rx)/vx
        ev = Event(t_col+t, [i, -2], [parts[i].colls, 0])
        push_event(ev)

    # collision partiucles
    for j  in range(N):
        if j==i:
            continue
        dr = parts[j].r - parts[i].r
        dv = parts[j].v - parts[i].v

        c = dr[0]**2 + dr[1]**2 - (parts[j].R + parts[i].R)**2
        b = 2 * dr @ dv
        a = dv[0]**2 + dv[1]**2

        D = b**2 - 4*a*c

        if a > 0 and b <= 0 and D >= 0:            # collision uniquement possible si b strictement inf 0
            t_col = (-b-sqrt(D))/(2*a)
            if t_col < 0:
                continue
            ev = Event(t_col+t, [i, j], [parts[i].colls, parts[j].colls])
            push_event(ev)
        


# cette fonction est appelé lorsqu'une collision particule/particule a lieu
def coll_part_eff(ind1, ind2,t, coll_count, parts, N, y_max, x_max):
    for i in [ind1, ind2]:
        coll_paroi_eff(i,t, coll_count, parts, N, y_max, x_max)


def init_events(parts, N, y_max, x_max):
    t=0
    for i in range(N):
        # extraire pos et vitesse particule
        vy = parts[i].v[1]
        vx = parts[i].v[0]

        ry = parts[i].r[1]
        rx = parts[i].r[0]

        ev = None
        # collision paroi
        if vy < 0:
            t_col = (parts[i].R - ry)/vy
            ev1 = Event(t_col+t, [i, -3], [0,0])
            ev = ev1
            push_event(ev)
        elif vy > 0:
            t_col = (y_max - parts[i].R - ry)/vy
            ev1 = Event(t_col+t, [i, -4], [0,0])
            ev = ev1
            push_event(ev)

        if vx < 0:
            t_col = (parts[i].R - rx)/vx
            ev = Event(t_col+t, [i, -1], [0,0])
            push_event(ev)
        elif vx > 0:
            t_col = (x_max - parts[i].R - rx)/vx
            ev = Event(t_col+t, [i, -2], [0,0])
            push_event(ev)
      
        
        for j in range(i+1, N):
            # collision partiucles
            dr = parts[j].r - parts[i].r
            dv = parts[j].v - parts[i].v

            c = dr[0]**2 + dr[1]**2 - (parts[j].R + parts[i].R)**2
            b = 2 * dr @ dv
            a = dv[0]**2 + dv[1]**2

            D = b**2 - 4*a*c
            
            if a > 0 and b <= 0 and D >= 0:
                t_col = (-b-sqrt(D))/(2*a)
                if t_col < 0:
                    continue
                ev = Event(t_col+t, [i, j], [0,0])
                push_event(ev)



# fonction pour simulation et animation
def calc_simulation(x_max, y_max, T, N, parts):

    # variables pour stocker les données
    data_pos = []

    init_events(parts, N, y_max, x_max)


    # initialiser liste des evenements
    t = 0
    while t <= T:

        ev = pop_event()

        # on verifie d'abord si le event n'est pas obselete
        if ev.coll_count[0] == parts[ev.items[0]].colls and (ev.items[1] < 0 or ev.coll_count[1] == parts[ev.items[1]].colls):
            dt = ev.t - t
            
            # affichage de la progression du calcul
            t += dt
            print(f"time: {t}")

            row = {}
            row[f"time"] = t
            for i in range(N):
                parts[i].r += parts[i].v * dt
                row[f"X{i}"] = parts[i].r[0]
                row[f"Y{i}"] = parts[i].r[1]
            data_pos.append(row)

            
            # changements des vitesses des particules en collision
            ind1 = min(ev.items)
            ind2 = max(ev.items)
            if ind1 < 0:      # collision paroie
                if ind1 >= -2:    #gauche ou droite
                    parts[ind2].v[0] *= -1
                    parts[ind2].colls +=1
                else:                   # haut et bas
                    parts[ind2].v[1] *= -1
                    parts[ind2].colls +=1

                # predire prochaines collisions et ajouter a evenement
                coll_paroi_eff(ind2, t, ev.coll_count, parts, N, y_max, x_max)
            else:                   # dans ce cas la collision est entre particules
                p1 = parts[ind1]
                p2 = parts[ind2]

                dr = p2.r - p1.r 
                norme_dr = np.linalg.norm(dr)

                vcm = (p1.m * p1.v + p2.m * p2.v)/(p1.m + p2.m)

                u1 = p1.v - vcm
                u2 = p2.v - vcm

                n = dr/norme_dr

                u1n = u1 @ n
                u2n = u2 @ n

                # on change les vitesses
                p1.v -= 2.0*u1n*n
                p2.v -= 2.0*u2n*n

                p1.colls += 1
                p2.colls += 1

                # predire prochaines collisions
                coll_part_eff(ind1, ind2, t, ev.coll_count, parts, N, y_max, x_max)


    print("préparation des animations")

    R = [p.R for p in parts]
    anim.anim_direct(x_max, y_max, R, dt, T, N, data_pos)
    return data_pos




# calcul de la simulation pour le mouvement brownien
def calc_simulation_brown(x_max, y_max, T, N, parts):

    # variables pour stocker les données
    data_pos = []

    init_events(parts, N, y_max, x_max)


    # initialiser liste des evenements
    t = 0
    t_prev_col_big = 0
    while t <= T:

        ev = pop_event()

        # on verifie d'abord si l'évenement est obselete
        if ev.coll_count[0] == parts[ev.items[0]].colls and (ev.items[1] < 0 or ev.coll_count[1] == parts[ev.items[1]].colls):
            dt = ev.t - t
            
            t += dt

            for i in range(N):
                parts[i].r += parts[i].v * dt

            # on enregesitre que quand grosse particule et que quand il y a collision
            if 0 in ev.items:
                row = {}
                row[f"time"] = t
                t_prev_col_big = t
                row[f"X0"] = parts[0].r[0]
                row[f"Y0"] = parts[0].r[1]
                data_pos.append(row)

            
            # changer les vitesses des particules en collision
            ind1 = min(ev.items)
            ind2 = max(ev.items)
            if ind1 < 0:      # collision paroie
                if ind1 >= -2:    #gauche ou droite
                    parts[ind2].v[0] *= -1
                    parts[ind2].colls +=1
                else:                   # haut et bas
                    parts[ind2].v[1] *= -1
                    parts[ind2].colls +=1

                # predire prochaines collisions et ajouter a evenement
                coll_paroi_eff(ind2, t, ev.coll_count, parts, N, y_max, x_max)
            else:                   # dans ce cas la collision est entre deux partiucles
                p1 = parts[ind1]
                p2 = parts[ind2]

                dr = p2.r - p1.r 
                norme_dr = np.linalg.norm(dr)

                vcm = (p1.m * p1.v + p2.m * p2.v)/(p1.m + p2.m)

                u1 = p1.v - vcm
                u2 = p2.v - vcm

                n = dr/norme_dr

                u1n = u1 @ n
                u2n = u2 @ n

                # on change les vitesses
                p1.v -= 2.0*u1n*n
                p2.v -= 2.0*u2n*n

                p1.colls += 1
                p2.colls += 1

                # predire prochaines collisions
                coll_part_eff(ind1, ind2, t, ev.coll_count, parts, N, y_max, x_max)

    return data_pos

