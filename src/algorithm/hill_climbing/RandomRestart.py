from cube.magic_cube import MagicCube
from cube.objective_function import ObjectiveFunction
from cube.neighbor_state import NeighborState
import matplotlib.pyplot as plt
import time


class RandomRestart:
    def __init__(self, max_restarts):
        self.max_restarts = max_restarts
        self.best_value = 999999
        self.best_state = None
        self.objective_values = []

    def searchbestNeighbor(self, current_state):
        best_neighbor_value = 999999
        best_neighbor = None

        for i in range(100):
            neighbor = NeighborState(current_state).generate_neighbor() #generate neigbor
            neighbor_value = ObjectiveFunction(neighbor).calculate() #check neighbor value

            if neighbor_value < best_neighbor_value:
                best_neighbor_value = neighbor_value
                best_neighbor = neighbor

        return best_neighbor, best_neighbor_value
    
    def evaluateNeighbor(self, initial_state):
        current_state = initial_state
        current_value = ObjectiveFunction(current_state).calculate()
        iterations = 0
        while True:
            best_neighbor, best_neighbor_value = self.searchbestNeighbor(current_state)
            
            #comparing
            if best_neighbor_value < current_value:
                current_state = best_neighbor
                current_value = best_neighbor_value
                iterations += 1
            else:
                break
            self.objective_values.append(current_value)

        return current_state, current_value, iterations

    def randomRestart(self):
        iteration_per_start = []

        #hill climb pertama
        initial_state = MagicCube()
        print(f"\nState Awal:")
        initial_state.display()
        print(f"\nNilai objective awal: {ObjectiveFunction(initial_state).calculate()}")

        total_iterations = 0

        start_time = time.time()

        final_state, final_value, iterations = self.evaluateNeighbor(initial_state)
        iteration_per_start.append(iterations)
        total_iterations += iterations

        if final_value < self.best_value:
                self.best_value = final_value
                self.best_state = final_state
        
        for restart in range(self.max_restarts): #restart
            initial_state = MagicCube()

            final_state, final_value, iterations = self.evaluateNeighbor(initial_state)
            total_iterations += iterations
            iteration_per_start.append(iterations)

            if final_value < self.best_value:
                self.best_value = final_value
                self.best_state = final_state
        
        execute_time = time.time() - start_time

        #print information           
        for step in range(len(iteration_per_start)):
            if step == 0:
                print(f"\nLangkah pertama - Total Iterations: {iteration_per_start[step]}")
            else:
                print(f"Restart ke-{step} - Total Iterations: {iteration_per_start[step]}")

        print(f"\nState Akhir:")
        self.best_state.display()
        print(f"\nNilai objective akhir: {self.best_value}")
        print(f"Waktu yang dibutuhkan: {execute_time:.2f} detik\n")

        self.show_plot(
                    objective_values=self.objective_values,
                    max_restarts=len(self.objective_values),
                    title=f'Perkembangan Nilai Objective Function\nMaksimal Restart: {self.max_restarts}\nWaktu: {execute_time:.2f} detik'
                )
    
    @staticmethod
    def show_plot(objective_values, max_restarts, title="Perkembangan Nilai Objective Function"):
        plt.figure(figsize=(10, 6))
        plt.plot(objective_values, label='Objective Value', color='blue')
        plt.title(title)
        plt.xlabel('Iteration')
        plt.ylabel('Objective Function Value')
        plt.grid(True, linestyle='--', linewidth=0.5)
        plt.legend()
        plt.tight_layout()
        plt.show()