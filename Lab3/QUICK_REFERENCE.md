# QUICK REFERENCE - PERFORMANCE TESTING CHEAT SHEET

## File Organization

```
Lab3/
├── SOURCE CODE
│   ├── main.cpp              Main program
│   ├── correlate.cpp         Implementations
│   ├── correlate.h           Declarations
│   └── Makefile              Build system
│
├── PERFORMANCE TOOLS
│   ├── run_all_tests.sh      ⭐ START HERE - Full pipeline
│   ├── collect_performance_data.sh
│   ├── analyze_performance.py
│   ├── export_to_csv.py
│   └── generate_quick_summary.sh
│
└── DOCUMENTATION
    ├── PERFORMANCE_ANALYSIS_README.md    ⭐ This toolkit overview
    ├── PERFORMANCE_TESTING_GUIDE.md      ⭐ Step-by-step Ubuntu guide
    ├── UBUNTU_SETUP.md
    ├── README.md
    ├── IMPLEMENTATION_SUMMARY.md
    └── QUICKSTART.md
```

---

## QUICKEST PATH TO RESULTS (Ubuntu VM)

```bash
# Step 1: Install dependencies (1 minute)
sudo apt-get update
sudo apt-get install build-essential python3-pip
pip3 install matplotlib numpy

# Step 2: Run everything (20-30 minutes)
cd ~/Lab3
chmod +x *.sh *.py
./run_all_tests.sh

# Step 3: View results (2 minutes)
cat performance_data/QUICK_SUMMARY.txt
cat performance_data/analysis_report.txt

# Step 4: Export for Excel (if needed)
cp performance_data/*.csv /path/to/windows/
```

---

## INDIVIDUAL COMMANDS

| Command | Time | Purpose |
|---------|------|---------|
| `make clean && make` | 30s | Compile program |
| `./correlate 50 500` | 5s | Quick test/verify |
| `./collect_performance_data.sh` | 20-30m | Full test suite |
| `./generate_quick_summary.sh` | 10s | Quick metrics |
| `python3 analyze_performance.py` | 30s | Full analysis |
| `python3 export_to_csv.py` | 5s | Export to Excel |

---

## TROUBLESHOOTING QUICK FIXES

```bash
# OpenMP not found
sudo apt-get install libomp-dev

# Python packages missing
pip3 install matplotlib numpy

# AVX compilation error
# Edit Makefile, change: SIMDFLAGS = -march=x86-64

# Out of memory
# Reduce matrix size: ./correlate 100 1000 2 all

# Need more details
./correlate <ny> <nx> <threads> <version>
# version: 1=seq, 2=omp, 3=opt, all
```

---

## KEY METRICS EXPLAINED

| Metric | Formula | Good Value |
|--------|---------|-----------|
| **Execution Time** | Wall clock | Lower is better |
| **Speedup** | Seq_Time / Parallel_Time | > Number of Threads = beating Amdahl's Law |
| **Efficiency** | (Speedup / Threads) × 100% | > 70% is good |
| **Throughput** | Correlations / Second | Higher is better |

---

## PERFORMANCE DATA INTERPRETATION

**If you see...**

✓ Speedup = 3.8x with 4 threads → Good parallelization (95% efficiency)
✗ Speedup = 1.1x with 4 threads → Serial bottleneck / overhead
✓ Optimized 2x faster than OpenMP → SIMD vectorization working
✗ All three versions similar → Maybe optimization flags not enabled

---

## WHAT TO INCLUDE IN YOUR REPORT

### Minimum (Required)
- [ ] System specifications (CPU, cores, RAM)
- [ ] Execution times for each version
- [ ] At least 2 graphs (speedup, efficiency)
- [ ] Summary of findings

