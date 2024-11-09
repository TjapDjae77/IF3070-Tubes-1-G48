import matplotlib.pyplot as plt
import numpy as np
import random
import time
from cube.magic_cube import MagicCube
from cube.objective_function import ObjectiveFunction
from cube.neighbor_state import NeighborState

class GeneticAlgorithm:
    def __init__(self, population_size, max_iteration, mutation_rate):
        self.population_size = population_size
        self.max_iteration =  max_iteration
        self.mutation_rate = mutation_rate
        self.population = [MagicCube() for _ in range(population_size)]
        self.fitness_scores = []

    def display_population(self):
        for i, cube in enumerate(self.population):
            print(f"Cube {i+1}:")
            cube.display()
            print("\n")

    def get_num_elite(self, iteration):
        if (self.population_size <= 5):
            return 0  
        elif (self.population_size <= 10):
            return 1  
        elif self.population_size <= 20:
            if (iteration < self.max_iteration * 0.4):
                return 1  
            else:
                return 2  
        else:
            if (iteration < self.max_iteration * 0.4):
                return 1  
            elif (iteration < self.max_iteration * 0.8):
                return 2  
            else:
                return 3  

    def evaluate_population(self):
        self.fitness_scores = []

        for cube in self.population:
            fitness_score = ObjectiveFunction(cube).calculate()
            self.fitness_scores.append((cube, fitness_score))

        self.fitness_scores.sort(key=lambda x: x[1])

    # def select_one(self):
    #     inverse_fitness_scores = [1 / fitness for _, fitness in self.fitness_scores]
    #     total_inverse_fitness = sum(inverse_fitness_scores)
    #     selection_probabilities = [inverse_fitness / total_inverse_fitness for inverse_fitness in inverse_fitness_scores]
    #     pick = random.uniform(0, 1)
    #     cumulative_probability = 0
    #     for (cube, _), probability in zip(self.fitness_scores, selection_probabilities):
    #         cumulative_probability += probability
    #         if pick <= cumulative_probability:
    #             return cube

    def sus_selection(self):
        inverse_fitness_scores = [1 / fitness for _, fitness in self.fitness_scores]
        total_inverse_fitness = sum(inverse_fitness_scores)
        selection_probabilities = [inverse_fitness / total_inverse_fitness for inverse_fitness in inverse_fitness_scores]

        cumulative_probabilities = []
        cumulative_sum = 0
        for prob in selection_probabilities:
            cumulative_sum += prob
            cumulative_probabilities.append(cumulative_sum)

        distance = 1.0 / 2
        start_point = random.uniform(0, distance)
        pointers = [start_point + i * distance for i in range(2)]

        selected_parents = []
        for pointer in pointers:
            for i, cumulative_prob in enumerate(cumulative_probabilities):
                if pointer <= cumulative_prob:
                    selected_parents.append(self.fitness_scores[i][0])  # Ambil individu yang terpilih
                    break

        return selected_parents

    def selection(self):
        parent1, parent2 = self.sus_selection()
        while parent1 == parent2:
            parent2 = self.sus_selection()

        return parent1, parent2

    def layer_crossover_pair(self, parent1, parent2):
        offspring1_cube = np.zeros_like(parent1.cube)
        offspring2_cube = np.zeros_like(parent2.cube)

        for i in range(parent1.size):
            if (i % 2 == 0):
                offspring1_cube[i] = parent1.cube[i]
                offspring2_cube[i] = parent2.cube[i]
            else:
                offspring1_cube[i] = parent2.cube[i]
                offspring2_cube[i] = parent1.cube[i]

        offspring1 = MagicCube(size=parent1.size)
        offspring2 = MagicCube(size=parent2.size)
        offspring1.cube = offspring1_cube
        offspring2.cube = offspring2_cube
        return offspring1, offspring2

    def uniform_crossover_pair(self, parent1, parent2):
        offspring1_cube = np.zeros_like(parent1.cube)
        offspring2_cube = np.zeros_like(parent2.cube)

        for i in range(parent1.size):
            for j in range(parent1.size):
                for k in range(parent1.size):
                    if (random.random() < 0.5):
                        offspring1_cube[i, j, k] = parent1.cube[i, j, k]
                        offspring2_cube[i, j, k] = parent2.cube[i, j, k]
                    else:
                        offspring1_cube[i, j, k] = parent2.cube[i, j, k]
                        offspring2_cube[i, j, k] = parent1.cube[i, j, k]
        
        offspring1 = MagicCube(size=parent1.size)
        offspring2 = MagicCube(size=parent2.size)
        offspring1.cube = offspring1_cube
        offspring2.cube = offspring2_cube
        return offspring1, offspring2
    
    def adaptive_crossover_pair(self, parent1, parent2, iteration, max_iteration):
        if (iteration < (max_iteration * 0.5)):
            return self.uniform_crossover_pair(parent1, parent2)
        elif (iteration  < (max_iteration * 0.8)):
            if (random.random() < 0.7):
                return self.uniform_crossover_pair(parent1, parent2)
            else:
                return self.layer_crossover_pair(parent1, parent2)
        else:
            return self.layer_crossover_pair(parent1, parent2)
        
    def swap_mutation(self, magic_cube):
        neighbor_state = NeighborState(magic_cube)
        return neighbor_state.generate_neighbor()

    def inversion_mutation(self, magic_cube):
        i = random.randint(0, magic_cube.size - 1)
        j = random.randint(0, magic_cube.size - 1)
        magic_cube.cube[i, j, :] = magic_cube.cube[i, j, ::-1]
        return magic_cube
    
    def scramble_mutation(self, magic_cube):
        layer_index = random.randint(0, magic_cube.size - 1)
        flat_layer = magic_cube.cube[layer_index].flatten()
        np.random.shuffle(flat_layer)
        magic_cube.cube[layer_index] = flat_layer.reshape(magic_cube.size, magic_cube.size)
        return magic_cube
    
    def adaptive_mutation(self, magic_cube, iteration, max_iteration):
        iteration_progress = iteration / max_iteration
        # Atur mutation rate adaptif berdasarkan progres iterasi
        if iteration_progress < 0.4:
            # Di awal hingga pertengahan, meningkatkan mutation rate mendorong eksplorasi
            if (self.mutation_rate < 0.3):
                self.mutation_rate = self.mutation_rate * 1.1
        elif 0.4 <= iteration_progress < 0.8:
            # Di pertengahan generasi, menurunkan mutation rate untuk menyeimbangkan eksplorasi dengan eksploitasi
            if (self.mutation_rate > 0.01):
                self.mutation_rate = self.mutation_rate * 0.98
        else:
            # Di akhir generasi, turunkan mutation rate untuk mengeksploitasi solusi terbaik
            if (self.mutation_rate > 0.05):
                self.mutation_rate = self.mutation_rate * 0.95


        if (random.random() >= self.mutation_rate):
            return magic_cube
        
        if (iteration < (max_iteration * 0.3)):
            return self.scramble_mutation(magic_cube)
        elif (iteration < (max_iteration * 0.7)):
            return self.inversion_mutation(magic_cube)
        else:
            return self.swap_mutation(magic_cube)

    @staticmethod  
    def get_valid_input(prompt, min_value=1, value_type="integer"):
        while True:
            try:
                user_input = input(prompt).split()

                if (value_type == "integer"):
                    if not all(x.lstrip('-').isdigit() for x in user_input):
                        raise TypeError("Semua input harus berupa angka bulat (integer).")
                    
                values = [int(x) for x in user_input]

                if any(value < min_value for value in values):
                    raise ValueError(f"Nilai minimal harus {min_value} atau lebih besar.")
                
                return values
            
            except (ValueError, TypeError) as e:
                print(f"Error: {e}\nSilakan masukkan input yang valid.")
    
    @staticmethod
    def run_multiple_tests(populations, iterations, mutation_rate=0.1, is_fixed_iteration=True):
        for param in (populations if is_fixed_iteration else iterations):
            run_results = []
            if(is_fixed_iteration):
                param_type = "Populasi"
                fixed_param = iterations[0]
            else:
                param_type = "Iterasi"
                fixed_param = populations[0]

            print(f"\nMenjalankan GA dengan {param_type} {param} dan {'Iterasi' if is_fixed_iteration else 'Populasi'} {fixed_param}:")
            for i in range(3):
                print(f"\nUji ke-{i + 1} untuk {param_type.lower()} {param} dan {'iterasi' if is_fixed_iteration else 'populasi'} {fixed_param}:")
                if is_fixed_iteration:
                    max_scores, avg_scores, duration = GeneticAlgorithm.run_genetic_algorithm(param, fixed_param, mutation_rate)
                else:
                    max_scores, avg_scores, duration = GeneticAlgorithm.run_genetic_algorithm(fixed_param, param, mutation_rate)
                run_results.append((max_scores, avg_scores, f'Run ke-{i+1}'))

            GeneticAlgorithm.plot_multiple_runs(
                run_results,
                max_iteration=fixed_param if is_fixed_iteration else param,
                title=f'{param_type} {param} dan {"Iterasi" if is_fixed_iteration else "Populasi"} {fixed_param}'
            )

                
    @staticmethod
    def run_genetic_algorithm(population_size, max_iteration, mutation_rate):
        ga = GeneticAlgorithm(population_size, max_iteration, mutation_rate)

        start_time = time.time()

        max_scores_per_iteration = []
        avg_scores_per_iteration = []
        
        ga.evaluate_population()

        print("Initial Fitness Scores for Entire Population:")
        for i, (cube, fitness_score) in enumerate(ga.fitness_scores):
            print(f"Cube {i+1} Fitness Score: {fitness_score}")
        
        print("\nState awal populasi (menampilkan individu pertama):")
        ga.population[0].display()

        for iteration in range(max_iteration):
            new_population = []

            num_elite = ga.get_num_elite(iteration)
            new_population = [ga.fitness_scores[i][0] for i in range(num_elite)]

            while len(new_population) < ga.population_size:
                parent1, parent2 = ga.selection()
                offspring1, offspring2 = ga.adaptive_crossover_pair(parent1, parent2, iteration, ga.max_iteration)
                offspring1 = ga.adaptive_mutation(offspring1, iteration, ga.max_iteration)
                offspring2 = ga.adaptive_mutation(offspring2, iteration, ga.max_iteration)
                new_population.extend([offspring1, offspring2])

            # Motong kalo kelebihan populasi (karena populasi ganjil)
            if len(new_population) > ga.population_size:
                new_population = new_population[:ga.population_size]

            # Ganti populasi lama dengan populasi baru
            ga.population = new_population
            
            # Evaluasi populasi baru
            ga.evaluate_population()

            scores = [fitness for _, fitness in ga.fitness_scores]
            max_score = min(scores)  # Nilai minimum dianggap terbaik
            avg_score = sum(scores) / len(scores)

            max_scores_per_iteration.append(max_score)
            avg_scores_per_iteration.append(avg_score)
            
        end_time = time.time()
        duration = end_time - start_time
        print("\nState akhir populasi (menampilkan individu terbaik):")
        ga.fitness_scores[0][0].display()

        best_fitness_score = ga.fitness_scores[0][1]
        print(f"\nNilai objective function akhir yang dicapai: {best_fitness_score}")
        print(f"Jumlah populasi: {population_size}")
        print(f"Banyak iterasi: {max_iteration}")
        print(f"Durasi proses pencarian: {duration:.2f} detik")

        # Cetak fitness score dari generasi baru
        print("\nFitness Scores for New Population:")
        for i, (cube, fitness_score) in enumerate(ga.fitness_scores):
            print(f"Cube {i+1} Fitness Score: {fitness_score}")

        return max_scores_per_iteration, avg_scores_per_iteration, duration
    
    @staticmethod
    def plot_multiple_runs(results, max_iteration, title="Perkembangan Nilai Objective Function"):
        iteration = range(max_iteration)
        num_runs = len(results)

        fig, axes = plt.subplots(1, num_runs, figsize=(18, 6), sharey=True)
        fig.suptitle(title)

        for idx, (max_scores, avg_scores, run_label) in enumerate(results):
            ax = axes[idx]
            ax.plot(iteration, max_scores, label='Maksimum', linestyle='--', color='red')
            ax.plot(iteration, avg_scores, label='Rata-rata', color='blue')
            ax.set_title(run_label)
            ax.set_xlabel('Iterasi')
            if idx == 0:
                ax.set_ylabel('Nilai Objective Function')
            ax.grid(True, linestyle='--', linewidth=0.5)
            ax.legend()

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()