# Lab Assignment 2: OpenMP Performance Evaluation
## Complete Solution with Report Generation

**UCS645: Parallel & Distributed Computing**

---

## 🌟 What's New in This Enhanced Version

This is an **ENHANCED version** designed to generate output **exactly like the example report PDF**. It includes:

✅ **Multiple thread counts** (1, 2, 4, 8, 10, 12)
✅ **Performance statistics** in perf stat format
✅ **VTune-style metrics tables**
✅ **Multiple scheduling strategies** (Q3)
✅ **Both parallelization methods** (Q2)
✅ **CSV export** for automatic graph generation
✅ **Python script** for publication-quality graphs
✅ **Complete report template** with examples

---

## 📦 Complete Package Contents

### **🔧 Programs**

| File | Description | Use For |
|------|-------------|---------|
| `q1_molecular_dynamics_report.cpp` | Enhanced Q1 with metrics | **Report** |
| `q2_dna_alignment_report.cpp` | Enhanced Q2 with both methods | **Report** |
| `q3_heat_diffusion_report.cpp` | Enhanced Q3 with 4 schedules | **Report** |
| `q1_molecular_dynamics.cpp` | Original Q1 | Reference |
| `q2_dna_alignment.cpp` | Original Q2 | Reference |
| `q3_heat_diffusion.cpp` | Original Q3 | Reference |

### **📜 Scripts**

| File | Purpose |
|------|---------|
| `run_report_versions.sh` | ⭐ **RUN THIS** - Compiles & runs enhanced versions |
| `generate_graphs.py` | ⭐ **RUN THIS** - Auto-generates all graphs |
| `run_all.sh` | Runs original versions |

### **📚 Documentation**

| File | Contents |
|------|----------|
| `PROJECT_GUIDE.md` | 📖 Complete overview (read first!) |
| `REPORT_TEMPLATE.md` | ⭐ Step-by-step report creation |
| `QUICKSTART.md` | Quick commands reference |
| `README.md` | Original comprehensive docs |
| `ANALYSIS.md` | 20+ pages detailed analysis |

---

## 🚀 Super Quick Start (3 Commands)

```bash
# 1. Run all experiments (creates txt and csv files)
chmod +x run_report_versions.sh && ./run_report_versions.sh

# 2. Generate graphs (creates PNG and PDF files)
pip3 install matplotlib pandas && python3 generate_graphs.py

# 3. Create your report using the template
# Open REPORT_TEMPLATE.md and follow step-by-step instructions
```

**That's it!** You now have everything needed for your report.

---

## 📊 What Gets Generated

### **After Step 1 (run_report_versions.sh)**

```
output/
├── q1_report_output.txt    # Contains tables, perf stats, VTune metrics
├── q2_report_output.txt    # Contains tables for both methods
└── q3_report_output.txt    # Contains tables for all 4 schedules

Root directory/
├── q1_molecular_dynamics_data.csv    # For graphing
├── q2_dna_alignment_data.csv         # For graphing
└── q3_heat_diffusion_data.csv        # For graphing
```

### **After Step 2 (generate_graphs.py)**

```
graphs/
├── q1_speedup.png (and .pdf)           # Molecular Dynamics graph
├── q2_speedup.png (and .pdf)           # DNA Alignment comparison
├── q3_speedup.png (and .pdf)           # Heat Diffusion comparison
├── efficiency_comparison.png           # Bonus: All three compared
└── summary_statistics.txt              # Key numbers for reference
```

---

## 📋 Example Output Preview

### **Q1: Molecular Dynamics - Execution Table**

```
Molecular Dynamics: Lennard-Jones Force Calculation
Number of particles: 1000
Cutoff distance: 2.5

Threads    Time (s)        Speedup    Efficiency
========================================================
1          0.023846        1.00       x100.0
2          0.011534        2.07       x103.4
4          0.006656        3.58       x89.6
8          0.004779        4.99       x62.4
10         0.004851        4.92       x49.2
12         0.004199        5.68       x47.3
========================================================
```

### **Performance Statistics (perf stat style)**

