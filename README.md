# phy68-gpu-nbody-sim
Run with: srun -p preempt --gres=gpu:1 --pty bash shmoo-cuda-nbody-block.sh

Or

Run with: ./standalone-test.sh to run a simulation with 131,000+ bodies for 1,000 iterations.

Simulation code from: https://github.com/harrism/mini-nbody
Adapted to run on the Tufts HPC, modified (under Apache 2.0 License) to have simulation account for masses, as well as
saving data to a file (inefficiently) to pass to the visualizer.

# File Structure
- All .bin files contain previous simulation data. They are ready to be used with the visualizer. The large N count .bin are not included.
- nbody_visualizer_v2.py: Visualizer for simulation data using PyQTGraph. Currently has a locked window zoom, can be changed. Requires position_loader.py
- position_loader.py: Loads all data from .bin files to be used in the visualizer.
- nbody-block-mod.cu: N-body GPU Simulation in CUDA. Requires timer.h
- timer.h: Allows simulation code to time itself.