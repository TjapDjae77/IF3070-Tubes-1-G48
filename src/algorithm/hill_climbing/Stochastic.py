from cube.magic_cube import MagicCube
from cube.objective_function import ObjectiveFunction
from cube.neighbor_state import NeighborState
import matplotlib.pyplot as plt
import time

class StochasticHillClimbing:
    def __init__(self, max_iteration):
        self.current_state = MagicCube()
        self.current_value = ObjectiveFunction(self.current_state).calculate()
        self.max_iteration = max_iteration
        self.objective_values = []  

    def searchbestNeighbor(self):
        best_neighbor_value = 999999
        best_neighbor = None

        for _ in range (self.max_iteration):
            neighbor = NeighborState(self.current_state).generate_neighbor()  
            neighbor_value = ObjectiveFunction(neighbor).calculate()  
            
            if neighbor_value < best_neighbor_value:
                best_neighbor = neighbor
                best_neighbor_value = neighbor_value
        
        return best_neighbor

    
    def evaluateNeighbor(self):
        print("\nState Awal:")
        self.current_state.display()
        print(f"Nilai Initial Objective Function: {self.current_value}")
        start_time = time.time() 
        
        for _ in range(self.max_iteration):
            best_neighbor = self.searchbestNeighbor()
            best_neighbor_value = ObjectiveFunction(best_neighbor).calculate()

            if best_neighbor_value < self.current_value:
                self.current_state = best_neighbor
                self.current_value = best_neighbor_value
            else:
                break  

            self.objective_values.append(self.current_value)

        end_time = time.time()  
        total_duration = end_time - start_time

        print(f"State Akhir: ")
        self.current_state.display()
        print(f"Nilai Final Objective Function: {self.current_value}")

        print(f"Jumlah Iterasi: {self.max_iteration}")
        print(f"Total search duration: {total_duration:.6f} seconds") 

        return total_duration
    
    @staticmethod
    def plot_multiple_runs(results, max_iteration, title="Perkembangan Nilai Objective Function"):
        iteration = range(max_iteration)
        num_runs = len(results)

        fig, axes = plt.subplots(1, num_runs, figsize=(18, 6), sharey=True)
        
        if num_runs == 1:
            axes = [axes]

        fig.suptitle(title)

        for idx, (objective_values, run_label, total_duration) in enumerate(results):
            ax = axes[idx]
            ax.plot(range(len(objective_values)), objective_values, label='Nilai Objective', color='blue')
            ax.set_title(run_label)
            ax.set_xlabel('Iterasi')
            if idx == 0:
                ax.set_ylabel('Nilai Objective Function')
            ax.grid(True, linestyle='--', linewidth=0.5)
            ax.legend()

            ax.text(0.5, 0.95, f"Durasi: {total_duration:.2f} detik", 
                    transform=ax.transAxes, ha="center", va="top", fontsize=12, color='red')

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()