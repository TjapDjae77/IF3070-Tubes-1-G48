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

    def evaluate_population(self):
        self.fitness_scores = []

        for cube in self.population:
            fitness_score = ObjectiveFunction(cube).calculate()
            self.fitness_scores.append((cube, fitness_score))

        self.fitness_scores.sort(key=lambda x: x[1])

    def select_one(self, total_fitness):
        pick = random.uniform(0, total_fitness)
        current = 0
        for cube, fitness in self.fitness_scores:
            current += total_fitness - fitness
            if current > pick:
                return cube

    def selection(self):
        total_fitness = sum(score[1] for score in self.fitness_scores)
        parent1 = self.select_one(total_fitness)
        parent2 = self.select_one(total_fitness)
        while parent1 ==  parent2:
            parent2 = self.select_one(total_fitness)

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
    
    def adaptive_crossover_pair(self, parent1, parent2, generation, max_iteration):
        if (generation < (max_iteration * 0.7)):
            return self.uniform_crossover_pair(parent1, parent2)
        elif (generation  < (max_iteration * 0.9)):
            if (random.random() < 0.8):
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
        # print(f"Inverted row at layer {i}, row {j}")
        return magic_cube
    
    def scramble_mutation(self, magic_cube):
        layer_index = random.randint(0, magic_cube.size - 1)
        flat_layer = magic_cube.cube[layer_index].flatten()
        np.random.shuffle(flat_layer)
        magic_cube.cube[layer_index] = flat_layer.reshape(magic_cube.size, magic_cube.size)
        # print(f"Scrambled layer at index {layer_index}")
        return magic_cube
    
    def adaptive_mutation(self, magic_cube, generation, max_iteration):
        generation_progress = generation / max_iteration
        # Atur mutation rate adaptif berdasarkan progres generasi
        if generation_progress < 0.4:
            # Di awal hingga pertengahan, gunakan mutation rate dasar
            self.mutation_rate = self.mutation_rate * 1.15
        elif 0.4 <= generation_progress < 0.8:
            # Di pertengahan generasi, tingkatkan mutation rate untuk mendorong eksplorasi
            self.mutation_rate = self.mutation_rate * 1.05
        else:
            # Di akhir generasi, turunkan mutation rate untuk mengeksploitasi solusi terbaik
            self.mutation_rate = self.mutation_rate * 0.9


        if (random.random() >= self.mutation_rate):
            return magic_cube
        
        if (generation < (max_iteration * 0.5)):
            return self.scramble_mutation(magic_cube)
        elif (generation < (max_iteration * 0.8)):
            return self.swap_mutation(magic_cube)
        else:
            # print("SWAP MUTATION")
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
    def run_multiple_tests(populations, iterations, mutation_rate=0.05, is_fixed_iteration=True):
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

        for generation in range(max_iteration):
            new_population = []
            
            for _ in range(population_size // 2):  # Lakukan crossover hingga populasi penuh
                # Seleksi untuk mendapatkan dua orang tua
                parent1, parent2 = ga.selection()

                # Cetak fitness score dari orang tua yang dipilih (opsional untuk debugging)
                # print("\nParent 1 Fitness Score:", ObjectiveFunction(parent1).calculate())
                # print("Parent 2 Fitness Score:", ObjectiveFunction(parent2).calculate())
                
                # Menghasilkan keturunan melalui adaptive crossover
                offspring1, offspring2 = ga.adaptive_crossover_pair(parent1, parent2, generation, max_iteration)

                # Melakukan adaptive mutation pada offspring
                offspring1 = ga.adaptive_mutation(offspring1, generation, max_iteration)
                offspring2 = ga.adaptive_mutation(offspring2, generation, max_iteration)
                
                # print("\nOffspring 1:", ObjectiveFunction(offspring1).calculate())
                # print("Offspring 2:", ObjectiveFunction(offspring2).calculate())

                # Tambahkan offspring ke populasi baru
                new_population.extend([offspring1, offspring2])

            if len(new_population) < population_size:
                parent1, parent2 = ga.selection()
                # print("\nParent 1 Fitness Score (extra):", ObjectiveFunction(parent1).calculate())
                # print("Parent 2 Fitness Score (extra):", ObjectiveFunction(parent2).calculate())

                # Menghasilkan keturunan melalui adaptive crossover
                extra_offspring, _ = ga.adaptive_crossover_pair(parent1, parent2, generation, max_iteration)
                # Melakukan adaptive mutation pada offspring
                extra_offspring = ga.adaptive_mutation(extra_offspring, generation, max_iteration)

                # print("\nExtra Offspring:", ObjectiveFunction(extra_offspring).calculate())

                # Tambahkan extra_offspring ke populasi baru
                new_population.append(extra_offspring)

            # Ganti populasi lama dengan populasi baru
            ga.population = new_population
            
            # Evaluasi populasi baru
            ga.evaluate_population()

            scores = [score[1] for score in ga.fitness_scores]
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

        # Plot nilai *objective function* maksimum dan rata-rata
        # plt.figure(figsize=(10, 6))
        # plt.plot(range(max_iteration), max_scores_per_iteration, label='Nilai Maksimum', color='red')
        # plt.plot(range(max_iteration), avg_scores_per_iteration, label='Nilai Rata-rata', color='blue')
        # plt.xlabel('Iterasi')
        # plt.ylabel('Nilai Objective Function')
        # plt.title('Perkembangan Nilai Objective Function per Iterasi')
        # plt.legend()
        # plt.grid(True)
        # plt.show()

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
            ax.set_xlabel('Generasi')
            if idx == 0:
                ax.set_ylabel('Nilai Objective Function')
            ax.grid(True, linestyle='--', linewidth=0.5)
            ax.legend()

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()

