import numpy as np
import random

class NeighborState:
    def __init__(self, magic_cube):
        self.magic_cube = magic_cube
        # self.size = magic_cube.size
        # self.magic_number = magic_cube.magic_number

    # Melakukan pencarian neighbor random
    def generate_neighbor(self):
        neighbor = self.magic_cube.cube.copy()

        size = self.magic_cube.size
        
        # Mencari random neighbor
        i1,j1,k1 = random.randint(0, size - 1), random.randint(0, size - 1), random.randint(0, size - 1)
        i2, j2, k2 = random.randint(0, size - 1), random.randint(0, size - 1), random.randint(0, size - 1)
        # Memastikan n1 dan n2 tidak sama
        while (i1, j1, k1) == (i2, j2, k2):
            i2, j2, k2 = random.randint(0, size - 1), random.randint(0, size - 1), random.randint(0, size - 1)

        # Menukar neighbor 
        neighbor[i1, j1, k1], neighbor[i2, j2, k2] = neighbor[i2, j2, k2], neighbor[i1, j1, k1] 

        return neighbor