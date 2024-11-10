from cube.magic_cube import MagicCube
from cube.objective_function import ObjectiveFunction
from cube.neighbor_state import NeighborState
import matplotlib.pyplot as plt
import time

class SidewayHillClimbing:
    def __init__(self, magic_cube, max_sideways_moves=100):
        self.magic_cube = magic_cube
        self.max_sideways_moves = max_sideways_moves
        self.iterations = 0
        self.objective_values = []  # List to track the objective values
        self.current_value = ObjectiveFunction(magic_cube).calculate()

    def searchbestNeighbor(self):
        best_neighbor = None
        best_neighbor_value = float('inf')
        # times = []  # List to store time taken for each neighbor evaluation

        for _ in range(25):  # Evaluasi neighbor
            # start_time = time.time()  
            neighbor = NeighborState(self.magic_cube).generate_neighbor()
            neighbor_value = ObjectiveFunction(neighbor).calculate()

            # end_time = time.time()  # End timing

        # Append time taken for this evaluation to list
            # times.append(end_time - start_time)
            
            if neighbor_value < best_neighbor_value:
                best_neighbor = neighbor
                best_neighbor_value = neighbor_value

        # avg_time_per_neighbor = sum(times) / len(times)
        # print(f"Average evaluation time per neighbor: {avg_time_per_neighbor:.6f} seconds")

        return best_neighbor

    def evaluateNeighbor(self):
        sideways_moves = 0
        start_time = time.time() 

        while True:
            best_neighbor = self.searchbestNeighbor()
            best_neighbor_value = ObjectiveFunction(best_neighbor).calculate()
            self.iterations += 1

            self.objective_values.append(self.current_value) # Buat nyimpen current_values

            if best_neighbor_value < self.current_value:
                self.magic_cube = best_neighbor
                self.current_value = best_neighbor_value
                sideways_moves = 0  # Reset Sideways Move

            elif best_neighbor_value == self.current_value and sideways_moves < self.max_sideways_moves:
                self.magic_cube = best_neighbor
                sideways_moves += 1
                print(f"Sideway move: {sideways_moves}")

            else:
                print("Tidak ada neighbor dengan value yang lebih baik.")
                break
            
            print(f"Iteration {self.iterations}: Current Value = {self.current_value}")

        self.objective_values.append(self.current_value)
        end_time = time.time()  # Capture the end time
        total_duration = end_time - start_time  # Calculate the total duration
        print(f"Total search duration: {total_duration:.6f} seconds")

        return self.magic_cube, self.current_value, self.iterations, total_duration

    @staticmethod
    def plot_multiple_runs(results, title="Objective Function Progress Over Iterations"):
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

            # Add total duration annotation
            ax.text(0.5, 0.95, f"Total Duration: {total_duration:.6f} s", 
                    transform=ax.transAxes, ha="center", va="top", fontsize=12, color='red')

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()