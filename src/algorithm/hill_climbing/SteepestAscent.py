import matplotlib.pyplot as plt
from cube.magic_cube import MagicCube
from cube.objective_function import ObjectiveFunction
from cube.neighbor_state import NeighborState
import time


class SteepestAscent:
    def __init__(self):
        self.current_state = MagicCube()
        self.current_value = 999999
        self.objective_values = []  

    def searchbestNeighbor(self):
        best_neighbor = None
        best_neighbor_value = 999999

        for i in range(100):
            neighbor = NeighborState(self.current_state).generate_neighbor() #generate neigbor
            neighbor_value = ObjectiveFunction(neighbor).calculate() #check neighbor value
            
            if neighbor_value < best_neighbor_value:
                best_neighbor_value = neighbor_value
                best_neighbor = neighbor

        return best_neighbor, best_neighbor_value
    
    def evaluateNeighbor(self):
        total_iteration = 0
        
        print(f"\nState Awal:")
        self.current_state.display()

        start_time = time.time()
        
        while True:
            best_neighbor, best_neighbor_value = self.searchbestNeighbor()

            #comparing
            if best_neighbor_value < self.current_value:
                self.current_state = best_neighbor
                self.current_value = best_neighbor_value
                total_iteration += 1
                self.objective_values.append(self.current_value)
            else:
                break
        
        execute_time = time.time() - start_time
        
        print(f"\nState Akhir:")
        self.current_state.display()

        print(f"\nNilai objective akhir: {self.current_value}")
        print(f"Total iterasi: {total_iteration}")
        print(f"Waktu yang dibutuhkan: {execute_time:.2f} detik\n")

        self.show_plot(
                objective_values=self.objective_values,
                title=f'Perkembangan Nilai Objective Function\nWaktu: {execute_time:.2f} detik'
            )

    @staticmethod
    def show_plot(objective_values, title="Perkembangan Nilai Objective Function"):
        plt.figure(figsize=(10, 6))
        plt.plot(objective_values, label='Objective Value', color='blue')
        plt.title(title)
        plt.xlabel('Iteration')
        plt.ylabel('Objective Function Value')
        plt.grid(True, linestyle='--', linewidth=0.5)
        plt.legend()
        plt.tight_layout()
        plt.show()