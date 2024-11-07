from cube.magic_cube import MagicCube
from cube.objective_function import ObjectiveFunction
from cube.neighbor_state import NeighborState
import math
import random
import time
import matplotlib.pyplot as plt

class SimulatedAnnealing:
    def __init__(self, starting_tem, cooling_rate, minimum_tem):
        self.starting_tem = starting_tem
        self.cooling_rate = cooling_rate
        self.minimum_tem = minimum_tem
        self.magic_cube = MagicCube()
    

    def simulatedannealing(self):
        neighbor_generator = NeighborState(self.magic_cube)
        objective_function = ObjectiveFunction(self.magic_cube)

        # Initial state kubus
        current_state = self.magic_cube
        current_score = objective_function.calculate()
        tem = self.starting_tem

        # Tracker data
        score_seluruh = [current_score]
        tem_seluruh = [tem]
        iterations = 0
        stuck_count = 0

        start_time = time.time()

        while tem > self.minimum_tem :
            # Pemanggilan algoritma neighbor
            neighbor = neighbor_generator.generate_neighbor()
        
            # Penyimpan nilai neighbor
            objective_function.magic_cube = neighbor
            neighbor_score = objective_function.calculate()

            # Algoritma penerimaan langkah
            if neighbor_score < current_score :
                current_state = neighbor
                current_score = neighbor_score
                stuck_count = 0
            else :
                probability = math.exp((current_score - neighbor_score) / tem)
                if random.random() < probability :
                    current_state = neighbor
                    current_score = neighbor_score
                    stuck_count = 0
                else :
                    stuck_count += 1
            
            # Update tracker data
            score_seluruh.append(current_score)
            tem_seluruh.append(tem)
            
            # Mengembalikan cube kembali
            self.magic_cube.cube = current_state.cube

            # Cooling system
            tem *= self.cooling_rate
            iterations += 1

        # Penghitungan durasi
        end_time = time.time()
        duration = end_time - start_time

        self.plot_results(score_seluruh, tem_seluruh)

        # Printing data
        print("\nFinal Cube State:")
        print(self.magic_cube.cube)
        print("Nilai Objective Value:", current_score)
        print("Total Iterasi:", iterations)
        print("Durasi:", duration)
        print("Stuck Count Frequency:", stuck_count)


        return self.magic_cube.cube

    def plot_results(self, scores_seluruh, tem_seluruh):
        plt.figure(figsize=(12, 6))

        # Plot objective function terhadap iterations
        plt.subplot(1, 2, 1)
        plt.plot(scores_seluruh, label='Objective Function')
        plt.xlabel('Iterations')
        plt.ylabel('Objective Function')
        plt.title('Objective Function terhadap Iterasi')
        plt.legend()

        # Plot temperature terhadap iterations
        plt.subplot(1, 2, 2)
        plt.plot(tem_seluruh, label='Temperature', color='orange')
        plt.xlabel('Iterations')
        plt.ylabel('Temperature')
        plt.title('Temperatur terhadap Iterasi')
        plt.legend()

        plt.tight_layout()
        plt.show()       