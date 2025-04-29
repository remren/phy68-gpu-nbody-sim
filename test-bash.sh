SRC=nbody-block-mod.cu
EXE=test-nbody-block-mod

module load cuda/10.0
module load gcc/7.3.0


nvcc -arch=sm_35 -ftz=true -I../ -o $EXE $SRC -DSHMOO

echo $EXE

K=131072

./$EXE $K
