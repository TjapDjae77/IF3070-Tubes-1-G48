from algorithm.genetic_algorithm.GeneticAlgorithm import GeneticAlgorithm
from algorithm.hill_climbing.SteepestAscent import SteepestAscent
from algorithm.hill_climbing.RandomRestart import RandomRestart
from algorithm.simulated_annealing.SimulatedAnnealing import SimulatedAnnealing
from algorithm.hill_climbing.Sideway import SidewayHillClimbing
from algorithm.hill_climbing.Stochastic import StochasticHillClimbing
from ascii import print_dual_color_ascii, print_loading_animation

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

            print_dual_color_ascii(cube, 2)
            print_loading_animation("Proses solving magic cube")
    
            sa = SteepestAscent()
            sa.evaluateNeighbor()

        elif (pilihan == '2'):
            print("\nAnda memilih Hill-Climbing with Sideways Move")
            try:
                ms = int(input("Masukkan variasi maksimal sideway moves: "))
                print(f"\nMenjalankan pengujian dengan berbagai variasi jumlah maksimal {ms} sideway moves:")

                print_dual_color_ascii(cube, 2)
                print_loading_animation("Proses solving magic cube")
                                
                shc = SidewayHillClimbing(max_sideways_moves=ms)
                shc.evaluateNeighbor()
                            
            except ValueError:
                print("Input harus berupa angka yang valid!")
        elif (pilihan == '3'):
            print("\nAnda memilih Random Restart Hill-Climbing.")
            try:
                print("\nMasukkan jumlah maksimal restart (misalnya: 10):")
                max_restart = int(input("Jumlah maksimal restart: "))

                print(f"\nMenjalankan Random Restart Hill Climbing dengan maksimal restart {max_restart}")
                print_dual_color_ascii(cube, 2)
                print_loading_animation("Proses solving magic cube")

                rr = RandomRestart(max_restarts=max_restart)
                rr.randomRestart()

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
                shc.evaluateNeighbor()
                
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

            # Meminta input jumlah populasi dan iterasi menggunakan fungsi get_valid_input
            population_size = GeneticAlgorithm.get_valid_input(
                prompt="Masukkan jumlah populasi (contoh: 50, minimal 2): ",
                min_value=2,  # Populasi minimal 2 agar proses berjalan
                value_type="integer"
            )[0]  # Mengambil elemen pertama dari list hasil get_valid_input

            max_iteration = GeneticAlgorithm.get_valid_input(
                prompt="Masukkan jumlah iterasi (contoh: 100, minimal 1): ",
                min_value=1,  # Iterasi minimal 1
                value_type="integer"
            )[0]  # Mengambil elemen pertama dari list hasil get_valid_input

            GeneticAlgorithm.run(population_size, max_iteration)
                
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
