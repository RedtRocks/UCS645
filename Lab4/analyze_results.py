#!/usr/bin/env python3
"""
Lab4 MPI Results Analysis
Generates tables and graphs from timing results
"""

import csv
import sys
from pathlib import Path
from collections import defaultdict

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


def load_results(filename="timing_results.csv"):
    """Load timing results from CSV file."""
    results = defaultdict(dict)
    
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                prog = row['Program']
                np_val = int(row['Processes'])
                time_sec = float(row['Time_Seconds'])
                speedup = float(row['Speedup'])
                efficiency = float(row['Efficiency'])
                
                results[prog][np_val] = {
                    'time': time_sec,
                    'speedup': speedup,
                    'efficiency': efficiency
                }
    except FileNotFoundError:
        print(f"Error: {filename} not found. Run './run_tests.sh' first.")
        sys.exit(1)
    
    return results


def print_summary_table(results):
    """Print formatted summary table."""
    print("\n" + "="*80)
    print("EXECUTION TIME SUMMARY (seconds)")
    print("="*80)
    
    # Get all processor counts
    all_procs = set()
    for prog_data in results.values():
        all_procs.update(prog_data.keys())
    all_procs = sorted(list(all_procs))
    
    # Header
    header = "Program".ljust(20)
    for np_val in all_procs:
        header += f"np={np_val}".center(12)
    print(header)
    print("-" * len(header))
    
    # Data rows
    for prog in sorted(results.keys()):
        row = prog.ljust(20)
        for np_val in all_procs:
            if np_val in results[prog]:
                time_val = results[prog][np_val]['time']
                row += f"{time_val:>10.4f}s".rjust(12)
            else:
                row += "    N/A    ".rjust(12)
        print(row)
    
    print()


def print_speedup_table(results):
    """Print speedup relative to single process."""
    print("="*80)
    print("SPEEDUP vs 1 PROCESS")
    print("="*80)
    
    all_procs = set()
    for prog_data in results.values():
        all_procs.update(prog_data.keys())
    all_procs = sorted(list(all_procs))
    
    header = "Program".ljust(20)
    for np_val in all_procs:
        header += f"np={np_val}".center(12)
    print(header)
    print("-" * len(header))
    
    for prog in sorted(results.keys()):
        row = prog.ljust(20)
        for np_val in all_procs:
            if np_val in results[prog]:
                speedup = results[prog][np_val]['speedup']
                row += f"{speedup:>9.2f}x".rjust(12)
            else:
                row += "    N/A    ".rjust(12)
        print(row)
    
    print()


def print_efficiency_table(results):
    """Print efficiency percentage."""
    print("="*80)
    print("EFFICIENCY (%)")
    print("="*80)
    
    all_procs = set()
    for prog_data in results.values():
        all_procs.update(prog_data.keys())
    all_procs = sorted(list(all_procs))
    
    header = "Program".ljust(20)
    for np_val in all_procs:
        header += f"np={np_val}".center(12)
    print(header)
    print("-" * len(header))
    
    for prog in sorted(results.keys()):
        row = prog.ljust(20)
        for np_val in all_procs:
            if np_val in results[prog]:
                eff = results[prog][np_val]['efficiency']
                row += f"{eff:>7.1f}%".rjust(12)
            else:
                row += "    N/A    ".rjust(12)
        print(row)
    
    print()


