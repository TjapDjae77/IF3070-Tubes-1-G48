import numpy as np

class ObjectiveFunction:
    def __init__(self, magic_cube):
        self.magic_cube = magic_cube
        self.size = magic_cube.size
        self.magic_number = magic_cube.magic_number
    
    def calculate(self):
        cube = self.magic_cube.cube
        total_error = 0

        for i in range(self.size):
            for j in range(self.size):
                # Jumlah error di baris tiap layer
                total_error += abs(np.sum(cube[i, j, :]) - self.magic_number)
    
                # Jumlah error di kolom tiap layer
                total_error += abs(np.sum(cube[i, :, j]) - self.magic_number)
    
                # Jumlah error di tiang tiap layer
                total_error += abs(np.sum(cube[:, i, j]) - self.magic_number)

        # Diagonal bidang pada layer horizontal
        for i in range(self.size):
            horizontal_diag_1 = np.sum(np.diag(cube[i]))
            horizontal_diag_2 = np.sum(np.diag(np.fliplr(cube[i])))
            total_error += abs(horizontal_diag_1 - self.magic_number)
            total_error += abs(horizontal_diag_2 - self.magic_number)

        # Diagonal menyilang horizontal dari depan ke belakang di tiap baris
        for j in range(self.size):
            front_back_diag_1 = np.sum([cube[i, j, i] for i in range(self.size)])
            front_back_diag_2 = np.sum([cube[i, j, self.size - 1 - i] for i in range(self.size)])
            total_error += abs(front_back_diag_1 - self.magic_number)
            total_error += abs(front_back_diag_2 - self.magic_number)

        # Diagonal menyilang vertikal dari sisi kiri ke kanan di tiap kolom
        for k in range(self.size):
            left_right_diag_1 = np.sum([cube[i, i, k] for i in range(self.size)])
            left_right_diag_2 = np.sum([cube[i, self.size - 1 - i, k] for i in range(self.size)])
            total_error += abs(left_right_diag_1 - self.magic_number)
            total_error += abs(left_right_diag_2 - self.magic_number)

        # Jumlah error diagonal ruang kubus
        total_error += abs(np.sum([cube[i, i, i] for i in range(self.size)]) - self.magic_number)
        total_error += abs(np.sum([cube[i, i, self.size - 1 - i] for i in range(self.size)]) - self.magic_number)
        total_error += abs(np.sum([cube[i, self.size - 1 - i, i] for i in range(self.size)]) - self.magic_number)
        total_error += abs(np.sum([cube[self.size - 1 - i, i, i] for i in range(self.size)]) - self.magic_number)

        return total_error

