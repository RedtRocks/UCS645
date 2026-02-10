# Report Template for Lab Assignment 2
## How to Create Your Report from the Generated Data

---

## Report Structure (Like Example PDF)

Your report should follow this structure:

```
Title Page
├── Lab Assignment-2
├── Your Roll Number {Your Name}

For Each Question (Q1, Q2, Q3):
├── Question Title
├── Execution Table(s)
├── Performance Statistics (perf stat)
├── Analysis Paragraph
├── VTune Stats Table
├── Detailed Analysis Paragraph
└── Graph (Threads vs Speedup)
```

---

## Step-by-Step Instructions

### **Step 1: Run the Report Versions**

```bash
cd Lab2
chmod +x run_report_versions.sh
./run_report_versions.sh
```

This will generate:
- `output/q1_report_output.txt`
- `output/q2_report_output.txt`
- `output/q3_report_output.txt`
- `q1_molecular_dynamics_data.csv`
- `q2_dna_alignment_data.csv`
- `q3_heat_diffusion_data.csv`

---

### **Step 2: Copy Tables for Your Report**

#### **Question 1: Molecular Dynamics**

**Copy THIS section from `output/q1_report_output.txt`:**

```
Threads    Time (s)        Speedup    Efficiency
========================================================
1          0.023846        1.00       x100.0
2          0.011534        2.07       x103.4
4          0.006656        3.58       x89.6
8          0.004779        4.99       x62.4
10         0.004851        4.92       x49.2
12         0.004199        5.68       x47.3
```

**Format as table in your report:**

| Threads | Time (s) | Speedup | Efficiency |
|---------|----------|---------|------------|
| 1       | 0.023846 | 1.00    | x100.0     |
| 2       | 0.011534 | 2.07    | x103.4     |
| ...     | ...      | ...     | ...        |

---

#### **Question 2: DNA Sequence Alignment**

You'll have **TWO tables**:

**Table 1: Wavefront Parallelization**
```
Threads    Time (s)        Speedup    Efficiency
--------------------------------------------------------
1          0.008492        1.00       x100.0
2          0.016714        0.51       x25.4
4          0.017579        0.48       x12.1
8          0.020430        0.42       x5.2
```

**Table 2: Row-wise Parallelization**
```
Threads    Time (s)        Speedup    Efficiency
--------------------------------------------------------
1          0.007243        1.00       x100.0
2          0.007314        0.99       x49.5
4          0.007518        0.96       x24.1
8          0.010126        0.72       x8.9
```

---

#### **Question 3: Heat Diffusion**

You'll have **FOUR tables** (one for each scheduling strategy):

**Table 1: Static Scheduling**
```
Threads    Time (s)        Speedup    Efficiency
------------------------------------------------------
1          0.513220        1.00       x100.0
2          0.268517        1.91       x95.6
4          0.156674        3.28       x81.9
8          0.127079        4.04       x50.5
```

**Table 2: Dynamic Scheduling**
**Table 3: Guided Scheduling**
**Table 4: Cache-Blocked Version**

---

### **Step 3: Copy Performance Statistics (perf stat)**

**Example from output files:**

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

**Copy this section directly into your report** under each question.

---

### **Step 4: VTune Metrics Tables**

**Example structure:**

| Metric | Observed Value | Interpretation |
|--------|---------------|----------------|
| CPI (Cycles Per Instruction) | 0.58 | Low CPI indicates efficient instruction execution |
| Effective Physical Core Utilization | ~14–22% (≈1.1–1.75 out of 8 cores) | Many physical cores remain underutilized |
| Cache Bound (Overall) | ~35–37% of clock cycles | Significant portion of execution time waiting for cache |
| ... | ... | ... |

**Copy the VTune tables from the output files and paste into your report.**

---

### **Step 5: Create Graphs**

#### **Option A: Using Excel**

1. Open `q1_molecular_dynamics_data.csv`
2. Select columns: `Threads`, `Speedup`
3. Insert → Chart → Line Chart
4. Format labels: "Threads vs Speedup"
5. Save as image

#### **Option B: Using Python**

```python
import pandas as pd
import matplotlib.pyplot as plt

# Read data
df = pd.read_csv('q1_molecular_dynamics_data.csv')

# Create graph
plt.figure(figsize=(8, 6))
plt.plot(df['Threads'], df['Speedup'], marker='o', linewidth=2, markersize=8)
plt.xlabel('Threads')
plt.ylabel('Speedup')
plt.title('Molecular Dynamics (Lennard-Jones): Threads vs Speedup')
plt.grid(True, alpha=0.3)
plt.axhline(y=1.0, color='gray', linestyle='--', label='Serial Baseline (1.0x)')
plt.legend()
plt.savefig('q1_speedup_graph.png', dpi=300, bbox_inches='tight')
plt.show()
```

#### **Option C: Using MATLAB**

```matlab
data = readtable('q1_molecular_dynamics_data.csv');
plot(data.Threads, data.Speedup, '-o', 'LineWidth', 2, 'MarkerSize', 8);
xlabel('Threads');
ylabel('Speedup');
title('Molecular Dynamics (Lennard-Jones): Threads vs Speedup');
grid on;
saveas(gcf, 'q1_speedup_graph.png');
```

**For Q2:** Plot both Wavefront and Row-wise on same graph with different colors
**For Q3:** Plot all four scheduling strategies on same graph

---

### **Step 6: Write Analysis Paragraphs**

#### **Format from Example Report:**

