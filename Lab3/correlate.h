#ifndef CORRELATE_H
#define CORRELATE_H

// Version 1: Sequential baseline implementation
void correlate_sequential(int ny, int nx, const float* data, float* result);

// Version 2: OpenMP parallelized implementation
void correlate_openmp(int ny, int nx, const float* data, float* result, int num_threads);

// Version 3: Highly optimized implementation with vectorization
void correlate_optimized(int ny, int nx, const float* data, float* result, int num_threads);

#endif // CORRELATE_H
