SRC=nbody-block-mod.cu
EXE=nbody-block-mod

module load cuda/10.0
module load gcc/7.3.0


nvcc -arch=sm_35 -ftz=true -I../ -o $EXE $SRC -DSHMOO

echo $EXE

K=1024
for i in {1..10}
do
    ./$EXE $K
    K=$(($K*2))
done

