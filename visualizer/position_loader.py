import numpy as np
import os


class ParticleDataLoader:
    def __init__(self, filename):
        self.file = open(filename, 'rb')
        self.nBodies = np.frombuffer(self.file.read(4), dtype=np.int32)[0]
        self.nIters = np.frombuffer(self.file.read(4), dtype=np.int32)[0]
        self.current_frame = 0

    def get_frame(self, frame_num):
        if frame_num >= self.nIters:
            return None

        self.file.seek(8 + frame_num * (4 + self.nBodies * 3 * 4))  # Header + previous frames
        timestep = np.frombuffer(self.file.read(4), dtype=np.int32)[0]
        data = np.frombuffer(self.file.read(self.nBodies * 3 * 4),
                             dtype=np.float32).reshape(-1, 3)
        return data

    def close(self):
        self.file.close()


# Usage example:
if __name__ == '__main__':
    loader = ParticleDataLoader("ex_particle_positions.bin")
    frame_10 = loader.get_frame(10)  # Get positions at timestep 10
    print(f'test:{frame_10}')
    loader.close()