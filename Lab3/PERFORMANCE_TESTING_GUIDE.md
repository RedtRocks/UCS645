# COMPREHENSIVE PERFORMANCE TESTING GUIDE FOR UBUNTU VM

## Overview
This guide provides step-by-step instructions to run performance analysis on Assignment 3 (Vector Correlation) in an Ubuntu VirtualBox VM. It includes compilation, data collection, and analysis.

---

## PHASE 1: PREPARATION

### Step 1.1: Transfer Files to Ubuntu VM

**On Windows (Host):**
- Copy the entire Lab3 directory to a shared folder or use SCP/Rsync

**On Ubuntu VM:**
```bash
# If using shared folder in VirtualBox
mkdir -p ~/projects
cp -r /media/sf_SharedFolder/Lab3 ~/projects/

# If using SCP
scp -r user@windows_ip:/path/to/Lab3 ~/projects/
```

### Step 1.2: Verify Files
```bash
cd ~/projects/Lab3
ls -la

# You should see:
# - main.cpp, correlate.cpp, correlate.h
# - Makefile
# - compile_and_test.sh, run_comprehensive_tests.sh
# - collect_performance_data.sh
# - analyze_performance.py
# - README.md, QUICKSTART.md, etc.
```

### Step 1.3: Install Dependencies
```bash
# Update package manager
sudo apt-get update

# Install build tools
sudo apt-get install -y build-essential

# Install Python3 for analysis (optional but recommended)
sudo apt-get install -y python3 python3-pip

# Install matplotlib for graphs (optional)
pip3 install matplotlib numpy

# Optional: Install performance analysis tools
sudo apt-get install -y linux-tools-generic

# Verify compiler and OpenMP support
g++ --version
g++ -fopenmp -E -dM - < /dev/null | grep -i omp
```

### Step 1.4: Check System Resources
```bash
# Check CPU details
lscpu

# Check available memory
free -h

# Check if AVX is supported
grep avx /proc/cpuinfo | head -1

# Count threads/cores
nproc
```

---

## PHASE 2: COMPILATION

### Step 2.1: Test Compilation with Makefile
```bash
cd ~/projects/Lab3

# Clean any old builds
make clean

# Build the program
make

# Verify compilation successful
ls -la correlate
./correlate --help  # Should show usage
```

### Step 2.2: Test with Small Example
```bash
# Quick test with small matrix
./correlate 50 500

# Expected output:
# - Matrix dimensions info
# - Three versions (Sequential, OpenMP, Optimized)
# - Execution times
# - Speedup and efficiency metrics
```

### Step 2.3: If Compilation Fails (AVX Support)

If you get AVX errors, modify the Makefile:

```bash
# Edit Makefile
nano Makefile

# Find this line:
# SIMDFLAGS = -mavx -mavx2 -mfma

# Replace with generic flags:
# SIMDFLAGS = -march=x86-64

# Or remove entirely if errors persist
```

---

## PHASE 3: DATA COLLECTION

### Step 3.1: Make Scripts Executable
```bash
chmod +x collect_performance_data.sh
chmod +x compile_and_test.sh
chmod +x analyze_performance.py
```

### Step 3.2: Run Comprehensive Performance Tests

**Important:** This will take 10-30 minutes depending on your VM resources.

```bash
# Full performance data collection
./collect_performance_data.sh

# The script will:
# 1. Capture system information
# 2. Run 4 test phases:
#    - Phase 1: Matrix size scaling (50x500 to 500x5000)
#    - Phase 2: Thread scaling (1-8 threads)
#    - Phase 3: Version comparison
#    - Phase 4: Large matrix stress test
# 3. Generate two output files:
#    - performance_data/performance_summary.txt
#    - performance_data/detailed_execution.log
```

### Step 3.3: Monitor Progress
```bash
# In another terminal, watch the output
tail -f performance_data/performance_summary.txt

# Or view detailed execution log
tail -f performance_data/detailed_execution.log
```

### Step 3.4: Shortened Testing (Fast Version - 5 minutes)

If you want quicker results for initial testing:

```bash
# Run just a few key tests
./correlate 100 1000 1 1        # Sequential baseline
./correlate 100 1000 4 2        # OpenMP with 4 threads
./correlate 100 1000 4 3        # Optimized with 4 threads
./correlate 500 5000 8 all      # All versions with 8 threads
```

---

## PHASE 4: ANALYSIS & REPORTING

### Step 4.1: Generate Analysis Report
```bash
# Run Python analysis script
python3 analyze_performance.py

# Output files generated:
# - performance_data/analysis_report.txt (text summary)
# - performance_data/performance_graphs.png (graphs)
```

### Step 4.2: View Results
```bash
# View text report
cat performance_data/analysis_report.txt

# View the detailed execution log
cat performance_data/detailed_execution.log | less

# View the summary
cat performance_data/performance_summary.txt | less
```

### Step 4.3: View Graphs (if matplotlib available)
```bash
# Display the PNG graphs (requires display capability)
eog performance_data/performance_graphs.png  # Eye of GNOME
# or
feh performance_data/performance_graphs.png   # feh viewer
# or
display performance_data/performance_graphs.png  # ImageMagick
```

### Step 4.4: Extract Specific Metrics
```bash
# Extract execution times only
grep "Execution time:" performance_data/detailed_execution.log

# Extract speedup values
grep "Speedup:" performance_data/detailed_execution.log

# Extract efficiency percentages
grep "Efficiency:" performance_data/detailed_execution.log

# Count how many tests passed
grep -c "PASSED" performance_data/detailed_execution.log
```

---

## PHASE 5: CREATING YOUR REPORT

