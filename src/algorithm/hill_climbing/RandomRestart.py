from cube.magic_cube import MagicCube
from cube.objective_function import ObjectiveFunction
from cube.neighbor_state import NeighborState


class RandomRestart:
    def __init__(self, max_restarts=10):
        self.max_restarts = max_restarts
        self.best_value

    def searchbestNeighbor(self):
        best_neighbor_value = 999999
        best_neighbor = None
        while True:
            neighbor = NeighborState(self.current_state).generate_neighbor() #generate neigbor
            neighbor_value = ObjectiveFunction(neighbor).calculate() #check neighbor value
            
            print(f"Current Neighbor Score: {neighbor_value}, Best Neighbor Score: {best_neighbor_value}")

            if neighbor_value < best_neighbor_value:
                best_neighbor_value = neighbor_value
                best_neighbor = neighbor
                print(f"changed: Current Neighbor Score: {neighbor_value}, Best Neighbor Score: {best_neighbor_value}")
            else:
                print(f"Generate BN - Current Neighbor Score: {neighbor_value}, Best Neighbor Score: {best_neighbor_value}")
                print()
                break

        return best_neighbor
    
    def evaluateNeighbor(self):
        current_value = ObjectiveFunction(self.current_state).calculate()
        total_iteration = 0

        while True:
            best_neighbor = self.searchbestNeighbor()
            best_neighbor_value = ObjectiveFunction(best_neighbor).calculate()

            print(f"Iteration {total_iteration + 1} - Current Score: {current_value}, Best Neighbor Score: {best_neighbor_value}")

            #comparing
            if best_neighbor_value < current_value:
                self.current_state = best_neighbor
                current_value = best_neighbor_value
                total_iteration += 1
                print(f"Current Score: {current_value}")

            else:
                print(f"Current Score: {current_value}, Best Neighbor Score: {best_neighbor_value}")
                print(f"Total iteration: {total_iteration}")
                print()
                break

    def randomRestart(self):
        best_value = 999999
        best_state = None