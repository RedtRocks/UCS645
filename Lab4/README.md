# Assignment 4 - MPI Exercises

This folder contains complete solutions for the four laboratory exercises.

## Files

- `q1_ring_comm.cpp`: Ring communication with value passing and rank addition
- `q2_array_sum.cpp`: Parallel sum of array `[1..100]` with average
- `q3_max_min.cpp`: Global max/min across random values with source process
- `q4_dot_product.cpp`: Parallel dot product of two fixed vectors
- `Makefile`: Build and run helpers

## Build

```bash
make
```

## Run

```bash
make run-q1
make run-q2
make run-q3
make run-q4
```

Or directly:

```bash
mpirun -np 4 ./q1_ring_comm
mpirun -np 4 ./q2_array_sum
mpirun -np 4 ./q3_max_min
mpirun -np 4 ./q4_dot_product
```