def plot_execution_times(results):
    """Plot execution time vs processor count."""
    plt.figure(figsize=(10, 6))
    
    for prog in sorted(results.keys()):
        procs = sorted(results[prog].keys())
        times = [results[prog][p]['time'] for p in procs]
        plt.plot(procs, times, marker='o', label=prog, linewidth=2, markersize=8)
    
    plt.xlabel('Number of Processes', fontsize=12, fontweight='bold')
    plt.ylabel('Execution Time (seconds)', fontsize=12, fontweight='bold')
    plt.title('Execution Time vs Number of Processes', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xticks(sorted(set(p for prog_data in results.values() for p in prog_data.keys())))
    plt.tight_layout()
    plt.savefig('execution_times.png', dpi=150)
    print("✓ Saved: execution_times.png")
    plt.close()


def plot_speedup(results):
    """Plot speedup vs processor count."""
    plt.figure(figsize=(10, 6))
    
    all_procs = sorted(set(p for prog_data in results.values() for p in prog_data.keys()))
    
    for prog in sorted(results.keys()):
        procs = sorted(results[prog].keys())
        speedups = [results[prog][p]['speedup'] for p in procs]
        plt.plot(procs, speedups, marker='s', label=prog, linewidth=2, markersize=8)
    
    # Add ideal speedup line
    plt.plot(all_procs, all_procs, 'k--', label='Ideal (linear)', linewidth=2, alpha=0.5)
    
    plt.xlabel('Number of Processes', fontsize=12, fontweight='bold')
    plt.ylabel('Speedup', fontsize=12, fontweight='bold')
    plt.title('Speedup vs Number of Processes', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xticks(all_procs)
    plt.tight_layout()
    plt.savefig('speedup.png', dpi=150)
    print("✓ Saved: speedup.png")
    plt.close()


def plot_efficiency(results):
    """Plot efficiency vs processor count."""
    plt.figure(figsize=(10, 6))
    
    for prog in sorted(results.keys()):
        procs = sorted(results[prog].keys())
        efficiencies = [results[prog][p]['efficiency'] for p in procs]
        plt.plot(procs, efficiencies, marker='^', label=prog, linewidth=2, markersize=8)
    
    plt.axhline(y=100, color='k', linestyle='--', label='Perfect efficiency', alpha=0.5)
    plt.xlabel('Number of Processes', fontsize=12, fontweight='bold')
    plt.ylabel('Efficiency (%)', fontsize=12, fontweight='bold')
    plt.title('Parallel Efficiency vs Number of Processes', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 105)
    plt.xticks(sorted(set(p for prog_data in results.values() for p in prog_data.keys())))
    plt.tight_layout()
    plt.savefig('efficiency.png', dpi=150)
    print("✓ Saved: efficiency.png")
    plt.close()


def plot_comparison_bars(results):
    """Plot side-by-side bar chart comparing programs at each processor count."""
    all_procs = sorted(set(p for prog_data in results.values() for p in prog_data.keys()))
    programs = sorted(results.keys())
    
    fig, axes = plt.subplots(1, len(all_procs), figsize=(16, 5), sharey=True)
    if len(all_procs) == 1:
        axes = [axes]
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(programs)))
    
    for idx, np_val in enumerate(all_procs):
        times = []
        labels = []
        
        for prog in programs:
            if np_val in results[prog]:
                times.append(results[prog][np_val]['time'])
                labels.append(prog.replace('q', 'Ex').replace('_', ' '))
            else:
                times.append(0)
                labels.append('')
        
        # Filter out empty
        times = [t for t, l in zip(times, labels) if l]
        labels = [l for l in labels if l]
        
        axes[idx].bar(range(len(labels)), times, color=colors[:len(labels)])
        axes[idx].set_title(f'{np_val} Process{"es" if np_val > 1 else ""}', 
                           fontsize=11, fontweight='bold')
        axes[idx].set_xticks(range(len(labels)))
        axes[idx].set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
        if idx == 0:
            axes[idx].set_ylabel('Time (seconds)', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('comparison_bars.png', dpi=150)
    print("✓ Saved: comparison_bars.png")
    plt.close()


def main():
    """Main analysis pipeline."""
    print("\n" + "="*80)
    print("Lab4 MPI Performance Analysis")
    print("="*80)
    
    results = load_results()
    
    # Print tables
    print_summary_table(results)
    print_speedup_table(results)
    print_efficiency_table(results)
    
    # Generate graphs
    print("\nGenerating graphs...")
    try:
        plot_execution_times(results)
        plot_speedup(results)
        plot_efficiency(results)
        plot_comparison_bars(results)
        
        print("\n" + "="*80)
        print("All graphs saved successfully!")
        print("="*80)
        print("\nGenerated files:")
        print("  • execution_times.png")
        print("  • speedup.png")
        print("  • efficiency.png")
        print("  • comparison_bars.png")
        print()
        
    except ImportError as e:
        print(f"\nWarning: Could not generate graphs ({e})")
        print("To fix: pip install matplotlib numpy")
        

if __name__ == '__main__':
    main()