```
Performance counter stats for 8 threads:

  125,699,005  cpu_atom/cycles/
  169,920,002  cpu_core/cycles/
  414,582,226  cpu_atom/instructions/       #   3.31 insn per cycle
  636,509,979  cpu_core/instructions/       #   3.75 insn per cycle
  122,843      cpu_atom/cache-references/
  237,009      cpu_core/cache-references/
  34,890       cpu_atom/cache-misses/       #   28.42% of all cache refs
  102,860      cpu_core/cache-misses/       #   43.40% of all cache refs

  0.01824792 seconds time elapsed
```

### **VTune Metrics Table**

```
Metric                        | Observed Value      | Interpretation
---------------------------------------------------------------------------------
CPI (Cycles Per Instruction)  | 0.58                | Good instruction efficiency
Effective Core Utilization    | ~14–22%             | Limited by synchronization
Cache Bound (Overall)         | ~35–37%             | Significant cache waiting time
DRAM Bound                    | <1%                 | Not memory bandwidth limited
Vectorization                 | 0%                  | Not possible with atomics
```

---

## 📈 Creating Your Report

### **Option 1: Follow the Template (Recommended)**

Open `REPORT_TEMPLATE.md` and follow the step-by-step instructions. It shows you:
- How to copy tables from output files
- How to format them for your report
- How to insert graphs
- How to write analysis paragraphs (with examples)
- Complete report structure

### **Option 2: Use the Example as Guide**

The example PDF (`inference_lab2_v1.pdf`) shows the expected format:
1. Question title
2. Execution table(s)
3. Performance statistics
4. Analysis paragraph
5. VTune table
6. Detailed analysis
7. Graph

Your enhanced output follows **exactly this format**.

---

## 🎯 Key Features of Enhanced Version

### **1. Multiple Thread Counts**
- Tests: 1, 2, 4, 8, 10, 12 threads
- Matches example report format
- Shows complete scaling behavior

### **2. Performance Statistics**
- perf stat style output
- CPU cycles and instructions
- Cache references and misses
- IPC (Instructions Per Cycle)
- Cache miss percentages

### **3. VTune-Style Metrics**
- Comprehensive metrics table
- CPI analysis
- Core utilization
- Cache-bound vs DRAM-bound
- Vectorization status
- Bottleneck identification

### **4. Multiple Methods (Q2)**
- Wavefront (anti-diagonal) parallelization
- Row-wise parallelization
- Direct comparison in output
- Shows why wavefront fails

### **5. Multiple Schedules (Q3)**
- Static scheduling
- Dynamic scheduling
- Guided scheduling
- Cache-blocked version (tile size 32)
- Performance comparison table

### **6. CSV Export**
- Ready for Excel/Python/MATLAB
- Easy graph creation
- Data in proper format

### **7. Analysis Summaries**
- Built-in analysis paragraphs
- Explains bottlenecks
- Interprets metrics
- Provides context

---

## 🔬 Understanding Results

### **Expected Patterns**

#### **Q1: Molecular Dynamics**
- ✅ Good speedup up to 8 threads (~5x)
- ⚠️ Efficiency drops at higher counts (47% at 12)
- 🔴 **Bottleneck:** Atomic operations causing synchronization overhead
- 📊 **Pattern:** Near-linear initially, then plateaus

#### **Q2: DNA Sequence Alignment**
- ❌ Wavefront: Speedup < 1 (WORSE than serial!)
- ⚠️ Row-wise: Limited improvement
- 🔴 **Bottleneck:** Data dependencies + barrier synchronization
- 📊 **Pattern:** Performance degrades with more threads

#### **Q3: Heat Diffusion**
- ✅ Best scalability (~4.6x at 8 threads)
- ✅ Guided scheduling performs best
- 🔴 **Bottleneck:** Cache bandwidth (not DRAM)
- 📊 **Pattern:** Smooth sub-linear scaling

---

## 📝 Report Writing Workflow

