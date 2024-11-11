from algorithm.genetic_algorithm.GeneticAlgorithm import GeneticAlgorithm
from cube.objective_function import ObjectiveFunction
from algorithm.hill_climbing.SteepestAscent import SteepestAscent
from algorithm.simulated_annealing.SimulatedAnnealing import SimulatedAnnealing
from algorithm.hill_climbing.Sideway import SidewayHillClimbing
from algorithm.hill_climbing.Stochastic import StochasticHillClimbing
from ascii import print_dual_color_ascii, print_loading_animation


def main_menu():
    while True:
        print("==================================START===================================")

        ascii_header = """
    .------------------------------------------------------------.
    |███████╗███████╗██╗      █████╗ ███╗   ███╗ █████╗ ████████╗|
    |██╔════╝██╔════╝██║     ██╔══██╗████╗ ████║██╔══██╗╚══██╔══╝|
    |███████╗█████╗  ██║     ███████║██╔████╔██║███████║   ██║   |
    |╚════██║██╔══╝  ██║     ██╔══██║██║╚██╔╝██║██╔══██║   ██║   |
    |███████║███████╗███████╗██║  ██║██║ ╚═╝ ██║██║  ██║   ██║   |
    |╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   |
    |                                                            |
    |██████╗  █████╗ ████████╗ █████╗ ███╗   ██╗ ██████╗         |
    |██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗████╗  ██║██╔════╝         |
    |██║  ██║███████║   ██║   ███████║██╔██╗ ██║██║  ███╗        |
    |██║  ██║██╔══██║   ██║   ██╔══██║██║╚██╗██║██║   ██║        |
    |██████╔╝██║  ██║   ██║   ██║  ██║██║ ╚████║╚██████╔╝        |
    |╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝         |
    '------------------------------------------------------------'
        """

        print_dual_color_ascii(ascii_header, 3)

        print("=====================================================================")

        # Tampilkan menu opsi
        print("""
            +-------------------------------+
            |     PILIH ALGORITMA YANG      |
            |          INGIN DICOBA         |
            +-------------------------------+
        """)
        # print("\nPilih algoritma yang ingin dicoba:")
        print("1. Steepest Ascent Hill-Climbing")
        print("2. Hill-Climbing with Sideways Move")
        print("3. Random Restart Hill-Climbing")
        print("4. Stochastic Hill-Climbing")
        print("5. Simulated Annealing")
        print("6. Genetic Algorithm")
        print("7. Keluar dari program")

        # Menerima input opsi dari pengguna
        pilihan = input("Masukkan nomor opsi (1-7): ")

        cube = """
                        .....:::::....              
                ....::::::::----:::::::....       
            ...:::::::::-::::::::::::-:::::::::... 
            .+#*+=--::::::::::--:::::::::::--+*#=. 
            .+#######*+==-:::::::::::-==**######=. 
            .+#############*+=---=+**###########=. 
            .+##################################-. 
            .=####@%#######################%####-. 
            .=####%%####%%###########%#####%####-. 
            .=###########%%#########%%##########-. 
            .=#################################*:. 
            .=####%%######################%%###*:. 
            .=####%@%####%###########%###%@%###*:. 
          ...=##########%@%#########%%#########*:..
          ...=#################################*:..
          ....:-+###########################*=-:...
          .......:::=*##################*=::.......
          ............::-+*#########+-:::..........
              ..............:-++=:.................
        """

        # Menentukan aksi berdasarkan input
        if (pilihan == '1'):
            print("\nAlgoritma Steepest Ascent Hill-Climbing belum terimplementasi.")
        elif (pilihan == '2'):
            print("\nAnda memilih Hill-Climbing with Sideways Move")
            try:
                ms = int(input("Masukkan variasi maksimal sideway moves: "))
                print(f"\nMenjalankan pengujian dengan berbagai variasi jumlah maksimal {ms} sideway moves:")

                print_dual_color_ascii(cube, 2)
                print_loading_animation("Proses solving magic cube")
                                
                results = []
                shc = SidewayHillClimbing(max_sideways_moves=ms)

                print("\nState Awal:")
                shc.current_state.display()
                print(f"Nilai Objective Awal: {shc.current_value}")

                total_duration = shc.evaluateNeighbor()

                print(f"State Akhir:")
                shc.current_state.display()
                print(f"Nilai Objective Akhir: {shc.current_value}")

                print(f"Total search duration: {total_duration:.6f} seconds")
                print(f"Jumlah Iterasi: {shc.iterations}")

                results.append((shc.objective_values, f"Jumlah Sideway Moves: {ms}", total_duration))
                SidewayHillClimbing.plot_multiple_runs(results, title="Perbandingan objective function terhadap banyak iterasi yang telah dilewati menggunakan Sideways Hill-Climbing")
            
            except ValueError:
                print("Input harus berupa angka yang valid!")
        elif (pilihan == '3'):
            print("\nAlgoritma Random Restart Hill-Climbing belum terimplementasi.")
        elif (pilihan == '4'):
            print("\nAnda memilih Algoritma Stochastic Hill-Climbing")
            try:
                maximum_iteration = int(input("Variasi maksimal iterasi: "))

                print(f"\nPengujian dengan maksimal {maximum_iteration} iterasi:")

                print_dual_color_ascii(cube, 2)
                print_loading_animation("Proses solving magic cube")

                shc = StochasticHillClimbing(max_iteration=maximum_iteration)
                total_duration = shc.evaluateNeighbor()

                objective_values = shc.objective_values

                print("\nState Awal:")
                shc.current_state.display()
                print(f"Nilai Objective Awal: {shc.current_value}")

                total_duration = shc.evaluateNeighbor()

                print(f"State Akhir:")
                shc.current_state.display()
                print(f"Nilai Objective Akhir: {shc.current_value}")

                print(f"Total search duration: {total_duration:.6f} seconds")
                print(f"Jumlah Iterasi: {shc.max_iteration}")

                StochasticHillClimbing.plot_multiple_runs(
                    [(objective_values, f'Percobaan dengan {maximum_iteration} iterasi', total_duration)],
                    max_iteration=maximum_iteration,
                    title=f'Perbandingan objective function terhadap banyak iterasi yang telah dilewati menggunakan Stochastic Hill-Climbing'
                )
            except ValueError:
                print("Input harus berupa angka yang valid!")
        elif (pilihan == '5'):
            print("\nAnda memilih Simulated Annealing")
            try:
                # Menerima input nilai yang dibutuhkan
                starting_tem_input = int(input("Masukkan nilai temperatur awal (misalnya: 1000) : ")) 
                cooling_rate_input = float(input("Masukkan nilai cooling rate (misalnya: 0.95) : "))
                minimum_tem_input = float(input("Masukkan nilai temperatur minimal (misalnya: 0.1) : "))

                # Menjalankan algoritma sesuai dengan input
                print_dual_color_ascii(cube, 2)
                print_loading_animation("Proses solving magic cube")
                sa = SimulatedAnnealing(starting_tem_input, cooling_rate_input, minimum_tem_input) 
                sa.simulatedannealing()  

            except ValueError:
                print("Input harus berupa angka yang valid!")

        elif (pilihan == '6'):
            print("\nAnda memilih Genetic Algorithm.")

            print("\n===Pengujian dengan variasi jumlah populasi dan iterasi tetap===")
            populations = GeneticAlgorithm.get_valid_input("\nMasukkan 3 variasi jumlah populasi (misalnya: 30 50 100): ", min_value=2)
            iteration_fixed = GeneticAlgorithm.get_valid_input("Masukkan jumlah iterasi tetap (contoh: 100): ", min_value=1)[0]

            GeneticAlgorithm.run_multiple_tests(populations, [iteration_fixed], is_fixed_iteration=True)

            print("\n===Pengujian dengan variasi jumlah iterasi dan populasi tetap===")
            iterations = GeneticAlgorithm.get_valid_input("\nMasukkan 3 variasi jumlah iterasi (contoh: 50 100 150): ", min_value=1)
            population_fixed = GeneticAlgorithm.get_valid_input("Masukkan jumlah populasi tetap (contoh: 20): ", min_value=2)[0]
            
            GeneticAlgorithm.run_multiple_tests([population_fixed], iterations, is_fixed_iteration=False)
                
        elif (pilihan == '7'):
            print("\nTerima kasih telah menggunakan program ini. Sampai jumpa!")
            break
        else:
            print("\nPilihan tidak valid. Silakan masukkan nomor opsi yang benar (1-7).")

# Panggilan fungsi main
if __name__ == "__main__":
    main_menu()
    
    sayonara = """
    .--------------------------------------------------------------------.
    |███████╗ █████╗ ██╗   ██╗ ██████╗ ███╗   ██╗ █████╗ ██████╗  █████╗ |
    |██╔════╝██╔══██╗╚██╗ ██╔╝██╔═══██╗████╗  ██║██╔══██╗██╔══██╗██╔══██╗|
    |███████╗███████║ ╚████╔╝ ██║   ██║██╔██╗ ██║███████║██████╔╝███████║|
    |╚════██║██╔══██║  ╚██╔╝  ██║   ██║██║╚██╗██║██╔══██║██╔══██╗██╔══██║|
    |███████║██║  ██║   ██║   ╚██████╔╝██║ ╚████║██║  ██║██║  ██║██║  ██║|
    |╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝|
    '--------------------------------------------------------------------'     
    """
    print_dual_color_ascii(sayonara)

    print("===========================END===========================")


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
