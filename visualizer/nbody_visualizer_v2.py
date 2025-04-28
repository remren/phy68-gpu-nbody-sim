from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
import pyqtgraph.opengl as gl
import numpy as np
import position_loader as pl

app = QApplication([])
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('Particle Animation Visualizer')
w.setCameraPosition(distance=10)

# Add grid
g = gl.GLGridItem()
w.addItem(g)

# Load particle data
# loader = pl.ParticleDataLoader("mass_test_particle_positions.bin")
loader = pl.ParticleDataLoader("mt4_mass_particle_positions.bin")
current_frame = 0
total_frames = loader.nIters  # Assuming your loader has nIters property
total_bodies = loader.nBodies
total_masses = loader.nMasses

color_bodies = np.empty((total_bodies, 4))
for i in range(total_bodies):
    color_bodies[i] = (1, 0, 0.5, 0.8)

color_bodies[0] = (0, 1, 0, 0.8) # set the first body to green
size_bodies = np.empty(total_bodies)
for i in range(total_bodies):
    size_bodies[i] = 1.5 * total_masses[i] / 1e9
size_bodies[0] = 15

# Create initial scatter plot
scatter = gl.GLScatterPlotItem(
    pos=loader.get_frame(0),
    # color=(1, 0, 0.5, 0.8),  # Initial color
    color=color_bodies,
    # size=7,
    size=size_bodies,
    pxMode=True,
    glOptions='opaque'
)
w.addItem(scatter)



def update():
    global current_frame

    # Get next frame's positions
    current_frame = (current_frame + 1) % total_frames
    new_positions = loader.get_frame(current_frame)

    # Update both positions and colors
    scatter.setData(pos=new_positions)

    # Update Window
    w.setCameraPosition(distance=6 + 10 * current_frame / total_frames)

    # Update window title with frame info
    w.setWindowTitle(f'Particle Animation Visualizer - Frame {current_frame}/{total_frames}')


# Set up animation timer
t = QTimer()
t.timeout.connect(update)
t.start(30)  # ~33 FPS

if __name__ == '__main__':
    app.exec_()
    loader.close()