```
┌─────────────────────────────────────────────────────────┐
│ 1. RUN EXPERIMENTS                                      │
│    ./run_report_versions.sh                             │
│    ├── Generates output/*.txt files                     │
│    └── Generates *.csv files                            │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 2. GENERATE GRAPHS                                      │
│    python3 generate_graphs.py                           │
│    └── Creates graphs/*.png and *.pdf files             │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 3. OPEN REPORT_TEMPLATE.md                              │
│    Follow step-by-step instructions to:                 │
│    ├── Copy tables from output files                    │
│    ├── Insert graphs from graphs/ folder                │
│    ├── Write analysis using provided examples           │
│    └── Format in Word/LaTeX                             │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ 4. SUBMIT                                               │
│    └── Export to PDF and submit                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ System Requirements

### **Software**
- Ubuntu Linux (native or VirtualBox)
- g++ with OpenMP support
- Python 3 (for graphs)
- matplotlib and pandas (for graphs)

### **Installation**
```bash
# Compiler and OpenMP
sudo apt update
sudo apt install build-essential

# Python libraries for graphs
pip3 install matplotlib pandas numpy
```

---

## 📖 Documentation Hierarchy

Start here based on your needs:

```
New to the project?
└─→ Start with PROJECT_GUIDE.md (this gives you the big picture)
    └─→ Then read QUICKSTART.md (for commands)
        └─→ Finally read REPORT_TEMPLATE.md (for report creation)

Want detailed understanding?
└─→ Read ANALYSIS.md (20+ pages of in-depth analysis)

Need quick reference?
└─→ Check QUICKSTART.md (all commands in one place)

Original comprehensive docs?
└─→ See README.md (full technical documentation)
```

---

## ⚡ Common Issues & Solutions

### **Issue: "Permission denied" when running scripts**
```bash
chmod +x run_report_versions.sh
chmod +x generate_graphs.py
```

### **Issue: "Module not found" for matplotlib**
```bash
pip3 install --user matplotlib pandas numpy
```

### **Issue: "No such file or directory" for CSV**
**Solution:** Run `./run_report_versions.sh` first to generate CSV files

### **Issue: Different numbers than example**
**Solution:** This is NORMAL! Your hardware is different. Focus on **patterns** not exact values.

---

## ✅ Success Criteria

Your report is ready when you have:

- [ ] All three questions with execution tables
- [ ] Performance statistics for each question
- [ ] VTune metrics tables for each question
- [ ] Graphs for all three questions
- [ ] Analysis paragraphs explaining bottlenecks
- [ ] Professional formatting (Word/LaTeX → PDF)
- [ ] Your roll number and name on title page

---

## 🎓 What You'll Learn

This assignment teaches:

1. **OpenMP Programming**
   - Parallel loops, scheduling, synchronization
   - Atomic operations, reduction clauses
   - Load balancing strategies

2. **Performance Analysis**
   - Speedup and efficiency calculations
   - Bottleneck identification
   - Cache vs memory bandwidth effects

3. **Optimization Techniques**
   - Cache blocking/tiling
   - Scheduling strategy selection
   - When parallelization helps (and when it doesn't)

4. **Scientific Computing**
   - N-body simulations (Q1)
   - Dynamic programming (Q2)
   - Finite difference methods (Q3)

---

## 📞 Support

Having issues? Check these resources in order:

1. **QUICKSTART.md** - Quick command reference
2. **REPORT_TEMPLATE.md** - Report creation help
3. **PROJECT_GUIDE.md** - Complete overview
4. **ANALYSIS.md** - Detailed explanations
5. **README.md** - Technical documentation

---

## 🎉 You're All Set!

This enhanced solution provides everything needed for a **professional, publication-quality report**:

✅ Report-ready output format
✅ Automatic graph generation
✅ Step-by-step templates
✅ Complete analysis guidance
✅ Multiple test scenarios
✅ Performance metrics
✅ Bottleneck identification

**Follow the 3-step quick start above and you'll have your report done in under an hour!**

---

**Project Version:** Enhanced Report Version 2.0
**Last Updated:** February 10, 2026
**Course:** UCS645 - Parallel & Distributed Computing
**Assignment:** Lab 2 - OpenMP Performance Evaluation

**Good luck with your assignment!** 🚀
