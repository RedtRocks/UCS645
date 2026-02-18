# QUICK START GUIDE - Assignment 3

## For Linux/Mac Users (with make)

### 1. Build
```bash
cd Lab3
make
```

### 2. Run
```bash
./correlate 100 1000
```

### 3. Test with Different Sizes
```bash
make test-small    # 100x1000
make test-medium   # 500x5000
make test-large    # 1000x10000
```

### 4. Performance Analysis (if perf available)
```bash
make perf-sequential
make perf-openmp-4
make perf-optimized-8
```

## For Windows Users (without make)

### 1. Compile using the batch file
```cmd
compile_and_test.bat
```

### 2. Or compile manually
```bash
g++ -std=c++11 -O3 -fopenmp -mavx -c main.cpp
g++ -std=c++11 -O3 -fopenmp -mavx -c correlate.cpp
g++ -o correlate.exe main.o correlate.o -fopenmp
```

### 3. Run
```bash
./correlate.exe 100 1000
```

## Command-Line Options

```bash
./correlate <ny> <nx> [threads] [version]
```

**Examples:**
```bash
# All three versions with default threads
./correlate 100 1000

# Specify number of threads
./correlate 500 5000 4

# Run only sequential (version 1)
./correlate 100 1000 1 1

# Run only OpenMP (version 2) with 8 threads
./correlate 500 5000 8 2

# Run only optimized (version 3) with 4 threads
./correlate 1000 10000 4 3
```

## What to Expect

### Small Matrix (100x1000)
- **Time:** < 1 second
- **Speedup (OpenMP):** ~3-5x
- **Speedup (Optimized):** ~10-15x

### Medium Matrix (500x5000)
- **Time:** 1-5 seconds
- **Speedup (OpenMP):** ~4-6x
- **Speedup (Optimized):** ~15-20x

### Large Matrix (1000x10000)
- **Time:** 10-30 seconds
- **Speedup (OpenMP):** ~5-7x
- **Speedup (Optimized):** ~20-30x

## Files Overview

| File | Description |
|------|-------------|
| `main.cpp` | Main program with benchmarking |
| `correlate.cpp` | Three correlation implementations |
| `correlate.h` | Function declarations |
| `Makefile` | Build automation (Linux/Mac) |
| `compile_and_test.sh` | Shell script (alternative to make) |
| `compile_and_test.bat` | Batch script (Windows) |
| `README.md` | Complete documentation |
| `QUICKSTART.md` | This file |

## Testing Different Thread Counts

```bash
# Test with 1, 2, 4, 8 threads
for t in 1 2 4 8; do
    echo "=== Testing with $t threads ==="
    ./correlate 500 5000 $t 2
done
```

## Testing Different Matrix Sizes

```bash
# Test with increasing sizes
./correlate 100 1000 4 all
./correlate 200 2000 4 all
./correlate 500 5000 4 all
```

## Verification

All three versions should produce **identical results**. The program automatically verifies correctness:
- ✓ PASSED = Results match
- ✗ FAILED = Results don't match (report as bug)

## Performance Metrics Explained

- **Execution time:** Total time in seconds
- **Throughput:** Correlations computed per second
- **Speedup:** Sequential time / Parallel time
- **Efficiency:** (Speedup / Threads) × 100%

### Good Efficiency Targets:
- **70-100%:** Excellent (near-linear scaling)
- **50-70%:** Good (typical for this problem)
- **30-50%:** Fair (overhead dominates at low sizes)
- **< 30%:** Poor (matrix too small or bottlenecks)

## Troubleshooting

### Program crashes or gives wrong results
- Check compiler version: `g++ --version` (need GCC 4.7+)
- Try without AVX: Remove `-mavx` flag
- Reduce matrix size for testing

### Very slow compilation
- Normal with `-O3` optimization
- Can use `-O2` for faster compilation with slightly lower performance

### No speedup observed
- Matrix might be too small (try larger sizes)
- CPU might have limited cores: Check with `nproc` (Linux) or Task Manager (Windows)
- Thermal throttling: Check CPU temperature

## Next Steps

1. ✅ Compile and run basic tests
2. ✅ Verify all versions produce same results
3. ✅ Test with different thread counts (1, 2, 4, 8)
4. ✅ Test with different matrix sizes
5. ✅ Analyze performance patterns
6. ✅ Write report with observations

## For Report Writing

Record these metrics:

| Matrix Size | Threads | Sequential (s) | OpenMP (s) | Optimized (s) | Speedup | Efficiency |
|-------------|---------|----------------|------------|---------------|---------|------------|
| 100x1000    | 1       |                |            |               |         |            |
| 100x1000    | 4       |                |            |               |         |            |
| 500x5000    | 1       |                |            |               |         |            |
| 500x5000    | 4       |                |            |               |         |            |
| 500x5000    | 8       |                |            |               |         |            |

## Key Observations to Note

1. How does speedup change with thread count?
2. Does efficiency improve or degrade with more threads?
3. How much faster is the optimized version than OpenMP alone?
4. What's the main bottleneck? (computation, memory, synchronization)
5. How does matrix size affect parallel efficiency?

---

**Need help?** Check README.md for detailed documentation!
