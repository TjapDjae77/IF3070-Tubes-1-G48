from cube.magic_cube import MagicCube
from cube.objective_function import ObjectiveFunction


class GeneticAlgorithm:
    def __init__(self, population_size, generations, mutation_rate):
        self.population_size = population_size
        self.generations =  generations
        self.mutation_rate = mutation_rate
        self.population = [MagicCube() for _ in range(population_size)]
    
    def display_population(self):
        for i, cube in enumerate(self.population):
            print(f"Cube {i+1}:")
            cube.display()
            print("\n")

    def evaluate_population(self):
        fitness_scores = []

        for cube in self.population:
            fitness_score = ObjectiveFunction(cube).calculate()
            fitness_scores.append((cube, fitness_score))

        fitness_scores.sort(key=lambda x: x[1])

        return fitness_scores