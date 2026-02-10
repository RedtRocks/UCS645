# Quick Start Guide
## Assignment 2: OpenMP Performance Evaluation

---

## ⚡ Super Quick Start (Recommended)

### Step 1: Navigate to Lab2 directory
```bash
cd ~/UCS645/Lab2
# or wherever you saved the files
```

### Step 2: Make the script executable and run
```bash
chmod +x run_all.sh
./run_all.sh
```

**That's it!** The script will:
- ✅ Compile all three programs
- ✅ Run all experiments
- ✅ Save output to `output/` directory

---

## 📋 Manual Compilation & Execution

### Compile Individual Programs
```bash
# Question 1: Molecular Dynamics
g++ -O3 -fopenmp -std=c++17 q1_molecular_dynamics.cpp -o q1_molecular_dynamics

# Question 2: DNA Sequence Alignment
g++ -O3 -fopenmp -std=c++17 q2_dna_alignment.cpp -o q2_dna_alignment

# Question 3: Heat Diffusion
g++ -O3 -fopenmp -std=c++17 q3_heat_diffusion.cpp -o q3_heat_diffusion
```

### Run Individual Programs
```bash
# Run Question 1
./q1_molecular_dynamics

# Run Question 2
./q2_dna_alignment

# Run Question 3
./q3_heat_diffusion
```

---

## 🎯 Testing Specific Thread Counts

### Set thread count before running
```bash
# Test with 1 thread (serial)
export OMP_NUM_THREADS=1
./q1_molecular_dynamics

# Test with 4 threads
export OMP_NUM_THREADS=4
./q1_molecular_dynamics

# Test with 8 threads
export OMP_NUM_THREADS=8
./q1_molecular_dynamics
```

### Or set inline
```bash
OMP_NUM_THREADS=4 ./q2_dna_alignment
```

---

## 📊 Save Output to Files

### Save and display simultaneously
```bash
./q1_molecular_dynamics | tee results_q1.txt
./q2_dna_alignment | tee results_q2.txt
./q3_heat_diffusion | tee results_q3.txt
```

### Save only (no display)
```bash
./q1_molecular_dynamics > results_q1.txt 2>&1
```

---

## 🔍 Performance Monitoring

### Using perf (if available)
```bash
# Basic stats
perf stat ./q1_molecular_dynamics

# Detailed counters
perf stat -e cycles,instructions,cache-misses,cache-references ./q1_molecular_dynamics

# In VirtualBox (use full path)
sudo /usr/lib/linux-tools/$(uname -r)/perf stat ./q1_molecular_dynamics
```

### Using time command
```bash
# Simple timing
time ./q1_molecular_dynamics

# Detailed timing
/usr/bin/time -v ./q1_molecular_dynamics
```

---

## 🐛 Troubleshooting

### Problem: Permission denied when running ./run_all.sh
```bash
chmod +x run_all.sh
```

### Problem: g++ command not found
```bash
sudo apt update
sudo apt install build-essential
```

### Problem: OpenMP not supported
```bash
# Verify installation
echo |cpp -fopenmp -dM |grep -i open

# Should show: #define _OPENMP 201511
```

### Problem: Programs compile but don't run in parallel
```bash
# Check available threads
echo $OMP_NUM_THREADS

# If empty, OpenMP will use all available cores
# Set explicitly:
export OMP_NUM_THREADS=4
```

---

## 📈 Understanding Output

### What to Look For

#### ✅ Good Signs
- Speedup increases with threads
- Efficiency > 70%
- Energy/Score values match across thread counts (correctness)

#### ⚠️ Warning Signs
- Speedup plateaus early
- Efficiency < 50%
- Different results with different thread counts (BUG!)

### Sample Expected Output

**Question 1:**
```
Threads    Time (s)    Speedup    Efficiency
1          2.45        1.00x      100.00%
2          1.35        1.81x      90.50%
4          0.75        3.27x      81.75%
8          0.45        5.44x      68.00%
```

**Analysis**: Good scaling up to 4 threads, moderate at 8 threads.

---

## 📚 Files Reference

| File | Purpose |
|------|---------|
| `q1_molecular_dynamics.cpp` | Question 1 source code |
| `q2_dna_alignment.cpp` | Question 2 source code |
| `q3_heat_diffusion.cpp` | Question 3 source code |
| `run_all.sh` | Automated compile & run script |
| `README.md` | Comprehensive documentation |
| `ANALYSIS.md` | Detailed output interpretation |
| `QUICKSTART.md` | This file |

---

## 🎓 Creating Your Report

### 1. Run Experiments
```bash
./run_all.sh
```

### 2. Save Results
Results are automatically saved in `output/` directory.

### 3. Create Tables
Copy the output tables directly into your report.

### 4. Create Graphs
Use the data to create:
- Speedup vs Threads
- Efficiency vs Threads
- Execution Time vs Threads

### 5. Add Analysis
Read `ANALYSIS.md` for detailed explanations of:
- Why speedup is sub-linear
- What bottlenecks exist
- How to interpret efficiency
- Comparisons with Amdahl's Law

---

## 🚀 Advanced Usage

### Run Multiple Times for Statistics
```bash
# Run 5 times and save all outputs
for i in {1..5}; do
    echo "Run $i"
    ./q1_molecular_dynamics >> results_all.txt
done
```

### Test Different Problem Sizes
Edit the source code to modify:
- **Q1**: Number of particles (`N`)
- **Q2**: Sequence length
- **Q3**: Grid size (`nx`, `ny`)

Then recompile and run.

### Profile with Different Schedules
The programs already test different OpenMP schedules:
- Static
- Dynamic
- Guided

Results are shown in the output.

---

## ❓ Quick FAQ

**Q: How long should programs take to run?**
A: Each program should complete in under 1 minute on a typical VM.

**Q: Do I need to run on bare metal or is VM okay?**
A: VM is fine! Results will show the same patterns.

**Q: What if I have fewer than 8 cores?**
A: Programs will automatically adapt to available cores.

**Q: Why are my speedups different from the analysis?**
A: Exact values depend on hardware. Patterns should be similar.

**Q: Can I modify the problem sizes?**
A: Yes! Edit the source code and recompile.

---

## 📞 Getting Help

1. **Compilation errors**: Check README.md troubleshooting section
2. **Runtime errors**: Ensure OpenMP is enabled
3. **Understanding output**: Read ANALYSIS.md
4. **Performance questions**: See performance metrics section in ANALYSIS.md

---

## ✅ Checklist for Submission

- [ ] All three programs compile without errors
- [ ] All three programs run successfully
- [ ] Output shows varying thread counts (1, 2, 4, 8)
- [ ] Speedup values are reasonable (> 1)
- [ ] Efficiency values decline with threads (expected)
- [ ] Created tables from output
- [ ] Created graphs (speedup, efficiency)
- [ ] Written analysis explaining results
- [ ] Compared with Amdahl's Law
- [ ] Identified bottlenecks for each program

---

**Ready to Start?**
```bash
cd Lab2
chmod +x run_all.sh
./run_all.sh
```

**Good luck with your assignment! 🎉**
