from cube.magic_cube import MagicCube
from cube.objective_function import ObjectiveFunction
from cube.neighbor_state import NeighborState

class StochasticHillClimbing:
    def __init__(self, max_iteration):
        self.current_state = MagicCube()
        self.max_iteration = max_iteration
    
    def searchbestNeighbor(self):
        best_neighbor_value = 999999
        best_neighbor = None

        for i in range (self.max_iteration):
            neighbor = NeighborState(self.current_state).generate_neighbor()  
            neighbor_value = ObjectiveFunction(neighbor).calculate()  
            
            if neighbor_value < best_neighbor_value:
                best_neighbor_value = neighbor_value
                best_neighbor = neighbor
            else:
                break
        
        return best_neighbor

    
    def evaluateNeighbor(self):
        current_value = ObjectiveFunction(self.current_state).calculate()
        
        for i in range(self.max_iteration):
            best_neighbor = self.searchbestNeighbor()
            best_neighbor_value = ObjectiveFunction(best_neighbor).calculate()

            if best_neighbor_value < current_value:
                self.current_state = best_neighbor
                current_value = best_neighbor_value  

            print(f"Iteration {i + 1} - Current Cube State:")
            self.current_state.display()

            final_score = best_neighbor_value
            print(f"Final score (objective value): {final_score}")

        return self.current_state