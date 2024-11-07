import numpy as np
import random
from cube.magic_cube import MagicCube

class NeighborState:
    def __init__(self, magic_cube):
        self.magic_cube = magic_cube
        # self.size = magic_cube.size
        # self.magic_number = magic_cube.magic_number

    # Memilih dua posisi acak berbeda
    def select_random_positions(self):
        # Mencari random posisi
        i1, j1, k1 = random.randint(0, self.magic_cube.size - 1), random.randint(0, self.magic_cube.size - 1), random.randint(0, self.magic_cube.size - 1)
        i2, j2, k2 = random.randint(0, self.magic_cube.size - 1), random.randint(0, self.magic_cube.size - 1), random.randint(0, self.magic_cube.size - 1)
        
        # Memastikan posisi 1 dan posisi 2 tidak sama
        while (i1, j1, k1) == (i2, j2, k2):
            i2, j2, k2 = random.randint(0, self.magic_cube.size - 1), random.randint(0, self.magic_cube.size - 1), random.randint(0, self.magic_cube.size - 1)
        
        return i1, j1, k1, i2, j2, k2

    # Melakukan pencarian neighbor random
    def generate_neighbor(self):
        neighbor = MagicCube(size=self.magic_cube.size)
        neighbor.cube = self.magic_cube.cube.copy()

        i1, j1, k1, i2, j2, k2 = self.select_random_positions()

        # Menukar neighbor 
        neighbor.cube[i1, j1, k1], neighbor.cube[i2, j2, k2] = neighbor.cube[i2, j2, k2], neighbor.cube[i1, j1, k1] 
        
        return neighbor
    
