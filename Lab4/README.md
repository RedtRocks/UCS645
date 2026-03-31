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

## Performance Analysis (Graphs & Tables)

To generate timing comparisons across different processor counts:

1. **Run all tests** (tests 1, 2, 4, and 8 processes)

   ```bash
   chmod +x run_tests.sh
   ./run_tests.sh
   ```

   This creates `timing_results.csv` with execution times, speedup, and efficiency.

2. **Generate graphs and tables**

   ```bash
   python3 analyze_results.py
   ```

   Generates:
   - `execution_times.png` — Time vs processor count
   - `speedup.png` — Speedup vs processor count (with ideal line)
   - `efficiency.png` — Parallel efficiency %
   - `comparison_bars.png` — Side-by-side bar charts

3. **View CSV directly**
   ```bash
   cat timing_results.csv
   ```

### What to Look For

- **q2_array_sum & q4_dot_product** → Should show better scaling (low communication overhead)
- **q1_ring_comm & q3_max_min** → Communication-bound; less ideal scaling
- **Efficiency** → Aim for >70% at 2–4 processes
