import numpy as np


"""

ici on définit ce qu'est une particule


"""


class Particule:
    
    def __init__(self):
        self.r = np.array([0.5, 0.5])
        self.v = np.asarray([0.9, 0.9], dtype=float)
        self.m = pow(10, -27)
        self.R = 0.05
        self.colls = 0


    def update(self, dt):
        self.r += self.v * dt