### Recommended (Better Grade)
- [ ] Multiple test scenarios (size + thread scaling)
- [ ] Detailed efficiency analysis
- [ ] Explanation of why each version performs differently
- [ ] Comparison to theoretical limits (Amdahl's Law)
- [ ] Discussion of bottlenecks

### Excellent (Best)
- [ ] 4+ different test scenarios
- [ ] Cache efficiency analysis
- [ ] Memory usage patterns
- [ ] Detailed performance science explanation
- [ ] Recommendations for further optimization

---

## FILE MANIFEST & USAGE

### Scripts to Run

```bash
# Recommended: One command to run everything
./run_all_tests.sh

# Alternative: Run individual steps
./collect_performance_data.sh    # Gather data
./generate_quick_summary.sh      # Quick summary
python3 analyze_performance.py   # Detailed analysis
python3 export_to_csv.py         # Format for Excel
```

### Output Files Created

```
performance_data/
├── performance_summary.txt      ← Main results
├── detailed_execution.log       ← Complete output
├── QUICK_SUMMARY.txt           ← Key metrics (2 pages)
├── analysis_report.txt         ← Analysis
├── performance_graphs.png      ← Graphs (matplotlib)
├── performance_data.csv        ← Full data (Excel)
└── performance_summary.csv     ← Summary (Excel)
```

---

## ENVIRONMENT SETUP (One-Time)

```bash
# Copy Lab3 to home directory
mkdir -p ~/projects
cp -r /path/to/Lab3 ~/projects/

# Install dependencies
sudo apt-get update
sudo apt-get install -y build-essential python3-pip
pip3 install matplotlib numpy

# Verify
g++ --version
python3 --version
nproc  # Show number of cores
```

---

## TESTING PHASES

**Phase 1: Matrix Size Scaling** (5 min)
- Tests: 50×500 to 500×5000
- Measures: Execution time scaling
- Finding: How efficiently scales with data size

**Phase 2: Thread Scaling** (5 min)
- Tests: 1, 2, 4, 8 threads
- Measures: Speedup vs threads
- Finding: Parallelization effectiveness

**Phase 3: Version Comparison** (3 min)
- Tests: All 3 implementations
- Measures: Version differences
- Finding: Optimization benefit

**Phase 4: Stress Test** (2-5 min)
- Tests: Large matrix 1000×10000
- Measures: Behavior under load
- Finding: Performance limits

---

## PERFORMANCE TARGETS (Reference)

```
Sequential baseline: 2-5 seconds for 500×5000 matrix

With OpenMP (4 threads):
- Expected speedup: 3.0-3.8x
- Expected efficiency: 75-95%

With Optimized (4 threads):
- Expected speedup: 4.5-6.0x
- Expected efficiency: 85-95%
```

(Actual results depend on VirtualBox CPU allocation)

---

## AFTER TESTING

```bash
# View summary report
cat performance_data/QUICK_SUMMARY.txt

# View detailed analysis
cat performance_data/analysis_report.txt

# View execution details
less performance_data/detailed_execution.log

# View graphs (if available)
eog performance_data/performance_graphs.png

# Copy CSV to Windows for Excel
cp performance_data/*.csv /media/sf_SharedFolder/
```

---

## COMMON ANALYSIS STATEMENTS

Use these in your report:

- "The sequential baseline took X seconds for a YxZ matrix."
- "OpenMP achieved Ax speedup with B threads, representing C% efficiency."
- "The optimized version was Dx faster due to SIMD vectorization."
- "Efficiency degraded from XY% at 2 threads to AB% at 8 threads."
- "Cache efficiency shows CD misses per correlations computed."
- "The application scales well up to EF threads before hitting serialization bottleneck."

---

## FINAL CHECKLIST

- [ ] Code compiles without warnings
- [ ] All three versions run correctly
- [ ] Verification shows PASSED
- [ ] Performance data collected (>50MB of data)
- [ ] Analysis report generated
- [ ] Graphs created (if matplotlib installed)
- [ ] CSV files exported
- [ ] Results reviewed and understood
- [ ] Report written with findings
- [ ] Report includes system specs
- [ ] Report includes graphs/tables
- [ ] Report discusses findings

## TIMING EXPECTATIONS

| Task | Expected Time |
|------|----------------|
| Setup (first time only) | 10 min |
| Compile | 1 min |
| Quick verification test | 5 sec |
| Full test suite | 20-30 min |
| Analysis & graph generation | 1 min |
| Generate report | 30-60 min |
| **TOTAL** | **~1-2 hours** |

---

## STILL STUCK?

1. Read: `PERFORMANCE_TESTING_GUIDE.md` (comprehensive)
2. Check: `UBUNTU_SETUP.md` (dependencies)
3. Review: `PERFORMANCE_ANALYSIS_README.md` (details)
4. Look at: Generated reports in `performance_data/`

