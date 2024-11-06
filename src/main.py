from algorithm.genetic_algorithm.GeneticAlgorithm import GeneticAlgorithm
from cube.objective_function import ObjectiveFunction



if __name__ == "__main__":
    population_size = 5
    max_generations = 10
    mutation_rate = 0.05

    ga = GeneticAlgorithm(population_size, max_generations, mutation_rate)

    # fitness_scores = ga.evaluate_population()

    ga.evaluate_population()

    print("Fitness Scores for Entire Population:")
    for i, (cube, fitness_score) in enumerate(ga.fitness_scores):
        print(f"Cube {i+1} Fitness Score: {fitness_score}")

    for generation in range(max_generations):
        new_population = []
        
        print(f"\n--- Generation {generation} ---")
        for _ in range(population_size // 2):  # Lakukan crossover hingga populasi penuh
            # Seleksi untuk mendapatkan dua orang tua
            parent1, parent2 = ga.selection()

            # Cetak fitness score dari orang tua yang dipilih (opsional untuk debugging)
            print("Parent 1 Fitness Score:", ObjectiveFunction(parent1).calculate())
            print("Parent 2 Fitness Score:", ObjectiveFunction(parent2).calculate())
            
            # Menghasilkan keturunan melalui adaptive crossover
            offspring1 = ga.adaptive_crossover(parent1, parent2, generation, max_generations)
            offspring2 = ga.adaptive_crossover(parent1, parent2, generation, max_generations)
            
            # Tambahkan offspring ke populasi baru
            new_population.extend([offspring1, offspring2])

        # Ganti populasi lama dengan populasi baru
        ga.population = new_population
        
        # Evaluasi populasi baru
        ga.evaluate_population()
        
        # Cetak fitness score dari generasi baru
        print("Fitness Scores for New Population:")
        for i, (cube, fitness_score) in enumerate(ga.fitness_scores):
            print(f"Cube {i+1} Fitness Score: {fitness_score}")

    # print("Initial Population Fitness Scores:")
    # for i, (cube, fitness_score) in enumerate(fitness_scores):
    #     print(f"Cube {i+1} Fitness Score: {fitness_score}")
    #     cube.display()
    #     print("\n")

    print("\nFinal Population after Evolution:")
    for i, (cube, fitness_score) in enumerate(ga.fitness_scores):
        print(f"Cube {i+1} Fitness Score: {fitness_score}")
        cube.display()

        


    
    



    
