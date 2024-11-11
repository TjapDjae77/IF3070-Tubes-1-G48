from algorithm.genetic_algorithm.GeneticAlgorithm import GeneticAlgorithm
from cube.objective_function import ObjectiveFunction
from cube.magic_cube import MagicCube
from algorithm.hill_climbing.SteepestAscent import SteepestAscent
from algorithm.hill_climbing.RandomRestart import RandomRestart
from algorithm.simulated_annealing.SimulatedAnnealing import SimulatedAnnealing
from algorithm.hill_climbing.Sideway import SidewayHillClimbing
from algorithm.hill_climbing.Stochastic import StochasticHillClimbing
from ascii import print_dual_color_ascii, print_loading_animation
import time


def main_menu():
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
    while True:


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
            print("\nAnda memilih Steepest Ascent Hill-Climbing.")
            print("\nMemulai Steepest Ascent Hill Climbing")
    
            initial_cube = MagicCube()
            sa = SteepestAscent(magic_cube=initial_cube)
            
            print(f"\nState Awal:")
            sa.current_state.display()
            
            start_time = time.time()

            total_iteration = sa.evaluateNeighbor()

            elapsed_time = time.time() - start_time

            print(f"\nState Akhir:")
            sa.current_state.display()
            print(f"\nFinal Objective Value: {sa.current_value}")
            print(f"Total Iterasi: {total_iteration}")
            print(f"Waktu: {elapsed_time:.2f} detik")

            SteepestAscent.plot_progression(
                objective_values=sa.objective_values,
                title=f'Perkembangan Nilai Objective Function\nWaktu: {elapsed_time:.2f} detik'
            )

        elif (pilihan == '2'):
            print("\nAnda memilih Hill-Climbing with Sideways Move")
            try:
                ms = int(input("Masukkan variasi maksimal sideway moves: "))
                print(f"\nMenjalankan pengujian dengan berbagai variasi jumlah maksimal {ms} sideway moves:")

                print_dual_color_ascii(cube, 2)
                print_loading_animation("Proses solving magic cube")
                                
                shc = SidewayHillClimbing(max_sideways_moves=ms)
                            
            except ValueError:
                print("Input harus berupa angka yang valid!")
        elif (pilihan == '3'):
            print("\nAnda memilih Random Restart Hill-Climbing.")
            try:
                print("\nMasukkan jumlah maksimal restart (misalnya: 10):")
                max_restart = int(input("Jumlah maksimal restart: "))

                print(f"\nMemulai Random Restart Hill Climbing dengan maksimak restart {max_restart}")
                
                rr = RandomRestart(max_restarts=max_restart)
                elapsed_time = rr.randomRestart()

                print(f"\nState Akhir:")
                rr.best_state.display()
                print(f"\nNilai objective akhir: {rr.best_value}")
                print(f"Waktu yang dibutuhkan: {elapsed_time:.2f} detik\n")

                RandomRestart.show_plot(
                    objective_values=rr.objective_values,
                    max_restarts=len(rr.objective_values),
                    title=f'Perkembangan Nilai Objective Function (Maks Restart = {max_restart})\nWaktu: {elapsed_time:.2f} detik'
                )
            except ValueError:
                print("Input harus berupa angka yang valid!")

        elif (pilihan == '4'):
            print("\nAnda memilih Algoritma Stochastic Hill-Climbing")
            try:
                maximum_iteration = int(input("Jumlah maksimal iterasi: "))

                print(f"\nPengujian dengan maksimal {maximum_iteration} iterasi:")

                print_dual_color_ascii(cube, 2)
                print_loading_animation("Proses solving magic cube")

                shc = StochasticHillClimbing(max_iteration=maximum_iteration)
                
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