### Step 5.1: Key Metrics to Include

**Performance Summary Table:**
```
Matrix Size | Sequential (s) | OpenMP (s) | Optimized (s) | OMP Speedup | Opt Speedup
--------|---|---|---|---|---
100x1000   | X.XX | Y.YY | Z.ZZ | Sx | Sx
200x2000   | X.XX | Y.YY | Z.ZZ | Sx | Sx
...
```

**Thread Scaling Analysis:**
- How speedup improves from 1 to 8 threads
- Efficiency metrics (actual vs ideal scaling)
- Identify breaking points where efficiency drops

**Version Comparison:**
- Sequential: baseline performance
- OpenMP: parallelization benefits
- Optimized: additional SIMD/vectorization benefits

### Step 5.2: Sample Report Structure

```
1. INTRODUCTION
   - Assignment overview
   - Objective of performance testing

2. METHODOLOGY
   - System specs used (CPU, RAM, cores)
   - Compiler flags and optimizations
   - Testing scenarios

3. RESULTS
   - Execution time comparisons
   - Speedup analysis
   - Efficiency analysis
   - Throughput measurements

4. GRAPHS & VISUALIZATIONS
   - Execution time vs matrix size
   - Speedup vs thread count
   - Efficiency vs thread count

5. ANALYSIS
   - Key findings
   - Bottlenecks identified
   - Optimization effectiveness

6. CONCLUSION
   - Overall performance summary
   - Recommendations for further optimization
```

### Step 5.3: Collect Data for Report
```bash
# Create a report template
mkdir -p ~/report_data

# Copy all analysis files
cp -r performance_data/* ~/report_data/

# Copy the summary for reference
cp IMPLEMENTATION_SUMMARY.md ~/report_data/

# Create a copy of the code for reference
cp *.cpp *.h ~/report_data/
```

---

## PHASE 6: CUSTOM TESTING SCENARIOS

### Custom Test 1: Specific Matrix Size
```bash
./correlate <ny> <nx> <threads> <version>

# Examples:
./correlate 128 2048 4 all          # Power-of-2 sizes
./correlate 150 1500 6 2            # Custom OpenMP test
./correlate 256 4096 8 3            # Optimized version only
```

### Custom Test 2: Profile with CPU Performance Data
```bash
# Get CPU cycle information
perf stat ./correlate 500 5000 8 2

# Output will show:
# - CPU cycles
# - Instructions executed
# - Cache misses
# - Branches and branch misses
```

### Custom Test 3: Memory Usage Analysis
```bash
# Monitor memory during execution
/usr/bin/time -v ./correlate 1000 10000 8 all

# Output shows:
# - Peak memory usage
# - Page faults
# - I/O statistics
```

### Custom Test 4: Vary OpenMP Settings
```bash
# Set OpenMP environment variables
export OMP_NUM_THREADS=4
export OMP_SCHEDULE=dynamic,10
./correlate 500 5000 4 2

# Or use multiple settings
for sched in static dynamic; do
    for chunk in 1 4 16; do
        echo "Schedule: $sched, Chunk: $chunk"
        OMP_SCHEDULE="$sched,$chunk" ./correlate 300 3000 4 2
    done
done
```

---

## PHASE 7: TROUBLESHOOTING

### Problem: Compilation Fails
**Solution:**
```bash
# Check GCC version (need 4.9+ for good C++11 support)
g++ --version

# Try without AVX flags if they fail
g++ -std=c++11 -O3 -fopenmp -c main.cpp
g++ -std=c++11 -O3 -fopenmp -c correlate.cpp
g++ -fopenmp main.o correlate.o -o correlate
```

### Problem: Port Forwarding Issues (No Display)
```bash
# If you can't see graphs, just work with text output
cat performance_data/analysis_report.txt

# Or copy files to shared folder
cp -r performance_data /media/sf_SharedFolder/

# Then view on Windows host
```

### Problem: Out of Memory
```bash
# Reduce matrix sizes or threads
./correlate 100 1000 2 all   # Smaller matrix
./correlate 500 5000 2 all   # Fewer threads

# Check system memory
free -h

# Kill other processes if needed
top  # Press 'q' to quit
```

### Problem: Slow Performance
```bash
# Ensure no thermal throttling
cat /sys/class/thermal/thermal_zone0/temp

# Check if using correct CPU frequency
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq

# Run just sequential baseline first
./correlate 100 1000 1 1
```

---

## PHASE 8: FINAL CHECKLIST

Before submitting your report:

- [ ] Code compiles without errors on Ubuntu
- [ ] All three versions (Sequential, OpenMP, Optimized) run correctly
- [ ] Verification shows PASSED for all tests
- [ ] Performance data collected in `performance_data/` directory
- [ ] Analysis report generated (`analysis_report.txt`)
- [ ] Graphs generated (if matplotlib installed)
- [ ] Speedup metrics extracted for all test cases
- [ ] Efficiency analysis complete
- [ ] System information documented
- [ ] Report written with findings and analysis

---

## QUICK START (TL;DR)

```bash
# Transfer files and setup
cd ~/projects/Lab3
sudo apt-get install -y build-essential python3-pip
pip3 install matplotlib numpy
make clean && make

# Quick test
./correlate 100 1000

# Full performance test (takes 15-30 minutes)
./collect_performance_data.sh

# Generate analysis
python3 analyze_performance.py

# View results
cat performance_data/analysis_report.txt
```

---

## Resources
- Assignment PDF: `Assignment_3.pdf`
- Implementation details: `IMPLEMENTATION_SUMMARY.md`
- Quick start: `QUICKSTART.md`
- Full documentation: `README.md`

