from cube.magic_cube import MagicCube
from cube.objective_function import ObjectiveFunction
from cube.neighbor_state import NeighborState

class SidewayHillClimbing:
    def __init__(self, max_sideway):  
        self.current_state = MagicCube()
        self.max_sideway = max_sideway  
    
    def searchbestNeighbor(self):
        best_neighbor = None
        best_neighbor_value = 999999

        while True:
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
        sideways_moves_remaining = self.max_sideway
        total_iterations = 0

        while True:
            best_neighbor = self.searchbestNeighbor()
            best_neighbor_value = ObjectiveFunction(best_neighbor).calculate()
            total_iterations += 1

            # Change `self.current_value` to `current_value` here
            if best_neighbor_value < current_value:
                self.current_state = best_neighbor
                current_value = best_neighbor_value
                sideways_moves_remaining = self.max_sideway  # Reset sideways count after an improvement

            elif best_neighbor_value == current_value:
                if sideways_moves_remaining > 0:
                    self.current_state = best_neighbor
                    sideways_moves_remaining -= 1
                    print(f"Sideways move: {self.max_sideway-sideways_moves_remaining}")
                else:
                    print("Reached maximum sideways moves, terminating.")
                    break

            else:
                print("No better neighbor found, terminating.")
                break

            print(f"Iteration {total_iterations} - Current Cube State:")
            self.current_state.display()
            print(f"Current score (objective value): {current_value}")

        final_score = current_value
        print(f"Final score (objective value): {final_score}")

        return self.current_state