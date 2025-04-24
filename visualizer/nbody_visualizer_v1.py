from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
import pyqtgraph.opengl as gl
import numpy as np
import position_loader as pl

app = QApplication([])
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('Persistent Scatter Plot Example')
w.setCameraPosition(distance=40)

numIters = 100

# Add grid
g = gl.GLGridItem()
w.addItem(g)

# # Old example code from generated_scatterplot_ex1.py
# # Generate initial positions (100 points for each of 10 scatter plots)
pos = np.random.uniform(-10, 10, size=(100, 10, 3))
pos[:, :, 2] = np.abs(pos[:, :, 2])  # Ensure z is positive

# load initial positions of points from data
loader = pl.ParticleDataLoader("ex_particle_positions.bin")
frame_0 = loader.get_frame(0)  # Get positions at timestep 10
print(f'test:{frame_0}')

# Create and store scatter plot items
ScatterPlotItems = {}
for point in range(10):
    # Initialize with consistent color and size
    ScatterPlotItems[point] = gl.GLScatterPlotItem(
        # pos=pos[:, point, :],
        pos = frame_0,
        color=(1, 0, 0.5, 0.8),  # RGBA - purple with slight transparency
        size=7,  # Slightly larger size
        pxMode=True,
        glOptions='opaque'  # Ensure points are rendered properly, i don't know why transparency fails on my machine.
    )
    w.addItem(ScatterPlotItems[point])

# Initialize colors with consistent opacity
color = np.zeros((pos.shape[0], 10, 4), dtype=np.float32)
color[:, :, 0] = 1  # Red channel
color[:, :, 1] = 0  # Green channel
color[:, :, 2] = 0.5  # Blue channel
color[:, :, 3] = 0.8  # Alpha channel (consistent opacity)

global iter
iter = 0
def update():
    # global color
    # # Create a copy of colors to modify
    # new_color = color.copy()
    #
    # # Create pulsing effect without making points disappear
    # phase = QTimer().remainingTime() % 2000 / 2000  # 2 second cycle
    # pulse = 0.3 + 1 * (1 + np.sin(2 * np.pi * phase))  # 0.3-0.8 opacity range
    #
    # # Apply pulse to all points
    # new_color[:, :, 3] = pulse
    #
    # # Update colors for all scatter plots
    # for point in range(10):
    #     ScatterPlotItems[point].setData(color=new_color[:, point, :])
    global iter
    if iter > numIters:
        iter = 0
    else:
        iter += 1

    pos_new = loader.get_frame(iter)
    for point in range(100):
        ScatterPlotItems[point].setData(pos=pos_new)



# # In the update function:
# def update():
#     global color
#     # Create varying opacity that never goes to zero
#     phase = QTimer().remainingTime() % 1000 / 1000
#     for i in range(10):
#         pulse = 0.5 + 0.3 * np.sin(2 * np.pi * phase + i * 0.2)
#         color[:, i, 3] = pulse
#
#     for point in range(10):
#         ScatterPlotItems[point].setData(color=color[:, point, :])


t = QTimer()
t.timeout.connect(update)
t.start(30)  # Faster updates for smoother animation

if __name__ == '__main__':
    app.exec_()