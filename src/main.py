from algorithm.genetic_algorithm.GeneticAlgorithm import GeneticAlgorithm
from cube.objective_function import ObjectiveFunction
from algorithm.hill_climbing.SteepestAscent import SteepestAscent



def main_menu():
    while True:
        # Tampilkan menu opsi
        print("\nPilih algoritma yang ingin dicoba:")
        print("1. Steepest Ascent Hill-Climbing")
        print("2. Hill-Climbing with Sideways Move")
        print("3. Random Restart Hill-Climbing")
        print("4. Stochastic Hill-Climbing")
        print("5. Simulated Annealing")
        print("6. Genetic Algorithm")
        print("7. Keluar dari program")

        # Menerima input opsi dari pengguna
        pilihan = input("Masukkan nomor opsi (1-7): ")

        # Menentukan aksi berdasarkan input
        if (pilihan == '1'):
            print("\nAlgoritma Steepest Ascent Hill-Climbing belum terimplementasi.")
        elif (pilihan == '2'):
            print("\nAlgoritma Hill Climbing with Sideways Move belum terimplementasi.")
        elif (pilihan == '3'):
            print("\nAlgoritma Random Restart Hill-Climbing belum terimplementasi.")
        elif (pilihan == '4'):
            print("\nAlgoritma Stochastic Hill-Climbing belum terimplementasi.")
        elif (pilihan == '5'):
            #implementasi fungsi run untuk simmulated annealing
            print("\nAlgoritma Simulated Annealing belum terimplementasi.")
        elif (pilihan == '6'):
            print("\nAnda memilih Genetic Algorithm.")
            try:
                # Menerima input variasi jumlah populasi
                print("\nMasukkan 3 variasi jumlah populasi (misalnya: 30 50 100)")
                population_input = input("Variasi populasi (pisahkan dengan spasi): ").split()
                populations = [int(x) for x in population_input]

                # Menerima input variasi jumlah iterasi
                print("\nMasukkan 3 variasi jumlah iterasi (misalnya: 100 200 300)")
                iterations_input = input("Variasi iterasi (pisahkan dengan spasi): ").split()
                iterations = [int(x) for x in iterations_input]

                # Jalankan pengujian untuk variasi jumlah iterasi dengan populasi tetap
                print("\nMenjalankan pengujian dengan 3 variasi jumlah populasi dan 3 variasi jumlah iterasi:")
                for pop_size in populations:
                    for iterasi in iterations:
                        print(f"\nMenjalankan GA dengan {pop_size} populasi dan {iterasi} iterasi:")

                        # Ulangi setiap kombinasi sebanyak 3 kali
                        for i in range(3):
                            print(f"\nUji ke-{i + 1} untuk populasi {pop_size} dan iterasi {iterasi}:")
                            GeneticAlgorithm.run_genetic_algorithm(pop_size, iterasi, 0.05)

            except ValueError:
                print("Input harus berupa angka yang valid!")

        elif (pilihan == '7'):
            print("\nTerima kasih telah menggunakan program ini. Sampai jumpa!")
            break
        else:
            print("\nPilihan tidak valid. Silakan masukkan nomor opsi yang benar (1-7).")

# Panggilan fungsi main
if __name__ == "__main__":
    main_menu()
    

    print("=================END==================")


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
