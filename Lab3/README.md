# Assignment 3: Vector Correlation with Makefiles and OpenMP

## Overview
This assignment implements **pairwise vector correlation** calculation using three different approaches:
1. **Sequential baseline** - Simple, single-threaded implementation
2. **OpenMP parallelized** - Multi-threaded using OpenMP directives
3. **Highly optimized** - Vectorization (SIMD), cache optimization, and OpenMP

## Files Structure
```
Lab3/
├── Makefile          # Build automation and performance testing
├── main.cpp          # Main program with CLI and benchmarking
├── correlate.cpp     # Three correlation implementations
├── correlate.h       # Function declarations
└── README.md         # This file
```

## Problem Description
Given an input matrix with `ny` rows and `nx` columns:
- Each row represents a vector with `nx` elements
- Calculate the **Pearson correlation coefficient** between every pair of rows
- Store result[i + j*ny] = correlation between row i and row j
- Only compute lower triangle: j ≤ i < ny

### Correlation Formula
For normalized vectors (mean=0, std=1):
```
correlation(X, Y) = (1/n) * Σ(xi * yi)
```

For non-normalized:
```
r = Σ((xi - μx)(yi - μy)) / (σx * σy * n)
```

## Compilation

### Build the program
```bash
make
```

### View all available targets
```bash
make help
```

### Clean build files
```bash
make clean
```

## Usage

### Basic Usage
```bash
./correlate <ny> <nx> [num_threads] [version]
```

**Parameters:**
- `ny` - Number of rows (vectors) in the matrix
- `nx` - Number of columns (elements per vector)
- `num_threads` - Number of OpenMP threads (optional, default: max available)
- `version` - Which version to run:
  - `1` = Sequential only
  - `2` = OpenMP only
  - `3` = Optimized only
  - `all` = All versions (default)

### Examples

```bash
# Run all versions with default threads on 100x1000 matrix
./correlate 100 1000

# Use 4 threads
./correlate 500 5000 4

# Run only sequential version
./correlate 100 1000 1 1

# Run only OpenMP version with 8 threads
./correlate 500 5000 8 2

# Run only optimized version with 4 threads
./correlate 1000 10000 4 3
```

## Quick Testing

```bash
# Small test
make test-small

# Medium test
make test-medium

# Large test
make test-large

# Run all tests
make test-all
```

## Performance Analysis with perf

### Sequential Version
```bash
make perf-sequential
```

### OpenMP with Different Thread Counts
```bash
make perf-openmp-1    # 1 thread
make perf-openmp-2    # 2 threads
make perf-openmp-4    # 4 threads
make perf-openmp-8    # 8 threads
```

### Optimized Version
```bash
make perf-optimized-1    # 1 thread
make perf-optimized-4    # 4 threads
make perf-optimized-8    # 8 threads
```

### Run All Perf Tests
```bash
make perf-all
```

## Benchmarking

### Comprehensive Benchmark
```bash
make benchmark
```
Tests multiple matrix sizes with different thread counts.

### Thread Scaling Test
```bash
make scaling-test
```
Measures speedup with 1, 2, 4, and 8 threads on a 500x5000 matrix.

### Size Scaling Test
```bash
make size-scaling
```
Measures performance with increasing matrix sizes.

## Implementation Details

### Version 1: Sequential Baseline
- Straightforward double-precision implementation
- No parallelism or optimizations
- Serves as correctness baseline and performance reference

**Algorithm:**
1. Normalize each row (mean=0, std=1)
2. Calculate dot product between normalized rows
3. Divide by nx to get correlation

**Time Complexity:** O(ny² × nx)

### Version 2: OpenMP Parallelized
- Uses OpenMP `#pragma omp parallel for` directives
- Parallelizes both normalization and correlation computation
- Dynamic scheduling for load balancing

**Optimizations:**
- Parallel normalization of all rows
- Parallel computation of correlation pairs
- Dynamic scheduling with chunk size 4

### Version 3: Highly Optimized
- **SIMD Vectorization:** AVX/AVX2 intrinsics for 4-way parallelism
- **Cache Optimization:** Improved memory access patterns
- **OpenMP Threading:** Multi-core parallelization
- **Compiler Optimizations:** -O3, -march=native

**Optimizations:**
1. Vectorized normalization using AVX (`_mm256_*` intrinsics)
2. Vectorized dot product (4 doubles at a time)
3. Aligned memory allocation for better vectorization
4. Manual loop unrolling where beneficial
5. Combined with OpenMP for multi-threading

## Expected Performance

### Typical Speedups (8-core CPU)
| Version | Threads | Speedup | Efficiency |
|---------|---------|---------|------------|
| Sequential | 1 | 1.0x | 100% |
| OpenMP | 4 | ~3.5x | ~88% |
| OpenMP | 8 | ~6.0x | ~75% |
| Optimized | 4 | ~8.0x | ~200% |
| Optimized | 8 | ~14.0x | ~175% |

*Optimized version achieves >100% efficiency due to SIMD vectorization providing 4x speedup on top of threading.*

### Performance Metrics (500x5000 matrix)
- **Correlation pairs:** 125,250
- **Sequential time:** ~2-3 seconds
- **OpenMP (8 threads):** ~0.4-0.5 seconds
- **Optimized (8 threads):** ~0.15-0.2 seconds

## Understanding Makefile Components

