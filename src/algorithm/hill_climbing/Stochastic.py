from cube.magic_cube import MagicCube
from cube.objective_function import ObjectiveFunction
from cube.neighbor_state import NeighborState
import matplotlib.pyplot as plt

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
        
        return best_neighbor

    
    def evaluateNeighbor(self):
        self.objective_values = []  
        current_value = ObjectiveFunction(self.current_state).calculate()
        
        for i in range(self.max_iteration):
            best_neighbor = self.searchbestNeighbor()
            best_neighbor_value = ObjectiveFunction(best_neighbor).calculate()

            if best_neighbor_value < current_value:
                self.current_state = best_neighbor
                current_value = best_neighbor_value
            else:
                break  

            # print(f"Iteration {i + 1} - Current Cube State:")
            # self.current_state.display()
            self.objective_values.append(current_value)

            # final_score = best_neighbor_value
            # print(f"Final score (objective value): {final_score}")

        return self.current_state
    
    @staticmethod
    def plot_multiple_runs(results, max_iteration, title="Perkembangan Nilai Objective Function"):
        iteration = range(max_iteration)
        num_runs = len(results)

        # Create subplots; adjust for when there's only one plot
        fig, axes = plt.subplots(1, num_runs, figsize=(18, 6), sharey=True)
        
        # If there's only one plot, `axes` will not be a list but a single object
        if num_runs == 1:
            axes = [axes]

        fig.suptitle(title)

        # Loop over each result and plot
        for idx, (objective_values, run_label) in enumerate(results):
            ax = axes[idx]  # Access the subplot (axes[idx] works since axes is now a list)
            ax.plot(iteration, objective_values, label='Nilai Objective', color='blue')
            ax.set_title(run_label)
            ax.set_xlabel('Iterasi')
            if idx == 0:
                ax.set_ylabel('Nilai Objective Function')
            ax.grid(True, linestyle='--', linewidth=0.5)
            ax.legend()

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()