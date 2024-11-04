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

        # Mencari random neighbor
        n1 = (random.randint(0, self.magic_cube.size - 1 ), 
              random.randint(0, self.magic_cube.size - 1), 
              random.randint(0, self.magic_cube.size - 1))
        
        n2 = (random.randint(0, self.magic_cube.size -1 ),
              random.randint(0, self.magic_cube.size - 1),
              random.randint(0, self.magic_cube.size - 1))
        
        # Memastikan n1 dan n2 tidak sama
        while n1 == n2 :
            n2 = (random.randint(0, self.magic_cube.size -1 ),
                  random.randint(0, self.magic_cube.size - 1), 
                  random.randint(0, self.magic_cube.size - 1))
            
        # Menukar neighbor 
        neighbor[n1], neighbor[n2] = neighbor[n1], neighbor[n2] 

        return neighbor