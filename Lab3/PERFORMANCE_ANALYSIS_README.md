# PERFORMANCE TESTING AND ANALYSIS TOOLKIT

## Overview

This toolkit provides a complete end-to-end solution for collecting, analyzing, and reporting performance metrics for Assignment 3 (Vector Correlation with Makefiles and OpenMP).

**Key Features:**
- Automated performance data collection
- Statistical analysis and reporting
- Graph generation for visualization
- CSV export for spreadsheet analysis
- Step-by-step execution guide

---

## Files Included

### Core Scripts

| File | Purpose |
|------|---------|
| `run_all_tests.sh` | **START HERE** - Automated pipeline (compile → test → analyze → export) |
| `collect_performance_data.sh` | Collects detailed performance metrics across multiple test scenarios |
| `analyze_performance.py` | Analyzes collected data and generates reports + graphs |
| `export_to_csv.py` | Exports results to CSV for Excel/spreadsheet analysis |
| `generate_quick_summary.sh` | Generates quick reference summary of key metrics |

### Documentation

| File | Purpose |
|------|---------|
| `PERFORMANCE_TESTING_GUIDE.md` | **COMPREHENSIVE GUIDE** - Step-by-step instructions for running tests on Ubuntu VM |
| `UBUNTU_SETUP.md` | Setup instructions and troubleshooting for Ubuntu/Linux |

### Application Code

| File | Purpose |
|------|---------|
| `main.cpp` | Main program with benchmarking and result verification |
| `correlate.cpp` | Three implementations (Sequential, OpenMP, Optimized) |
| `correlate.h` | Function declarations |

---

## QUICK START (5 Minutes)

### On Ubuntu VM:

```bash
# Navigate to Lab3 directory
cd ~/projects/Lab3

# Make scripts executable
chmod +x *.sh
chmod +x *.py

# Run the complete pipeline
./run_all_tests.sh

# Wait 15-30 minutes for completion
# Results will be in performance_data/ directory
```

---

## DETAILED WORKFLOW

### Step 1: Preparation
```bash
# Install dependencies
sudo apt-get update
sudo apt-get install -y build-essential python3 python3-pip
pip3 install matplotlib numpy

# Verify system
lscpu | grep -E "CPU|Cores"
free -h | grep Mem
```

### Step 2: Compilation
```bash
# Build the program
make clean
make

# Quick test
./correlate 50 500
```

### Step 3: Collect Performance Data
```bash
# Option A: Automated pipeline (recommended)
./run_all_tests.sh

# Option B: Manual data collection
./collect_performance_data.sh  # Takes 15-30 minutes

# Option C: Quick test (3 minutes)
./correlate 100 1000 4 all
./correlate 200 2000 4 all
./correlate 500 5000 8 all
```

### Step 4: Analyze Results
```bash
# Generate analysis report and graphs
python3 analyze_performance.py

# Generate quick summary
./generate_quick_summary.sh

# View results
cat performance_data/analysis_report.txt
cat performance_data/QUICK_SUMMARY.txt
```

### Step 5: Export for Excel
```bash
# Create CSV files
python3 export_to_csv.py

# Copy to Windows shared folder
cp performance_data/*.csv /media/sf_SharedFolder/
```

---

## Output Structure

After running tests, you'll have:

```
performance_data/
├── performance_summary.txt        # Detailed execution results
├── detailed_execution.log          # Complete test output
├── QUICK_SUMMARY.txt              # Quick reference summary
├── analysis_report.txt            # Statistical analysis
├── performance_graphs.png         # Visualization graphs
├── performance_data.csv           # Full dataset in CSV
└── performance_summary.csv        # Summary in CSV
```

---

## Test Scenarios

### Phase 1: Matrix Size Scaling
Tests how performance changes with increasing matrix dimensions:
- 50×500 (smallest)
- 100×1000
- 200×2000
- 300×3000
- 500×5000 (largest)

**What to look for:**
- Execution time scaling with O(n²) or O(n³) complexity
- Memory efficiency
- Cache utilization

### Phase 2: Thread Scaling
Tests how speedup changes with increasing thread count:
- 1 thread (sequential baseline)
- 2 threads
- 4 threads
- 8 threads

**What to look for:**
- Linear speedup vs actual speedup
- Efficiency degradation at higher thread counts
- Amdahl's Law effects

### Phase 3: Version Comparison
Compares the three implementations:
1. **Sequential**: Single-threaded baseline
2. **OpenMP**: Parallelized version
3. **Optimized**: SIMD + Vectorization + Parallelization

**What to look for:**
- OpenMP overhead cost
- SIMD benefits
- Combined optimization effectiveness

### Phase 4: Stress Test
Large matrix to test limits:
- 1000×10000 matrix
- 8 threads
- All versions

**What to look for:**
- Memory pressure
- Cache behavior under load
- Practical performance limits

---

## Key Performance Metrics

### 1. Execution Time
- **Definition:** Wall-clock time to complete correlation calculation
- **Unit:** Seconds
- **What it means:** Lower is better

### 2. Speedup
- **Formula:** `Sequential Time / Parallel Time`
- **Reference:** 1.0 = no improvement, 4.0 = 4x faster
- **Ideal:** Linear speedup = number of threads

### 3. Efficiency
- **Formula:** `(Speedup / Number of Threads) × 100%`
- **Reference:** 100% = perfect parallelization
- **Typical:** 70-90% is good, <50% indicates bottleneck

### 4. Throughput
- **Formula:** `Number of Correlations / Execution Time`
- **Unit:** Correlations per second
- **What it means:** Higher is better

### 5. Amdahl's Law
- **Formula:** `1 / ((1-p) + (p/n))` where p = parallelizable fraction, n = threads
- **Concept:** Limits maximum possible speedup with limited parallelizable portions

