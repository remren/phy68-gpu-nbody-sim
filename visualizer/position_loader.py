import numpy as np
import os


class ParticleDataLoader:
    def __init__(self, filename):
        self.file = open(filename, 'rb')
        self.nBodies = np.frombuffer(self.file.read(4), dtype=np.int32)[0]
        self.nIters = np.frombuffer(self.file.read(4), dtype=np.int32)[0]
        self.nMasses = np.empty(shape=self.nBodies, dtype=np.float32)
        for i in range(self.nBodies):
            self.nMasses[i] = np.frombuffer(self.file.read(4), dtype=np.float32)[0]
        self.current_frame = 0

    def get_frame(self, frame_num):
        if frame_num >= self.nIters:
            return None

        # logic for seeking coordinate data
        #   lol
        #
        # self.file.seek(8 + (4 * self.nBodies * 2 - 4) + frame_num * (4 + self.nBodies * 3 * 4))  # If mass data is in header
        self.file.seek(8 + frame_num * (4 + self.nBodies * 3 * 4)) # Header + previous frames (+ 8 due to )
        timestep = np.frombuffer(self.file.read(4), dtype=np.int32)[0]
        data = np.frombuffer(self.file.read(self.nBodies * 3 * 4),
                             dtype=np.float32).reshape(-1, 3)
        return data

    def close(self):
        self.file.close()


# Usage example:
if __name__ == '__main__':
    # loader = ParticleDataLoader("large_mass_particle_positions.bin")
    # 0.6357
    # 1.4012985e-45
    # 66
    # loader = ParticleDataLoader("mass_test_particle_positions.bin")
    loader = ParticleDataLoader("mt4_mass_particle_positions.bin")
    frame_0 = loader.get_frame(0)  # Get positions at timestep 0
    loader.close()

    # for i in range(loader.nBodies):
    #     for j in range(3):
    #         if frame_0[i][j] != 1.0:
    #             print(f'starting i: {i}, {j}')

    print(f'test masses: {loader.nMasses}')
    # print(f'test:{frame_0}')