from cube.magic_cube import MagicCube
from cube.objective_function import ObjectiveFunction
from cube.neighbor_state import NeighborState
import random


class SteepestAscent:
    def __init__(self):
        self.current_state = MagicCube()

    def searchbestNeighbor(self):
        best_neighbor = 999
        while True:
            neighbor = NeighborState(self.current_state).generate_neighbor() #generate neigbor
            neighbor_value = ObjectiveFunction(neighbor).calculate() #check neighbor value
            
            if neighbor_value < best_neighbor: 
                best_neighbor = neighbor_value
            else:
                break
        return best_neighbor
    
    def evaluateNeighbor(self):
        current_value = ObjectiveFunction(self.current_state).calculate()
        total_iteration = 0

        while True:
            best_neighbor = self.searchbestNeighbor()
            best_neighbor_value = ObjectiveFunction(best_neighbor).calculate()

            #comparing
            if best_neighbor_value < current_value:
                self.current_state = best_neighbor
                total_iteration += 1
            else:
                print (f"Total iteration: {total_iteration}")
                break

        return self.current_state
