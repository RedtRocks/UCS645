#!/usr/bin/env python3
# ============================================================================
# CSV EXPORT TOOL FOR PERFORMANCE DATA
# Converts performance_summary.txt to CSV for Excel/spreadsheet analysis
# ============================================================================

import re
import csv
import sys
from pathlib import Path
from collections import defaultdict

class CSVExporter:
    def __init__(self, data_dir="performance_data"):
        self.data_dir = Path(data_dir)
        self.summary_file = self.data_dir / "performance_summary.txt"
        self.results = []
        
    def parse_summary_file(self):
        """Parse performance_summary.txt and extract data"""
        
        if not self.summary_file.exists():
            print(f"Error: {self.summary_file} not found")
            return False
        
        with open(self.summary_file, 'r') as f:
            content = f.read()
        
        # Split into test blocks
        test_blocks = content.split('TEST:')
        
        for block in test_blocks[1:]:  # Skip header
            lines = block.split('\n')
            test_name = lines[0].strip()
            
            # Parse configuration from test name and output
            matrix_match = re.search(r'(\d+)x(\d+)', test_name)
            threads_match = re.search(r'Threads: (\d+)', block)
            version_match = re.search(r'Version: (\w+)', block)
            
            ny = int(matrix_match.group(1)) if matrix_match else 0
            nx = int(matrix_match.group(2)) if matrix_match else 0
            threads = int(threads_match.group(1)) if threads_match else 0
            version = version_match.group(1) if version_match else "all"
            
            # Extract timing information
            times = re.findall(r'Execution time:\s*([\d.]+)\s*seconds', block)
            speedups = re.findall(r'Speedup:\s*([\d.]+)x', block)
            efficiencies = re.findall(r'Efficiency:\s*([\d.]+)%', block)
            throughputs = re.findall(r'Throughput:\s*([\d.]+)', block)
            
            # Store results
            result = {
                'test_name': test_name,
                'ny': ny,
                'nx': nx,
                'matrix_elements': ny * nx,
                'correlation_pairs': int(ny * (ny + 1) / 2),
                'threads': threads,
                'version': version,
                'seq_time': float(times[0]) if len(times) > 0 else None,
                'omp_time': float(times[1]) if len(times) > 1 else None,
                'opt_time': float(times[2]) if len(times) > 2 else None,
                'omp_speedup': float(speedups[0]) if len(speedups) > 0 else None,
                'opt_speedup': float(speedups[1]) if len(speedups) > 1 else None,
                'omp_efficiency': float(efficiencies[0]) if len(efficiencies) > 0 else None,
                'opt_efficiency': float(efficiencies[1]) if len(efficiencies) > 1 else None,
                'seq_throughput': float(throughputs[0]) if len(throughputs) > 0 else None,
                'omp_throughput': float(throughputs[1]) if len(throughputs) > 1 else None,
                'opt_throughput': float(throughputs[2]) if len(throughputs) > 2 else None,
            }
            
            self.results.append(result)
        
        return True
    
    def export_to_csv(self):
        """Export results to CSV file"""
        
        csv_file = self.data_dir / "performance_data.csv"
        
        if not self.results:
            print("No data to export")
            return False
        
        with open(csv_file, 'w', newline='') as f:
            fieldnames = [
                'test_name', 'ny', 'nx', 'matrix_elements', 'correlation_pairs',
                'threads', 'version',
                'seq_time', 'omp_time', 'opt_time',
                'omp_speedup', 'opt_speedup',
                'omp_efficiency', 'opt_efficiency',
                'seq_throughput', 'omp_throughput', 'opt_throughput'
            ]
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in self.results:
                writer.writerow(result)
        
        print(f"CSV exported to: {csv_file}")
        return True
    
    def export_performance_summary_csv(self):
        """Export a summary CSV with key metrics only"""
        
        csv_file = self.data_dir / "performance_summary.csv"
        
        summary_data = []
        
        # Group by matrix size
        by_size = defaultdict(list)
        for result in self.results:
            key = f"{result['ny']}x{result['nx']}"
            by_size[key].append(result)
        
        for size_key, results in sorted(by_size.items()):
            # Get one representative result (preferably version='all')
            rep = next((r for r in results if r['version'] == 'all'), results[0])
            
            summary_data.append({
                'matrix_size': size_key,
                'ny': rep['ny'],
                'nx': rep['nx'],
                'threads': rep['threads'],
                'sequential_time': rep['seq_time'],
                'openmp_time': rep['omp_time'],
                'optimized_time': rep['opt_time'],
                'omp_speedup': rep['omp_speedup'],
                'opt_speedup': rep['opt_speedup'],
                'omp_efficiency': rep['omp_efficiency'],
                'opt_efficiency': rep['opt_efficiency'],
            })
        
        with open(csv_file, 'w', newline='') as f:
            if summary_data:
                fieldnames = summary_data[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(summary_data)
        
        print(f"Summary CSV exported to: {csv_file}")
        return True

def main():
    print("=" * 80)
    print("PERFORMANCE DATA CSV EXPORT TOOL")
    print("=" * 80)
    print()
    
    data_dir = "performance_data"
    
    if len(sys.argv) > 1:
        data_dir = sys.argv[1]
    
    exporter = CSVExporter(data_dir)
    
    print(f"Reading from: {exporter.summary_file}")
    
    if not exporter.parse_summary_file():
        sys.exit(1)
    
    print(f"Found {len(exporter.results)} test results")
    print()
    
    # Export both CSV files
    exporter.export_to_csv()
    exporter.export_performance_summary_csv()
    
    print()
    print("CSV export complete!")
    print()
    print("You can now:")
    print("1. Open performance_data.csv in Excel for detailed analysis")
    print("2. Open performance_summary.csv for quick comparison")
    print("3. Create custom pivot tables and charts")

if __name__ == "__main__":
    main()