**After Execution Table:**
Write 1-2 paragraphs explaining:
- What the experiment does
- Observed execution times
- Speedup pattern (linear, sub-linear)
- Efficiency at different thread counts
- Main findings

**Example:**
```
In this experiment, a parallel molecular dynamics simulation for Lennard-Jones
force calculation was implemented using OpenMP for a system of 1000 particles
with a cutoff distance of 2.5. The program computes inter-particle forces
efficiently, and the observed execution times decrease consistently as the
number of threads increases, indicating correct parallelization without
functional errors.

The performance results show near-linear speedup up to 8 threads, achieving
a speedup of 4.99×. Beyond this point, performance gains begin to saturate,
with a maximum speedup of 5.68× observed at 12 threads and an efficiency of
47.3%. This reduction in efficiency at higher thread counts is attributed to
increased memory access contention, cache misses, and synchronization overhead
rather than flaws in the algorithm.
```

**After VTune Table:**
Write 2-3 paragraphs explaining:
- VTune analysis findings
- CPI, cache behavior, memory bandwidth
- Core utilization
- Bottleneck identification
- Why performance is limited

**Example structure from report:**
```
VTune memory analysis shows that the application is not DRAM-bound, as the
observed memory bandwidth (~3.4 GB/s) is far below the platform peak of 57 GB/s.
Instead, the program is mainly cache-bound, with a noticeable amount of time
spent on L1 cache accesses. The very low DRAM-bound percentage confirms that
main memory is not the performance bottleneck.

Microarchitecture analysis reports a low CPI (~0.58), indicating efficient
instruction execution. However, physical core utilization remains low (14–22%),
suggesting that performance is limited by cache stalls, synchronization overhead,
and lack of vectorization rather than raw computation. Overall, OpenMP
parallelization improves execution time, but scalability is constrained by
cache behaviour and memory access patterns rather than compute capability.
```

---

### **Step 7: Put It All Together**

**Final Report Structure:**

```
========================================
Lab Assignment-2
[Your Roll Number] {Your Name}
========================================

Q.1> Molecular Dynamics – Force Calculation:

Execution Table:-
[Paste Table Here]

->Performance Statistics:-(perf stat)
[Paste perf stat output here]

[Analysis Paragraph 1]
[Analysis Paragraph 2]

->VTUNE STATS
[Paste VTune Table Here]

[Analysis Paragraph 3]
[Analysis Paragraph 4]

[Graph Image]

========================================

Q.2> BIOINFORMATICS_DNA SEQUENCE ALIGNMENT:-

EXECUTION TABLE:-
WAVEFRONT PARALLELIZATION (ANTI-DIAGONAL)
[Paste Table 1]

ROW-WISE PARALLELISATION(SIMPLER, BUT LIMITED)
[Paste Table 2]

PERFORMANCE STATISTICS:- (perf stat)
[Paste perf output]

[Analysis Paragraphs]

VTUNE STATS
[Paste VTune Table]

[Analysis Paragraphs]

[Graph comparing both methods]

========================================

Q.3 Scientific Computing - Heat Diffusion Simulation:-

-> STATIC SCHEDULING
[Table 1]

->DYNAMIC SCHEDULING
[Table 2]

->GUIDED SCHEDULING
[Table 3]

->CACHE BLOCK VERSION(BLOCK SIZE:32)
[Table 4]

Execution & Performance Statistics (perf stat)
[Paste perf output]

[Analysis Paragraphs]

[VTune Table]

[Analysis Paragraphs]

[Graph comparing all scheduling strategies]

========================================
```

---

## Quick Checklist

- [ ] Run `./run_report_versions.sh`
- [ ] Copy execution tables from output files
- [ ] Copy perf stats sections
- [ ] Copy VTune metrics tables
- [ ] Create graphs from CSV files
- [ ] Write analysis paragraphs (use provided summaries as guide)
- [ ] Format everything in Word/LaTeX
- [ ] Include your roll number and name
- [ ] Export as PDF

---

## Key Points for Analysis Writing

### **Question 1:**
- Mention: atomic operations, synchronization overhead, cache contention
- Explain: why efficiency drops at 8+ threads
- Compare: actual results with Amdahl's Law prediction

### **Question 2:**
- Mention: data dependencies, barrier synchronization, wavefront limitations
- Explain: why speedup < 1 for wavefront (worse than serial!)
- Compare: wavefront vs row-wise approaches

### **Question 3:**
- Mention: stencil computation, cache locality, memory patterns
- Explain: why guided scheduling performs best
- Compare: all four scheduling strategies
- Note: cache-blocking improvement

---

## Graph Requirements

**Must create 4 graphs total:**

1. **Q1:** Threads vs Speedup (single line)
2. **Q2:** Threads vs Speedup (two lines: Wavefront vs Row-wise)
3. **Q3:** Threads vs Speedup (four lines: all scheduling strategies)

**Graph formatting:**
- X-axis: Threads (1, 2, 4, 8, 10, 12)
- Y-axis: Speedup
- Include baseline at y=1.0 (dotted line)
- Use different colors/markers for each method
- Add legend
- Add grid for readability

---

## Common Mistakes to Avoid

❌ **Don't:**
- Copy-paste without understanding
- Skip the VTune metrics table
- Forget to explain WHY performance degrades
- Use vague language like "performance is good"

✅ **Do:**
- Explain specific bottlenecks (atomics, dependencies, cache misses)
- Use data from your tables in analysis
- Compare with theoretical predictions
- Be specific about percentages and measurements

---

**Your report should look professional and data-driven, just like the example PDF!**

Good luck! 🎉
