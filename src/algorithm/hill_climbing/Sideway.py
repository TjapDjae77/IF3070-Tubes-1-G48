from cube.magic_cube import MagicCube
from cube.objective_function import ObjectiveFunction
from cube.neighbor_state import NeighborState
import matplotlib.pyplot as plt
import time

class SidewayHillClimbing:
    def __init__(self, max_sideways_moves=100):
        self.current_state = MagicCube()
        self.current_value = ObjectiveFunction(self.current_state).calculate()
        self.max_sideways_moves = max_sideways_moves
        self.iterations = 0
        self.objective_values = []  

    def searchbestNeighbor(self):
        best_neighbor = None
        best_neighbor_value = 99999

        for _ in range(25): 
            neighbor = NeighborState(self.current_state).generate_neighbor()
            neighbor_value = ObjectiveFunction(neighbor).calculate()
            
            if neighbor_value < best_neighbor_value:
                best_neighbor = neighbor
                best_neighbor_value = neighbor_value

        return best_neighbor

    def evaluateNeighbor(self):
        sideways_moves = 0
        start_time = time.time() 

        while True:
            best_neighbor = self.searchbestNeighbor()
            best_neighbor_value = ObjectiveFunction(best_neighbor).calculate()
            self.iterations += 1

            self.objective_values.append(self.current_value) 

            if best_neighbor_value < self.current_value:
                self.current_state = best_neighbor
                self.current_value = best_neighbor_value
                sideways_moves = 0 # RESET

            elif best_neighbor_value == self.current_value and sideways_moves < self.max_sideways_moves:
                self.current_state = best_neighbor
                sideways_moves += 1

            else:
                print("Tidak ada neighbor dengan value yang lebih baik.")
                break

        self.objective_values.append(self.current_value)

        end_time = time.time() 
        total_duration = end_time - start_time

        return total_duration

    @staticmethod
    def plot_multiple_runs(results, title="Pebandingan Objective Function dan Iterasi"):
        fig, axes = plt.subplots(1, len(results), figsize=(18, 6), sharey=True)

        if len(results) == 1:
            axes = [axes]

        fig.suptitle(title)

        for idx, (objective_values, run_label, total_duration) in enumerate(results):
            ax = axes[idx]
            iterations = range(len(objective_values))

            ax.plot(iterations, objective_values, label='Objective Value', color='blue')
            ax.set_title(run_label)
            ax.set_xlabel('Iteration')
            if idx == 0:
                ax.set_ylabel('Objective Function Value')
            ax.grid(True, linestyle='--', linewidth=0.5)
            ax.legend()

            ax.text(0.5, 0.95, f"Total Duration: {total_duration:.6f} s", 
                    transform=ax.transAxes, ha="center", va="top", fontsize=12, color='red')

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()