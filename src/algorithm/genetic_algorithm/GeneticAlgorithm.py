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

    def get_num_elite(self, iteration):
        ''' Mendapatkan jumlah individu elite di populasi '''
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
        ''' Prosedur untuk mengevaluasi seluruh populasi dan di-sorting menaik '''
        self.fitness_scores = []

        for cube in self.population:
            fitness_score = ObjectiveFunction(cube).calculate()
            self.fitness_scores.append((cube, fitness_score))

        self.fitness_scores.sort(key=lambda x: x[1])

    def tournament_selection(self, tournament_size):
        ''' Konsep seleksi menggunakan tournament selection, yaitu 
        mengambil sampel sebanyak tournament size secara random untuk diambil 2 individu terbaik sebagai parent'''
        participants = random.sample(self.fitness_scores, tournament_size)
        # Mengurutkan peserta berdasarkan fitness secara ascending
        sorted_participants = sorted(participants, key=lambda x: x[1])
        # Mengembalikan dua individu terbaik
        return sorted_participants[0][0], sorted_participants[1][0]

    def selection(self):
        ''' Seleksi individu untuk dijadikan parent dan memastikan parent bukanlah individu yang sama '''
        tournament_size = 2 if self.population_size < 20 else 5

        parent1, parent2 = self.tournament_selection(tournament_size=tournament_size)
        
        while parent1 == parent2:
            parent2 = self.tournament_selection(tournament_size=5)

        return parent1, parent2

    def partial_layer_crossover(self, parent1, parent2):
        ''' Teknik crossover yang digunakan adalah menggabungkan konsep 
        layer preservation dengan unique element filling '''
        # Membuat matriks kosong untuk child
        child1_cube = np.zeros_like(parent1.cube)
        child2_cube = np.zeros_like(parent2.cube)

        # Isi 3 layer pertama child 1 dengan elemen dari parent 1
        child1_cube[:3] = parent1.cube[:3]
        
        # Isi 3 layer terakhir child 2 dengan elemen dari parent 2
        child2_cube[-3:] = parent2.cube[-3:]

        # Buat set elemen yang sudah digunakan di child 1 dan child 2 serta menghilangkan bilangan nol di dalam set
        used_elements_1 = set(child1_cube.flatten()) - {0}
        used_elements_2 = set(child2_cube.flatten()) - {0}

        # Isi layer yang tersisa di child 1 dengan elemen unik dari parent 2
        for i in range(parent2.size):
            if (len(used_elements_1) == parent1.size**3):
                break
            for j in range(parent2.size):
                if (len(used_elements_1) == parent1.size**3):
                    break
                for k in range(parent2.size):
                    if (len(used_elements_1) == parent1.size**3):
                        break
                    element = parent2.cube[i, j, k]
                    if element not in used_elements_1:
                        for x in range(3, parent1.size):
                            for y in range(parent1.size):
                                for z in range(parent1.size):
                                    if child1_cube[x, y, z] == 0:
                                        child1_cube[x, y, z] = element
                                        used_elements_1.add(element)
                                        break
                                if element in used_elements_1:
                                    break
                            if element in used_elements_1:
                                break

        # Isi layer yang tersisa di child 2 dengan elemen unik dari parent 1
        for i in range(parent1.size):
            if (len(used_elements_2) == parent2.size**3):
                break
            for j in range(parent1.size):
                if (len(used_elements_2) == parent2.size**3):
                    break
                for k in range(parent1.size):
                    if (len(used_elements_2) == parent2.size**3):
                        break
                    element = parent1.cube[i, j, k]
                    if element not in used_elements_2:
                        for x in range(parent2.size - 3):
                            for y in range(parent2.size):
                                for z in range(parent2.size):
                                    if child2_cube[x, y, z] == 0:
                                        child2_cube[x, y, z] = element
                                        used_elements_2.add(element)
                                        break
                                if element in used_elements_2:
                                    break
                            if element in used_elements_2:
                                break

        # Membuat objek MagicCube baru untuk child
        child1 = MagicCube(size=parent1.size)
        child2 = MagicCube(size=parent2.size)
        child1.cube = child1_cube
        child2.cube = child2_cube
        return child1, child2
        
    def swap_mutation(self, magic_cube):
        ''' Swap mutation dilakukan dengan cara yang sama seperti mencari neighbor '''
        neighbor_state = NeighborState(magic_cube)
        return neighbor_state.generate_neighbor()
    
    def scramble_mutation(self, magic_cube):
        ''' Scramble mutation dilakukan dengan cara mencari index layer cube secara acak lalu bilangan-bilangan pada layer tersebut akan dishuffle '''
        layer_index = random.randint(0, magic_cube.size - 1)
        flat_layer = magic_cube.cube[layer_index].flatten()
        np.random.shuffle(flat_layer)
        magic_cube.cube[layer_index] = flat_layer.reshape(magic_cube.size, magic_cube.size)
        return magic_cube
    
    def adaptive_mutation(self, magic_cube, iteration, max_iteration):
        ''' Adaptive mutation akan memilih antara scramble mutation atau swap mutation berdasarkan progress iteration '''
        iteration_progress = iteration / max_iteration
        # Atur mutation rate adaptif berdasarkan progres generasi
        if iteration_progress < 0.5:
            # Di awal hingga pertengahan, mutation rate akan ditingkatkan hingga 50% dengan tujuan eksplorasi yang kuat
            if (self.mutation_rate < 0.5):
                self.mutation_rate = self.mutation_rate * 1.1
        else: # 0.5 <= iteration_progress <= 1
            # Di pertengahan hingga akhir, turunkan mutation rate untuk mengeksploitasi solusi terbaik
            if(self.mutation_rate > 0.1):
                self.mutation_rate = self.mutation_rate * 0.99

        # Terdapat probabilitas mutation rate yang jika tidak dipenuhi maka tidak akan dilakukan mutation
        if (random.random() >= self.mutation_rate):
            return magic_cube
        # Untuk 30% dari total iterasi, akan dilakukan scramble mutation
        if (iteration < (max_iteration * 0.3)):
            mutated_cube = self.scramble_mutation(magic_cube)
        else: # 70% sisanya akan dilakukan swap mutation
            mutated_cube = self.swap_mutation(magic_cube)

        # Memastikan bahwa jika ada yang duplikat fitnessnya maka akan dilakukan swap mutation hingga semua fitness pada populasi bersifat unik
        while self.is_duplicate_fitness(mutated_cube):
            mutated_cube = self.swap_mutation(mutated_cube)
        
        return mutated_cube

    def is_duplicate_fitness(self, cube):
        ''' Fungsi untuk memeriksa apakah ada duplikat fitness pada populasi '''
        # Menghitung fitness score dari individu yang di-check
        fitness_score = ObjectiveFunction(cube).calculate()
        
        # Memeriksa apakah fitness score ini sudah ada di populasi
        for _, existing_fitness in self.fitness_scores:
            if existing_fitness == fitness_score:
                return True
        return False

    @staticmethod  
    def get_valid_input(prompt, min_value=1, value_type="integer"):
        ''' Fungsi untuk memastikan input dari pengguna itu harus berupa integer dan 
        harus memiliki nilai lebih dari sama dengan min_value '''
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
    def run(population_size, max_iteration, mutation_rate=0.3):
        ''' Fungsi untuk menjalankan Genetic Algorithm, GA berikut menggunakan konsep elitisme,
          yaitu menyimpan elemen terbaik pada suatu iterasi untuk diletakkan pada generasi berikutnya  '''
        ga = GeneticAlgorithm(population_size, max_iteration, mutation_rate)
        # Memulai timer
        start_time = time.time()
        # Menyiapkan array untuk nilai maksimum dan rata-rata score per iterasi
        max_scores_per_iteration = []
        avg_scores_per_iteration = []
        # Mengevaluasi populasi
        ga.evaluate_population()
        # Menampilkan state awal populasi (best fitness)
        print("\nState awal populasi (menampilkan individu pertama):")
        ga.population[0].display()

        for iteration in range(max_iteration):
            # Populasi baru dikosongkan ulang setiap iterasi baru
            new_population = []
            # Mendapatkan jumlah elemen elite
            num_elite = ga.get_num_elite(iteration)
            # Memasukkkan elemen elite ke dalam populasi baru
            new_population = [ga.fitness_scores[i][0] for i in range(num_elite)]

            while len(new_population) < ga.population_size:
                # Melakukan seleksi, crossover, mutation dan dimasukkan ke dalam array new population
                parent1, parent2 = ga.selection()
                child1, child2 = ga.partial_layer_crossover(parent1, parent2)
                child1 = ga.adaptive_mutation(child1, iteration, ga.max_iteration)
                child2 = ga.adaptive_mutation(child2, iteration, ga.max_iteration)
                new_population.extend([child1, child2])

            # Memotong kalo kelebihan populasi (karena jumlah populasi yang harus dimasukkan ke new population itu ganjil)
            if len(new_population) > ga.population_size:
                new_population = new_population[:ga.population_size]

            # Mengganti populasi lama dengan populasi baru
            ga.population = new_population
            
            # Evaluasi populasi baru
            ga.evaluate_population()

            scores = [score[1] for score in ga.fitness_scores]
            max_score = min(scores)  # Nilai minimum dianggap terbaik
            avg_score = sum(scores) / len(scores)
            # Menyimpan score maksimum dan rata-rata ke dalam array
            max_scores_per_iteration.append(max_score)
            avg_scores_per_iteration.append(avg_score)

        # Mengakhiri timer    
        end_time = time.time()
        # Menghitung durasi
        duration = end_time - start_time
        # Menampilkan state akhir populasi (best fitness)
        print("\nState akhir populasi (menampilkan individu terbaik):")
        ga.fitness_scores[0][0].display()
        best_fitness_score = ga.fitness_scores[0][1]
        # Menampilkan Objective Function akhir, populasi, iterasi, dan durasi pencarian
        print(f"\nNilai objective function akhir yang dicapai: {best_fitness_score}")
        print(f"Jumlah populasi: {population_size}")
        print(f"Banyak iterasi: {max_iteration}")
        print(f"Durasi proses pencarian: {duration:.2f} detik")
        # Menjalankan fungsi plotting hasil iterasi
        GeneticAlgorithm.plot_result(max_scores_per_iteration, avg_scores_per_iteration, max_iteration, population_size)
    
    @staticmethod
    def plot_result(max_scores, avg_scores, max_iteration, population_size):
        ''' Fungsi untuk melakukan plotting hasil pencarian genetik '''
        plt.figure(figsize=(10, 6))
        plt.plot(range(max_iteration), max_scores, label='Nilai Maksimum', linestyle='--', color='red')
        plt.plot(range(max_iteration), avg_scores, label='Nilai Rata-rata', color='blue')
        plt.xlabel('Iterasi')
        plt.ylabel('Nilai Objective Function')
        plt.title(f'Perkembangan Nilai Objective Function\nPopulasi: {population_size} dan Iterasi: {max_iteration}')
        plt.legend()
        plt.grid(True)
        plt.show()