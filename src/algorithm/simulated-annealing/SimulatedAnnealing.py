from cube.magic_cube import MagicCube
from cube.objective_function import ObjectiveFunction


class SimulatedAnnealing:
    def __init__(self, starting_tem, cooling_rate, minimum_tem):
        self.starting_tem = starting_tem;
        self.cooling_rate = cooling_rate;
        self.minimum_tem = minimum_tem;

# Algoritma Simulated Annealing
# 
# Loop until Tawal < Takhir
# Hitung state cube, objective function dan neighbor
# Acceptance probability : p=exp((current_score−neighbor_score)/T), turunkan temperatur T=T×α
# Algoritma terhenti ketika mencapai hasil optimum atau mencapai tmin