### Variables
```makefile
CXX = g++                    # C++ compiler
CXXFLAGS = -std=c++11 -Wall  # C++ standard and warnings
OPTFLAGS = -O3 -march=native # Optimization flags
OMPFLAGS = -fopenmp          # OpenMP support
SIMDFLAGS = -mavx -mavx2     # SIMD instruction sets
```

### Key Rules
```makefile
all:        # Default target - builds executable
clean:      # Removes build artifacts
run:        # Compiles and runs with default params
test-*:     # Various test scenarios
perf-*:     # Performance analysis with perf
benchmark:  # Comprehensive performance testing
```

### Automatic Variables
- `$@` - Target name
- `$<` - First dependency
- `$^` - All dependencies
- `$(SOURCES:.cpp=.o)` - Pattern substitution

## Performance Testing Guide

### Step 1: Build
```bash
make clean && make
```

### Step 2: Verify Correctness
```bash
./correlate 100 1000
```
Check that all versions produce identical results.

### Step 3: Basic Performance Test
```bash
make test-all
```

### Step 4: Thread Scaling Analysis
```bash
make scaling-test
```
Observe speedup with increasing threads.

### Step 5: Detailed perf Analysis
```bash
# Sequential baseline
make perf-sequential

# OpenMP with 8 threads
make perf-openmp-8

# Optimized with 8 threads
make perf-optimized-8
```

### Step 6: Compare Metrics
Look for:
- **Instructions per cycle (IPC):** Higher is better (optimized should be ~3-4 with SIMD)
- **Cache miss rate:** Lower is better
- **Branch mispredictions:** Lower is better
- **Execution time:** Lower is better

## Sample Output

```
=========================================================================
VECTOR CORRELATION COMPUTATION
=========================================================================
Matrix dimensions: 500 rows x 5000 columns
Total elements: 2500000
Correlation pairs to compute: 125250
Available threads: 8
Using threads: 8
=========================================================================

--- VERSION 1: SEQUENTIAL BASELINE ---
Execution time: 2.458361 seconds
Throughput: 50952.36 correlations/second

--- VERSION 2: OPENMP PARALLELIZED (8 threads) ---
Execution time: 0.412753 seconds
Throughput: 303514.72 correlations/second
Speedup: 5.96x
Efficiency: 74.5%
Verifying correctness... PASSED

--- VERSION 3: HIGHLY OPTIMIZED (8 threads + SIMD) ---
Execution time: 0.168234 seconds
Throughput: 744628.45 correlations/second
Speedup: 14.61x
Efficiency: 182.6%
Verifying correctness... PASSED

=========================================================================
PERFORMANCE SUMMARY
=========================================================================
Sequential:  2.458361 s  (baseline)
OpenMP:      0.412753 s  (speedup: 5.96x)
Optimized:   0.168234 s  (speedup: 14.61x)

Optimized vs OpenMP: 2.45x faster
=========================================================================
```

## Troubleshooting

### Issue: "command not found: perf"
**Solution:** perf is Linux-specific. On Windows/Mac, run the program directly:
```bash
./correlate 500 5000 8
```

### Issue: Low performance gains
**Possible causes:**
1. CPU doesn't support AVX2: Check with `lscpu | grep avx`
2. Not enough cores: Check with `nproc`
3. Thermal throttling: Monitor CPU frequency
4. Matrix too small: Try larger sizes (1000x10000)

### Issue: Compilation errors with AVX
**Solution:** Remove SIMD intrinsics or add:
```makefile
CXXFLAGS += -mno-avx  # Disable AVX if not supported
```

### Issue: Different results between versions
**Solution:** Small floating-point differences are expected due to different computation orders.
Check tolerance in `verify_results()` function (default: 1e-4).

## Advanced Usage

### Custom Matrix Size Sweep
```bash
for size in $(seq 100 100 1000); do
    echo "Testing ${size}x$((size*10))"
    ./correlate $size $((size*10)) 8 3
done
```

### Performance CSV Export
```bash
echo "ny,nx,threads,time,speedup" > results.csv
for threads in 1 2 4 8; do
    ./correlate 500 5000 $threads 3 | grep "Execution time" | \
        awk -v t=$threads '{print "500,5000," t "," $3}' >> results.csv
done
```

## Learning Objectives

After completing this assignment, you should understand:

1. **Makefile concepts:**
   - Variables and macros
   - Pattern rules and dependencies
   - Automatic variables ($@, $<, $^)
   - Phony targets

2. **OpenMP parallelization:**
   - Parallel for directives
   - Thread management
   - Scheduling strategies
   - Load balancing

3. **Performance optimization:**
   - SIMD vectorization
   - Cache-friendly algorithms
   - Memory access patterns
   - Compiler optimizations

4. **Performance measurement:**
   - Timing with chrono
   - perf stat analysis
   - Speedup and efficiency calculations
   - Bottleneck identification

## References

- [GNU Make Manual](https://www.gnu.org/software/make/manual/)
- [OpenMP Specifications](https://www.openmp.org/specifications/)
- [Intel Intrinsics Guide](https://software.intel.com/sites/landingpage/IntrinsicsGuide/)
- [Linux perf Wiki](https://perf.wiki.kernel.org/index.php/Main_Page)

## Author
UCS645: Parallel & Distributed Computing
Assignment 3: Makefiles and Vector Correlation
