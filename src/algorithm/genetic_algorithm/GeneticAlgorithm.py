import numpy as np
import random
from cube.magic_cube import MagicCube
from cube.objective_function import ObjectiveFunction


class GeneticAlgorithm:
    def __init__(self, population_size, max_generations, mutation_rate):
        self.population_size = population_size
        self.max_generations =  max_generations
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
    
    def adaptive_crossover_pair(self, parent1, parent2, generation, max_generations):
        if (generation < (max_generations * 0.3)):
            print("TERPILIH UNIFORM BAGIAN 1")
            return self.uniform_crossover_pair(parent1, parent2)
        elif (generation  < (max_generations * 0.7)):
            if (random.random() < 0.5):
                print("TERPILIH UNIFORM BAGIAN 2")
                return self.uniform_crossover_pair(parent1, parent2)
            else:
                print("TERPILIH LAYER BAGIAN 2")
                return self.layer_crossover_pair(parent1, parent2)
        else:
            print("TERPILIH LAYER BAGIAN 3")
            return self.layer_crossover_pair(parent1, parent2)



