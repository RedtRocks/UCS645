#!/usr/bin/env python3
# ============================================================================
# PERFORMANCE ANALYSIS AND VISUALIZATION TOOL
# Parses performance data and generates graphs and reports
# ============================================================================

import os
import re
import sys
import json
from pathlib import Path
from collections import defaultdict

# Try to import matplotlib for graphing
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Warning: matplotlib not available. Graphing will be skipped.")
    print("Install with: pip3 install matplotlib numpy")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

class PerformanceAnalyzer:
    def __init__(self, data_dir="performance_data"):
        self.data_dir = data_dir
        self.results = defaultdict(list)
        self.system_info = {}
        self.parse_data()

    def parse_data(self):
        """Parse all performance data files"""
        summary_file = Path(self.data_dir) / "performance_summary.txt"
        
        if not summary_file.exists():
            print(f"Error: {summary_file} not found")
            return
        
        with open(summary_file, 'r') as f:
            content = f.read()
        
        # Extract system information
        self.extract_system_info(content)
        
        # Extract test results
        self.extract_test_results(content)
    
    def extract_system_info(self, content):
        """Extract system information from summary file"""
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'Date:' in line:
                self.system_info['date'] = line.split('Date:', 1)[1].strip()
            elif 'Cores:' in line:
                self.system_info['cores'] = line.split('Cores:', 1)[1].strip()
            elif 'Memory:' in line:
                self.system_info['memory'] = line.split('Memory:', 1)[1].strip()
            elif 'CPU:' in line:
                self.system_info['cpu'] = line.split('CPU:', 1)[1].strip()
    
    def extract_test_results(self, content):
        """Extract timing and speedup information"""
        # Pattern to match execution times
        time_pattern = r'Execution time:\s*([\d.]+)\s*seconds'
        speedup_pattern = r'Speedup:\s*([\d.]+)x'
        efficiency_pattern = r'Efficiency:\s*([\d.]+)%'
        throughput_pattern = r'Throughput:\s*([\d.]+)\s*correlations/second'
        
        # Split by test
        test_blocks = content.split('TEST:')
        
        for block in test_blocks[1:]:  # Skip first split (header)
            test_name = block.split('\n')[0].strip()
            
            times = re.findall(time_pattern, block)
            speedups = re.findall(speedup_pattern, block)
            efficiencies = re.findall(efficiency_pattern, block)
            throughputs = re.findall(throughput_pattern, block)
            
            if times:
                self.results[test_name] = {
                    'times': [float(t) for t in times],
                    'speedups': [float(s) for s in speedups],
                    'efficiencies': [float(e) for e in efficiencies],
                    'throughputs': [float(t) for t in throughputs]
                }
    
    def generate_text_report(self):
        """Generate a text report of findings"""
        report_path = Path(self.data_dir) / "analysis_report.txt"
        
        with open(report_path, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("PERFORMANCE ANALYSIS REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("SYSTEM INFORMATION\n")
            f.write("-" * 80 + "\n")
            f.write(f"Date: {self.system_info.get('date', 'N/A')}\n")
            f.write(f"CPU Cores: {self.system_info.get('cores', 'N/A')}\n")
            f.write(f"Memory: {self.system_info.get('memory', 'N/A')}\n")
            f.write(f"CPU Model: {self.system_info.get('cpu', 'N/A')}\n")
            f.write("\n")
            
            f.write("KEY FINDINGS\n")
            f.write("-" * 80 + "\n\n")
            
            # Analyze results
            f.write("1. EXECUTION TIME ANALYSIS\n")
            f.write("   Fastest Test: {}\n".format(
                min(self.results.keys(), 
                    key=lambda k: min(self.results[k]['times'][0:1]) if self.results[k]['times'] else float('inf'),
                    default="N/A")
            ))
            
            f.write("\n2. SPEEDUP ANALYSIS\n")
            all_speedups = []
            for test, data in self.results.items():
                if data['speedups']:
                    all_speedups.extend(data['speedups'])
                    f.write(f"   {test}: {data['speedups']}\n")
            
            if all_speedups:
                f.write(f"   Average Speedup: {sum(all_speedups)/len(all_speedups):.2f}x\n")
                f.write(f"   Max Speedup: {max(all_speedups):.2f}x\n")
            
            f.write("\n3. EFFICIENCY ANALYSIS\n")
            all_efficiencies = []
            for test, data in self.results.items():
                if data['efficiencies']:
                    all_efficiencies.extend(data['efficiencies'])
                    f.write(f"   {test}: {data['efficiencies']}\n")
            
            if all_efficiencies:
                f.write(f"   Average Efficiency: {sum(all_efficiencies)/len(all_efficiencies):.1f}%\n")
            
            f.write("\n4. THROUGHPUT ANALYSIS\n")
            for test, data in self.results.items():
                if data['throughputs']:
                    f.write(f"   {test}: {data['throughputs']} correlations/sec\n")
            
            f.write("\n" + "=" * 80 + "\n")
        
        print(f"Report generated: {report_path}")
        return report_path
    
    def generate_graphs(self):
        """Generate performance graphs"""
        if not MATPLOTLIB_AVAILABLE or not NUMPY_AVAILABLE:
            print("Skipping graphs (matplotlib/numpy not available)")
            return
        
        print("Generating graphs...")
        
        # Graph 1: Speedup comparison
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Extract matrix size scaling data
        matrix_sizes = []
        seq_times = []
        omp_times = []
        opt_times = []
        
        for test_name, data in sorted(self.results.items()):
            if 'Matrix Size' in test_name:
                size = test_name.replace('Matrix Size ', '').strip()
                matrix_sizes.append(size)
                if len(data['times']) >= 3:
                    seq_times.append(data['times'][0])
                    omp_times.append(data['times'][1])
                    opt_times.append(data['times'][2])
        
        # Plot 1: Execution time vs matrix size
        if matrix_sizes:
            ax = axes[0, 0]
            x_pos = np.arange(len(matrix_sizes))
            width = 0.25
            
            ax.bar(x_pos - width, seq_times, width, label='Sequential', color='skyblue')
            ax.bar(x_pos, omp_times, width, label='OpenMP', color='orange')
            ax.bar(x_pos + width, opt_times, width, label='Optimized', color='green')
            
            ax.set_xlabel('Matrix Size')
            ax.set_ylabel('Execution Time (seconds)')
            ax.set_title('Execution Time vs Matrix Size (4 threads)')
            ax.set_xticks(x_pos)
            ax.set_xticklabels(matrix_sizes, rotation=45, ha='right')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        # Plot 2: Speedup vs threads
        thread_counts = []
        thread_speedups_omp = []
        thread_speedups_opt = []
        
        for test_name, data in sorted(self.results.items()):
            if 'Thread Count' in test_name:
                threads = int(test_name.replace('Thread Count ', '').strip())
                thread_counts.append(threads)
                if data['speedups'] and len(data['speedups']) >= 1:
                    thread_speedups_omp.append(data['speedups'][0])
                if data['speedups'] and len(data['speedups']) >= 2:
                    thread_speedups_opt.append(data['speedups'][1])
        
        if thread_counts:
            ax = axes[0, 1]
            ax.plot(thread_counts, thread_speedups_omp, 'o-', label='OpenMP', linewidth=2, markersize=8)
            ax.plot(thread_counts, thread_speedups_opt, 's-', label='Optimized', linewidth=2, markersize=8)
            
            # Add ideal scaling line
            if thread_counts:
                ideal = [1] + list(thread_counts[1:])
                ax.plot(thread_counts, ideal, '--', label='Ideal Scaling', color='gray', linewidth=2)
            
            ax.set_xlabel('Number of Threads')
            ax.set_ylabel('Speedup (x)')
            ax.set_title('Speedup vs Thread Count (500x5000 matrix)')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        # Plot 3: Efficiency vs threads
        if thread_counts:
            ax = axes[1, 0]
            thread_eff_omp = []
            thread_eff_opt = []
            
            for test_name, data in sorted(self.results.items()):
                if 'Thread Count' in test_name:
                    if data['efficiencies'] and len(data['efficiencies']) >= 1:
                        thread_eff_omp.append(data['efficiencies'][0])
                    if data['efficiencies'] and len(data['efficiencies']) >= 2:
                        thread_eff_opt.append(data['efficiencies'][1])
            
            if thread_eff_omp:
                ax.plot(thread_counts, thread_eff_omp, 'o-', label='OpenMP', linewidth=2, markersize=8)
            if thread_eff_opt:
                ax.plot(thread_counts, thread_eff_opt, 's-', label='Optimized', linewidth=2, markersize=8)
            
            ax.axhline(y=100, color='gray', linestyle='--', label='Perfect Efficiency')
            ax.set_xlabel('Number of Threads')
            ax.set_ylabel('Efficiency (%)')
            ax.set_title('Parallel Efficiency vs Thread Count')
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.set_ylim([0, 105])
        
        # Plot 4: Summary statistics
        ax = axes[1, 1]
        ax.axis('off')
        
        # Calculate statistics
        stats_text = "SUMMARY STATISTICS\n" + "=" * 40 + "\n\n"
        
        all_speedups = []
        for test, data in self.results.items():
            all_speedups.extend(data['speedups'])
        
        if all_speedups:
            stats_text += f"Average Speedup: {np.mean(all_speedups):.2f}x\n"
            stats_text += f"Max Speedup: {np.max(all_speedups):.2f}x\n"
            stats_text += f"Min Speedup: {np.min(all_speedups):.2f}x\n"
        
        stats_text += f"\nTotal Tests Run: {len(self.results)}\n"
        
        ax.text(0.1, 0.9, stats_text, transform=ax.transAxes,
                fontsize=10, verticalalignment='top', family='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        graph_path = Path(self.data_dir) / "performance_graphs.png"
        plt.savefig(graph_path, dpi=150, bbox_inches='tight')
        print(f"Graphs saved to: {graph_path}")
        plt.close()

def main():
    data_dir = "performance_data"
    
    if len(sys.argv) > 1:
        data_dir = sys.argv[1]
    
    print("=" * 80)
    print("PERFORMANCE ANALYSIS TOOL")
    print("=" * 80)
    print()
    
    analyzer = PerformanceAnalyzer(data_dir)
    
    print("System Information:")
    for key, value in analyzer.system_info.items():
        print(f"  {key}: {value}")
    print()
    
    print(f"Tests analyzed: {len(analyzer.results)}")
    print()
    
    # Generate reports
    analyzer.generate_text_report()
    analyzer.generate_graphs()
    
    print()
    print("Analysis complete!")
    print(f"Output directory: {data_dir}")

if __name__ == "__main__":
    main()

