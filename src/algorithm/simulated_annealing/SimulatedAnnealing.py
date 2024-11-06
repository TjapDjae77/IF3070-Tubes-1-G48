from cube.magic_cube import MagicCube
from cube.objective_function import ObjectiveFunction
from cube.neighbor_state import NeighborState
import math
import random
import numpy

class SimulatedAnnealing:
    def __init__(self, starting_tem, cooling_rate, minimum_tem):
        self.starting_tem = starting_tem
        self.cooling_rate = cooling_rate
        self.minimum_tem = minimum_tem
        self.magic_cube = MagicCube()
    

    def simulatedannealing(self):
        neighbor_generator = NeighborState(self.magic_cube)
        objective_function = ObjectiveFunction(self.magic_cube)

        # Initial state kubus
        current_state = self.magic_cube.cube.copy()
        current_score = objective_function.calculate()
        tem = self.starting_tem

        while tem > self.minimum_tem :
            # Pemanggilan algoritma neighbor
            neighbor = neighbor_generator.generate_neighbor()
        
            # Penyimpan nilai neighbor
            self.magic_cube.cube = neighbor
            neighbor_score = objective_function.calculate()

            # Algoritma penerimaan langkah
            if neighbor_score < current_score :
                current_state = neighbor.copy()
                current_score = neighbor_score
            else :
                probability = math.exp((current_score - neighbor_score) / tem)
                if random.random() < probability :
                    current_state = neighbor
                    current_score = neighbor_score
            
            # Mengembalikan cube kembali
            self.magic_cube.cube = current_state

            tem *= self.cooling_rate

        return current_state, current_score

        
        
# Algoritma Simulated Annealing
# 
# Loop until Tawal < Takhir
# Hitung state cube, objective function dan neighbor
# Acceptance probability : p=exp((current_score−neighbor_score)/T), turunkan temperatur T=T×α
# Algoritma terhenti ketika mencapai hasil optimum atau mencapai tmin