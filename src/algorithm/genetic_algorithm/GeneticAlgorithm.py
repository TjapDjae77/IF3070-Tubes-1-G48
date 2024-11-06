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
            current += 1 / (fitness + 1)
            if current > pick:
                return cube

    def selection(self):
        total_fitness = sum(1/(score[1] + 1) for score in self.fitness_scores)
        parent1 = self.select_one(total_fitness)
        parent2 = self.select_one(total_fitness)
        while parent1 ==  parent2:
            parent2 = self.select_one(total_fitness)

        return parent1, parent2

    def layer_crossover(self, parent1, parent2):
        offspring_cube = np.zeros_like(parent1.cube)

        for i in range(parent1.size):
            if (i % 2 == 0):
                offspring_cube[i] = parent1.cube[i]
            else:
                offspring_cube[i] = parent2.cube[i]

        offspring = MagicCube(size=parent1.size)
        offspring.cube = offspring_cube
        return offspring

    def uniform_crossover(self, parent1, parent2):
        offspring_cube = np.zeros_like(parent1.cube)

        for i in range(parent1.size):
            for j in range(parent1.size):
                for k in range(parent1.size):
                    if (random.random() < 0.5):
                        offspring_cube[i, j, k] = parent1.cube[i, j, k]
                    else:
                        offspring_cube[i, j, k] = parent2.cube[i, j, k]
        
        offspring = MagicCube(size=parent1.size)
        offspring.cube = offspring_cube
        return offspring
    
    def adaptive_crossover(self, parent1, parent2, generation, max_generations):
        if (generation < (max_generations * 0.3)):
            return self.uniform_crossover(parent1, parent2)
        elif (generation  < (max_generations * 0.7)):
            if (random.random() < 0.5):
                return self.uniform_crossover(parent1, parent2)
            else:
                return self.layer_crossover(parent1, parent2)
        else:
            return self.layer_crossover(parent1, parent2)