---

## Creating Your Report

### Recommended Report Structure

```
1. EXECUTIVE SUMMARY
   - Key findings in 1-2 paragraphs
   - Overall performance assessment

2. METHODOLOGY
   - Test scenarios and parameters
   - System specifications
   - Compiler flags used

3. RESULTS
   - Execution Time Analysis
   - Speedup Comparison
   - Efficiency Analysis
   - Throughput Measurements

4. VISUALIZATIONS
   - Execution Time vs Matrix Size (bar chart)
   - Speedup vs Thread Count (line chart)
   - Efficiency vs Thread Count (line chart)
   - Performance Comparison (stacked bar)

5. ANALYSIS & INTERPRETATION
   - What each metric tells you
   - Bottlenecks identified
   - Why certain versions outperform others

6. RECOMMENDATIONS
   - Further optimization opportunities
   - Best parameters for different workloads

7. CONCLUSION
   - Summary of findings
   - Trade-offs between approaches
```

### Example Metrics to Include

**Table 1: Execution Time Comparison**
```
Matrix Size | Sequential | OpenMP(4) | Optimized(4) | OMP Speedup | Opt Speedup
50×500      | 0.023s     | 0.012s    | 0.008s       | 1.92x       | 2.88x
100×1000    | 0.091s     | 0.036s    | 0.022s       | 2.53x       | 4.14x
200×2000    | 0.372s     | 0.121s    | 0.068s       | 3.07x       | 5.47x
500×5000    | 2.341s     | 0.651s    | 0.341s       | 3.60x       | 6.87x
```

**Table 2: Efficiency Analysis (8 threads)**
```
Threads | Sequential | OpenMP  | Optimized
1       | Baseline   | 100%    | 100%
2       | Speedup    | 1.89x   | 1.95x (94-98% eff)
4       | Speedup    | 3.61x   | 3.79x (90-95% eff)
8       | Speedup    | 6.87x   | 7.12x (86-89% eff)
```

---

## Troubleshooting

### Compilation Issues

**Problem:** `error: omp.h: No such file`
```bash
# Solution: Install OpenMP
sudo apt-get install libomp-dev
```

**Problem:** `error: unknown option '-mavx'`
```bash
# Solution: Modify Makefile, remove AVX flags
# Edit Makefile and change: SIMDFLAGS = -march=x86-64
```

### Runtime Issues

**Problem:** Out of memory with large matrices
```bash
# Solution: Run smaller matrices first
./correlate 100 1000 4 all  # Instead of 1000x10000
```

**Problem:** Slow performance on VirtualBox
```bash
# Solution: Allocate more CPU cores in VirtualBox settings
# Settings → System → Processor → increase CPU count
```

### Analysis Issues

**Problem:** `matplotlib not available`
```bash
# Solution: Install matplotlib
pip3 install matplotlib numpy
```

**Problem:** CSV export fails
```bash
# Solution: Install Python packages
pip3 install numpy
```

---

## Advanced Options

### Custom Test Parameters

```bash
# Run custom matrix size
./correlate <ny> <nx> <threads> <version>

Examples:
./correlate 128 1280 4 all    # Power-of-2 matrix
./correlate 1024 10240 8 2    # Large matrix, OpenMP only
./correlate 512 5120 16 3     # With 16 threads, optimized only
```

### Environment Variables

```bash
# Control OpenMP behavior
export OMP_NUM_THREADS=8
export OMP_SCHEDULE=dynamic,4
export OMP_PROC_BIND=true

./correlate 500 5000 8 2
```

### Performance Analysis with `perf`

```bash
# Measure CPU cycles and instructions
perf stat -e cycles,instructions,cache-references,cache-misses \
    ./correlate 500 5000 8 2

# Profile execution
perf record ./correlate 500 5000 8 2
perf report
```

### Memory Analysis

```bash
# Monitor peak memory usage
/usr/bin/time -v ./correlate 1000 10000 8 all
```

---

## Sample Analysis Output

```
EXECUTION TIME SUMMARY
Sequential:  2.341 s  (baseline)
OpenMP:      0.651 s  (speedup: 3.60x)
Optimized:   0.341 s  (speedup: 6.87x)

Optimized vs OpenMP: 1.91x faster (vectorization benefit)

EFFICIENCY (8 threads)
OpenMP:      85.8% (6.87x speedup / 8 threads)
Optimized:   89.1% (7.12x speedup / 8 threads)

THROUGHPUT
Sequential:  1,068,341 correlations/sec
OpenMP:      3,841,168 correlations/sec (3.60x)
Optimized:   7,332,856 correlations/sec (6.87x)
```

---

## Best Practices for Report Writing

1. **Use actual numbers** - Include measured values, not estimates
2. **Show graphs** - Visual representation is powerful
3. **Explain findings** - Why did performance change?
4. **Compare versions** - Highlight differences between approaches
5. **Discuss trade-offs** - What's gained and lost with each approach
6. **Provide context** - How do these results compare to theoretical limits?
7. **Be honest** - Report both successes and limitations

---

## Resources

- **Main Application Documentation:** See `README.md`
- **Execution Guide:** See `PERFORMANCE_TESTING_GUIDE.md`
- **Implementation Details:** See `IMPLEMENTATION_SUMMARY.md`
- **Compiler Flags:** See `Makefile`
- **Assignment Details:** See `Assignment_3.pdf`

---

## Support

For issues or questions:
1. Check `PERFORMANCE_TESTING_GUIDE.md` Troubleshooting section
2. Review generated analysis reports
3. Check detailed execution logs
4. Verify system meets requirements (GCC 4.9+, OpenMP, AVX support)

