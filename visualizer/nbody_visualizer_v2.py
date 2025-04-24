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
loader = pl.ParticleDataLoader("first_large_mass_particle_positions.bin")
current_frame = 0
total_frames = loader.nIters  # Assuming your loader has nIters property

# Create initial scatter plot
scatter = gl.GLScatterPlotItem(
    pos=loader.get_frame(0),
    color=(1, 0, 0.5, 0.8),  # Initial color (purple with transparency)
    size=7,
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

    # Update window title with frame info
    w.setWindowTitle(f'Particle Animation Visualizer - Frame {current_frame}/{total_frames}')


# Set up animation timer
t = QTimer()
t.timeout.connect(update)
t.start(30)  # ~33 FPS

if __name__ == '__main__':
    app.exec_()