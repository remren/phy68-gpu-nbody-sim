#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <fstream>
#include "timer.h"

#define BLOCK_SIZE 256
#define SOFTENING 1e-9f

typedef struct { float4 *pos, *vel; } BodySystem;

void save_positions(const float4* positions, int nBodies, int timestep, FILE* file) {
    fwrite(&timestep, sizeof(int), 1, file);
    for (int i = 0; i < nBodies; i++) {
        fwrite(&positions[i].x, sizeof(float), 3, file); // Save only x,y,z
    }
}

void randomizeBodies(float *data, int n) {
    for (int i = 0; i < n; i += 4) {
        data[i] = 2.0f * (rand() / (float)RAND_MAX) - 1.0f;
        data[i + 1] = 2.0f * (rand() / (float)RAND_MAX) - 1.0f;
        data[i + 2] = 2.0f * (rand() / (float)RAND_MAX) - 1.0f;
        data[i + 3] = 1.0f;
    }
    // Make the 0 element mass larger than others.
    data[3] = 10000000.0f;
}

__global__
void bodyForce(float4 *p, float4 *v, float dt, int n) {
    int i = blockDim.x * blockIdx.x + threadIdx.x;
    if (i < n) {
        float Fx = 0.0f; float Fy = 0.0f; float Fz = 0.0f;

        for (int tile = 0; tile < gridDim.x; tile++) {
            __shared__ float3 spos[BLOCK_SIZE];
            float4 tpos = p[tile * blockDim.x + threadIdx.x];
            spos[threadIdx.x] = make_float3(tpos.x, tpos.y, tpos.z);
            __syncthreads();

            for (int j = 0; j < BLOCK_SIZE; j++) {
                float dx = spos[j].x - p[i].x;
                float dy = spos[j].y - p[i].y;
                float dz = spos[j].z - p[i].z;
                float distSqr = dx*dx + dy*dy + dz*dz + SOFTENING;
                float invDist = rsqrtf(distSqr);
                float invDist3 = invDist * invDist * invDist;

                Fx += dx * invDist3 * tpos.w;
                Fy += dy * invDist3 * tpos.w;
                Fz += dz * invDist3 * tpos.w;
            }
            __syncthreads();
        }

        v[i].x += dt*Fx; v[i].y += dt*Fy; v[i].z += dt*Fz;
    }
}

int main(const int argc, const char** argv) {
    int nBodies = 100;
    if (argc > 1) nBodies = atoi(argv[1]);

    const float dt = 0.01f;
    const int nIters = 1000;

    int bytes = 2*nBodies*sizeof(float4);
    float *buf = (float*)malloc(bytes);
    BodySystem p = { (float4*)buf, ((float4*)buf) + nBodies };

    randomizeBodies(buf, 8*nBodies);

    float *d_buf;
    cudaMalloc(&d_buf, bytes);
    BodySystem d_p = { (float4*)d_buf, ((float4*)d_buf) + nBodies };

    int nBlocks = (nBodies + BLOCK_SIZE - 1) / BLOCK_SIZE;
    double totalTime = 0.0;

    // Open output file
    FILE* output_file = fopen("large_mass_particle_positions.bin", "wb");
    if (!output_file) {
        printf("Error opening output file!\n");
        return 1;
    }

    // Write header (nBodies, nIters, nMasses)
    fwrite(&nBodies, sizeof(int), 1, output_file);
    fwrite(&nIters, sizeof(int), 1, output_file);
    for (int i = 0; i < 8*nBodies; i += 4) {
        fwrite(&buf[i + 3], sizeof(float), 1, output_file); // save all masses (+ 3 is w struct field), same logic as randomizeBodies
    }

    for (int iter = 1; iter <= nIters; iter++) {
        StartTimer();

        cudaMemcpy(d_buf, buf, bytes, cudaMemcpyHostToDevice);
        bodyForce<<<nBlocks, BLOCK_SIZE>>>(d_p.pos, d_p.vel, dt, nBodies);
        cudaMemcpy(buf, d_buf, bytes, cudaMemcpyDeviceToHost);

        for (int i = 0; i < nBodies; i++) {
            p.pos[i].x += p.vel[i].x*dt;
            p.pos[i].y += p.vel[i].y*dt;
            p.pos[i].z += p.vel[i].z*dt;
        }

        // Save positions for this timestep
        save_positions(p.pos, nBodies, iter, output_file);

        const double tElapsed = GetTimer() / 1000.0;
        if (iter > 1) {
            totalTime += tElapsed;
        }
#ifndef SHMOO
        printf("Iteration %d: %.3f seconds\n", iter, tElapsed);
#endif
    }

    fclose(output_file);
    double avgTime = totalTime / (double)(nIters-1);

#ifdef SHMOO
    printf("%d Bodies, %d Iterations, average of %0.3f Billion Interactions / sec, totalTime=%f\n",
           nBodies, nIters, 1e-9 * nBodies * nBodies / avgTime, totalTime);
#else
    printf("Average rate: %.3f Billion Interactions / second\n",
           1e-9 * nBodies * nBodies / avgTime);
#endif

    free(buf);
    cudaFree(d_buf);
    return 0;
}