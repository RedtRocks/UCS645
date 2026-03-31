# Assignment 5 - MPI Part II (C++)

This folder contains C++ MPI solutions for all Assignment 5 questions.

## Files

- `q1_daxpy.cpp` - DAXPY operation with serial vs MPI timing, speedup, and efficiency
- `q2_broadcast_race.cpp` - Linear `MyBcast` vs `MPI_Bcast` timing comparison
- `q3_distributed_dot_product.cpp` - Distributed dot product using `MPI_Bcast` + `MPI_Reduce`
- `q4_master_slave_primes.cpp` - Master-slave prime search up to a max value
- `q5_master_slave_perfect_numbers.cpp` - Master-slave perfect number search up to a max value
- `Makefile` - Build and quick run targets
- `run_tests.sh` - Automated timing suite (Q1-Q3) + functional checks (Q4-Q5)
- `analyze_results.py` - Table + graph generation from timing CSV

## Build

```bash
make clean
make
```

## Run Individual Questions

```bash
mpirun -np 4 ./q1_daxpy
mpirun -np 4 ./q2_broadcast_race
mpirun -np 4 ./q3_distributed_dot_product 1.0
mpirun -np 4 ./q4_master_slave_primes 1000
mpirun -np 4 ./q5_master_slave_perfect_numbers 10000
```

## Full Test + Analysis Workflow

```bash
chmod +x run_tests.sh
./run_tests.sh
python3 analyze_results.py
```

Outputs:

- `timing_results_q5.csv` - Timing/speedup/efficiency table data
- `q1_daxpy_scaling.png` - Q1 time + speedup plots
- `q2_broadcast_race.png` - Q2 linear broadcast vs MPI_Bcast comparison
- `q3_dot_product_scaling.png` - Q3 time/speedup/efficiency plots
- `q4_output.txt` - Q4 program output capture
- `q5_output.txt` - Q5 program output capture

## Suggested Process Counts

- Q1: `1, 2, 4, 8`
- Q2: `2, 4, 8, 16`
- Q3: `1, 2, 4, 8`
- Q4/Q5: `4` (functional demonstration)

## Notes

- Q2 uses 10 million doubles by default (~80 MB per process). You can reduce by passing an argument:
  `mpirun -np 4 ./q2_broadcast_race 2000000`
- Q3 avoids allocating full vectors by generating local values on-the-fly in each rank.
