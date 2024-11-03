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
    

        # Jumlah error di diagonal bidang tiap layer
        for i in range(self.size):
            total_error += abs(np.sum(np.diag(cube[i])) - self.magic_number)

            total_error += abs(np.sum(np.diag(np.fliplr(cube[i]))) - self.magic_number)


        # Jumlah error diagonal ruang kubus
        total_error += abs(np.sum([cube[i, i, i] for i in range(self.size)]) - self.magic_number)
        total_error += abs(np.sum([cube[i, i, self.size - 1 - i] for i in range(self.size)]) - self.magic_number)
        total_error += abs(np.sum([cube[i, self.size - 1 - i, i] for i in range(self.size)]) - self.magic_number)
        total_error += abs(np.sum([cube[self.size - 1 - i, i, i] for i in range(self.size)]) - self.magic_number)

        return total_error

