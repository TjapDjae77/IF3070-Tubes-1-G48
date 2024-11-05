from cube.magic_cube import MagicCube
from cube.objective_function import ObjectiveFunction
from cube.neighbor_state import NeighborState
import math
import random


class SimulatedAnnealing:
    def __init__(self, starting_tem, cooling_rate, minimum_tem, magic_cube):
        self.starting_tem = starting_tem
        self.cooling_rate = cooling_rate
        self.minimum_tem = minimum_tem
        self.magic_cube = magic_cube

        # Pembuatan objek neighbor
        neighbor_generator = NeighborState(magic_cube)

        # Initial state kubus
        current_state = magic_cube.cube
        current_score = magic_cube.ObjectiveFunction()
        tem = starting_tem

        while tem > minimum_tem :
        # Pemanggilan algoritma neighbor
            neighbor = neighbor_generator.generate_neighbor()
        
        # Penyimpan nilai neighbor
            neighbor_score = magic_cube.ObjectiveFunction()

        # Algoritma penerimaan langkah
        if neighbor_score < current_score :
            current_state = neighbor
            current_score = neighbor_score
        else :
            probability = math.exp((current_score - neighbor_score) / tem)
            if random.random() < probability :
                current_state = neighbor
                current_score = neighbor_score

        tem *= cooling_rate
        
# Algoritma Simulated Annealing
# 
# Loop until Tawal < Takhir
# Hitung state cube, objective function dan neighbor
# Acceptance probability : p=exp((current_score−neighbor_score)/T), turunkan temperatur T=T×α
# Algoritma terhenti ketika mencapai hasil optimum atau mencapai tmin