# phy68-gpu-nbody-sim
Run with: srun -p preempt --gres=gpu:1 --pty bash shmoo-cuda-nbody-block.sh

Simulation code from: https://github.com/harrism/mini-nbody
Adapted to run on the Tufts HPC, modified (under Apache 2.0 License) to have simulation account for masses, as well as
saving data to a file (inefficiently) to pass to the visualizer.