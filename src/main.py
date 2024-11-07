from algorithm.genetic_algorithm.GeneticAlgorithm import GeneticAlgorithm
from cube.objective_function import ObjectiveFunction
from algorithm.hill_climbing.SteepestAscent import SteepestAscent



if __name__ == "__main__":
    population_size = 5
    max_generations = 5
    mutation_rate = 0.05

    ga = GeneticAlgorithm(population_size, max_generations, mutation_rate)

    # fitness_scores = ga.evaluate_population()

    ga.evaluate_population()

    print("Initial Fitness Scores for Entire Population:")
    for i, (cube, fitness_score) in enumerate(ga.fitness_scores):
        print(f"Cube {i+1} Fitness Score: {fitness_score}")
        # cube.display()

    for generation in range(max_generations):
        new_population = []
        
        print(f"\n--- Generation {generation} ---")
        for _ in range(population_size // 2):  # Lakukan crossover hingga populasi penuh
            # Seleksi untuk mendapatkan dua orang tua
            parent1, parent2 = ga.selection()

            # Cetak fitness score dari orang tua yang dipilih (opsional untuk debugging)
            print("\nParent 1 Fitness Score:", ObjectiveFunction(parent1).calculate())
            # parent1.display()
            print("Parent 2 Fitness Score:", ObjectiveFunction(parent2).calculate())
            # parent2.display()
            
            # Menghasilkan keturunan melalui adaptive crossover
            offspring1, offspring2 = ga.adaptive_crossover_pair(parent1, parent2, generation, max_generations)

            print("SEBELUM MUTATION")
            print("\nOffspring 1:", ObjectiveFunction(offspring1).calculate())
            
            print("Offspring 2:", ObjectiveFunction(offspring2).calculate())

            # Melakukan adaptive mutation pada offspring
            offspring1 = ga.adaptive_mutation(offspring1, generation, max_generations)
            offspring2 = ga.adaptive_mutation(offspring2, generation, max_generations)
            
            print("SETELAH MUTATION")
            print("\nOffspring 1:", ObjectiveFunction(offspring1).calculate())
            # offspring1.display()
            print("Offspring 2:", ObjectiveFunction(offspring2).calculate())
            # offspring2.display()

            # Tambahkan offspring ke populasi baru
            new_population.extend([offspring1, offspring2])

        if len(new_population) < population_size:
            parent1, parent2 = ga.selection()
            print("\nParent 1 Fitness Score (extra):", ObjectiveFunction(parent1).calculate())
            # parent1.display()
            print("Parent 2 Fitness Score (extra):", ObjectiveFunction(parent2).calculate())
            # parent2.display()
            extra_offspring, _ = ga.adaptive_crossover_pair(parent1, parent2, generation, max_generations)
            print("SEBELUM MUTATION")
            print("\nExtra Offspring:", ObjectiveFunction(extra_offspring).calculate())
            extra_offspring = ga.adaptive_mutation(extra_offspring, generation, max_generations)
            print("SETELAH MUTATION")
            print("\nExtra Offspring:", ObjectiveFunction(extra_offspring).calculate())
            # extra_offspring.display()
            new_population.append(extra_offspring)

        # Ganti populasi lama dengan populasi baru
        ga.population = new_population
        
        # Evaluasi populasi baru
        ga.evaluate_population()
        
        # Cetak fitness score dari generasi baru
        print("\nFitness Scores for New Population:")
        for i, (cube, fitness_score) in enumerate(ga.fitness_scores):
            print(f"Cube {i+1} Fitness Score: {fitness_score}")

    # print("Initial Population Fitness Scores:")
    # for i, (cube, fitness_score) in enumerate(fitness_scores):
    #     print(f"Cube {i+1} Fitness Score: {fitness_score}")
    #     cube.display()
    #     print("\n")

    print("===================================")
    # print("\nFinal Population after Evolution:")
    # for i, (cube, fitness_score) in enumerate(ga.fitness_scores):
    #     print(f"Cube {i+1} Fitness Score: {fitness_score}")
    #     cube.display()

    # # Initialize the Magic Cube
    # initial_cube = MagicCube()

    # # Display the initial state
    # print("Initial Cube State:")
    # initial_cube.display()
    # initial_score = ObjectiveFunction(initial_cube).calculate()
    # print("Initial Score:", initial_score)

    # # Run Steepest Ascent Hill Climbing with the initial cube
    # hc = SteepestAscent(initial_cube)
    # final_state = hc.evaluateNeighbor()
    # final_score = ObjectiveFunction(final_state).calculate()

    # # Display final state and score
    # print("\nFinal Cube State After Steepest Ascent Hill Climbing:")
    # final_state.display()
    # print("Final Score:", final_score)
