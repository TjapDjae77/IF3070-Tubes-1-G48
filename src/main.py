from algorithm.genetic_algorithm.GeneticAlgorithm import GeneticAlgorithm

if __name__ == "__main__":
    population_size = 5
    generations = 10
    mutation_rate = 0.05

    ga = GeneticAlgorithm(population_size, generations, mutation_rate)

    fitness_scores = ga.evaluate_population()


    print("Initial Population Fitness Scores:")
    for i, (cube, fitness_score) in enumerate(fitness_scores):
        print(f"Cube {i+1} Fitness Score: {fitness_score}")
        cube.display()  # Menampilkan state dari setiap kubus
        print("\n")

