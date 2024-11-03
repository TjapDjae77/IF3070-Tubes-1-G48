import numpy as np
import random

class MagicCube:
    def __init__(self, size=5):
        self.size = size
        self.magic_number = 315
        self.cube = self.initialize_cube()

    def initialize_cube(self):
        numbers = list(range(1, self.size**3 + 1))
        random.shuffle(numbers)
        return np.array(numbers).reshape((self.size, self.size, self.size))
    
    def display(self):
        print("Current Cube State: ")
        print(self.cube)