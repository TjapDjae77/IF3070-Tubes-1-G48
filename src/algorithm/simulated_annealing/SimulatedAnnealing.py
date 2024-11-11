import math
import random
import time
import matplotlib.pyplot as plt
from cube.magic_cube import MagicCube
from cube.objective_function import ObjectiveFunction
from cube.neighbor_state import NeighborState

class SimulatedAnnealing:
    def __init__(self, starting_tem, cooling_rate, minimum_tem):
        self.starting_tem = starting_tem
        self.cooling_rate = cooling_rate
        self.minimum_tem = minimum_tem
        self.magic_cube = MagicCube()
    
    def initial_state(self):
        # Display state awal kubus
        print("Initial Cube: ")
        self.magic_cube.display()        
        awal_score = ObjectiveFunction(self.magic_cube).calculate()
        print("Initial Objective Function Score: ", awal_score)

    def accept_neighbor(self, current_score, neighbor_score, tem):
        # Penerimaan neighbor
        if neighbor_score < current_score:
            return True, 1.0  # Probabilitas penuh jika lebih baik
        probability = math.exp((current_score - neighbor_score) / tem)
        return random.random() < probability, probability   
    
    def tracker_data(self, score_seluruh, prob_seluruh, current_score, tem, probability):
        # Update data tracker untuk plotting
        score_seluruh.append(current_score)
        # tem_seluruh.append(tem)
        prob_seluruh.append(probability)

    def simulatedannealing(self):
        neighbor_generator = NeighborState(self.magic_cube)
        objective_function = ObjectiveFunction(self.magic_cube)

        # Initial state kubus
        current_state = self.magic_cube
        current_score = objective_function.calculate()
        tem = self.starting_tem

        # Display data initial state
        self.initial_state()

        # Tracker data
        score_seluruh = [current_score]
        tem_seluruh = [tem]
        prob_seluruh = []
        iterations = 0
        stuck_count = 0

        start_time = time.time()

        while tem > self.minimum_tem:
            # Pemanggilan algoritma neighbor
            neighbor = neighbor_generator.generate_neighbor()
        
            # Penyimpan nilai neighbor
            objective_function.magic_cube = neighbor
            neighbor_score = objective_function.calculate()

            # Pemanggilan algoritma penerimaan neighbor
            accepted, probability = self.accept_neighbor(current_score, neighbor_score, tem)
            if accepted:
                current_state = neighbor
                current_score = neighbor_score
                stuck_count = 0
                iterations += 1
            else:
                stuck_count += 1

            # Update tracker data
            self.tracker_data(score_seluruh, prob_seluruh, current_score, tem, probability)
            
            # Update state cube
            self.magic_cube.cube = current_state.cube

            # Cooling system dan penghitungan iterasi
            tem *= self.cooling_rate

        # Penghitungan durasi
        end_time = time.time()
        duration = end_time - start_time

        # Pemanggilan algoritma print
        self.final_state(current_score, iterations, duration, stuck_count)
        self.plot_results(score_seluruh, prob_seluruh)

        return self.magic_cube.cube
    
    def final_state(self, current_score, iterations, duration, stuck_count):
        # Print data final state cube
        print("\nFinal Cube State: ")
        print(self.magic_cube.cube)
        print("Nilai Final Objective Function: ", current_score)
        print("Total Iterasi: ", iterations)
        print(f"Durasi: {duration:.2f}")
        print("Jumlah Stuck: ", stuck_count)

    def plot_results(self, scores_seluruh, prob_seluruh):
        plt.figure(figsize=(12, 6))

        # Plot objective function terhadap iterations
        plt.subplot(1, 2, 1)
        plt.plot(scores_seluruh, label='Objective Function')
        plt.xlabel('Iterations')
        plt.ylabel('Objective Function')
        plt.title('Objective Function terhadap Iterasi')
        plt.legend()

        # Plot probability terhadap iterations
        plt.subplot(1, 2, 2)
        plt.plot(prob_seluruh, label='Probability', color='green')
        plt.xlabel('Iterations')
        plt.ylabel('Acceptance Probability')
        plt.title('Probability terhadap Iterasi')
        plt.legend()

        plt.tight_layout()
        plt.show()
