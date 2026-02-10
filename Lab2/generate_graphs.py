#!/usr/bin/env python3
"""
Automatic Graph Generation for Lab Assignment 2
Reads CSV files and generates publication-quality graphs
Run after executing the report versions: python3 generate_graphs.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Set style for better-looking graphs
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (10, 7)
plt.rcParams['font.size'] = 12
plt.rcParams['lines.linewidth'] = 2.5
plt.rcParams['lines.markersize'] = 10

def create_output_directory():
    """Create graphs directory if it doesn't exist"""
    if not os.path.exists('graphs'):
        os.makedirs('graphs')
    print("✓ Created 'graphs' directory")

def plot_q1_molecular_dynamics():
    """Generate graph for Question 1: Molecular Dynamics"""
    try:
        df = pd.read_csv('q1_molecular_dynamics_data.csv')

        plt.figure(figsize=(10, 7))
        plt.plot(df['Threads'], df['Speedup'],
                marker='o', color='#2E7D32', linewidth=2.5, markersize=10,
                label='Observed Speedup')

        # Add ideal linear speedup line
        ideal = df['Threads'].values
        plt.plot(df['Threads'], ideal, '--', color='gray', linewidth=2,
                alpha=0.7, label='Ideal Linear Speedup')

        plt.xlabel('Threads', fontsize=14, fontweight='bold')
        plt.ylabel('Speedup', fontsize=14, fontweight='bold')
        plt.title('Molecular Dynamics (Lennard-Jones): Threads vs Speedup',
                 fontsize=16, fontweight='bold', pad=20)
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=12, loc='upper left')
        plt.xticks(df['Threads'])
        plt.ylim(bottom=0)

        # Add annotations for key points
        max_speedup = df['Speedup'].max()
        max_threads = df.loc[df['Speedup'].idxmax(), 'Threads']
        plt.annotate(f'Max: {max_speedup:.2f}x @ {max_threads} threads',
                    xy=(max_threads, max_speedup),
                    xytext=(max_threads-1, max_speedup+0.5),
                    arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                    fontsize=11, color='red', fontweight='bold')

        plt.tight_layout()
        plt.savefig('graphs/q1_speedup.png', dpi=300, bbox_inches='tight')
        plt.savefig('graphs/q1_speedup.pdf', bbox_inches='tight')
        print("✓ Generated Q1 graph: graphs/q1_speedup.png")
        plt.close()

    except FileNotFoundError:
        print("✗ Error: q1_molecular_dynamics_data.csv not found. Run ./q1_report first.")
    except Exception as e:
        print(f"✗ Error generating Q1 graph: {e}")

def plot_q2_dna_alignment():
    """Generate graph for Question 2: DNA Sequence Alignment"""
    try:
        df = pd.read_csv('q2_dna_alignment_data.csv')

        plt.figure(figsize=(10, 7))

        # Plot Wavefront data
        wavefront = df[df['Method'] == 'Wavefront']
        plt.plot(wavefront['Threads'], wavefront['Speedup'],
                marker='o', color='#1565C0', linewidth=2.5, markersize=10,
                label='Wavefront (Anti-diagonal)')

        # Plot Row-wise data
        rowwise = df[df['Method'] == 'Row-wise']
        plt.plot(rowwise['Threads'], rowwise['Speedup'],
                marker='s', color='#F57C00', linewidth=2.5, markersize=10,
                label='Row-wise Parallelisation')

        # Add serial baseline
        plt.axhline(y=1.0, color='gray', linestyle='--', linewidth=2,
                   alpha=0.7, label='Serial Baseline (1.0x)')

        plt.xlabel('Threads', fontsize=14, fontweight='bold')
        plt.ylabel('Speedup', fontsize=14, fontweight='bold')
        plt.title('DNA Sequence Alignment: Threads vs Speedup',
                 fontsize=16, fontweight='bold', pad=20)
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=12, loc='best')
        plt.xticks(wavefront['Threads'])

        # Annotate the poor performance
        plt.text(6, 0.5, 'Wavefront shows\nperformance degradation\ndue to dependencies',
                fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.tight_layout()
        plt.savefig('graphs/q2_speedup.png', dpi=300, bbox_inches='tight')
        plt.savefig('graphs/q2_speedup.pdf', bbox_inches='tight')
        print("✓ Generated Q2 graph: graphs/q2_speedup.png")
        plt.close()

    except FileNotFoundError:
        print("✗ Error: q2_dna_alignment_data.csv not found. Run ./q2_report first.")
    except Exception as e:
        print(f"✗ Error generating Q2 graph: {e}")

def plot_q3_heat_diffusion():
    """Generate graph for Question 3: Heat Diffusion with all scheduling strategies"""
    try:
        df = pd.read_csv('q3_heat_diffusion_data.csv')

        plt.figure(figsize=(11, 7))

        colors = {
            'Static': '#D32F2F',
            'Dynamic': '#1976D2',
            'Guided': '#388E3C',
            'Cache-Blocked': '#F57C00'
        }

        markers = {
            'Static': 'o',
            'Dynamic': 's',
            'Guided': '^',
            'Cache-Blocked': 'D'
        }

        # Plot each scheduling strategy
        for schedule in df['Schedule'].unique():
            data = df[df['Schedule'] == schedule]
            plt.plot(data['Threads'], data['Speedup'],
                    marker=markers.get(schedule, 'o'),
                    color=colors.get(schedule, 'blue'),
                    linewidth=2.5, markersize=10,
                    label=schedule)

        # Add ideal linear speedup
        threads = df[df['Schedule'] == 'Static']['Threads'].values
        plt.plot(threads, threads, '--', color='gray', linewidth=2,
                alpha=0.7, label='Ideal Linear Speedup')

        plt.xlabel('Threads', fontsize=14, fontweight='bold')
        plt.ylabel('Speedup', fontsize=14, fontweight='bold')
        plt.title('2D Heat Diffusion Simulation: Scheduling Strategy Comparison (Up to 8 Threads)',
                 fontsize=16, fontweight='bold', pad=20)
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=11, loc='upper left')
        plt.xticks(threads)
        plt.ylim(bottom=0)

        # Find best performing
        max_row = df.loc[df['Speedup'].idxmax()]
        plt.annotate(f"Best: {max_row['Schedule']}\n{max_row['Speedup']:.2f}x @ {max_row['Threads']} threads",
                    xy=(max_row['Threads'], max_row['Speedup']),
                    xytext=(max_row['Threads']-1.5, max_row['Speedup']+0.4),
                    arrowprops=dict(arrowstyle='->', color='darkgreen', lw=1.5),
                    fontsize=10, color='darkgreen', fontweight='bold',
                    bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))

        plt.tight_layout()
        plt.savefig('graphs/q3_speedup.png', dpi=300, bbox_inches='tight')
        plt.savefig('graphs/q3_speedup.pdf', bbox_inches='tight')
        print("✓ Generated Q3 graph: graphs/q3_speedup.png")
        plt.close()

    except FileNotFoundError:
        print("✗ Error: q3_heat_diffusion_data.csv not found. Run ./q3_report first.")
    except Exception as e:
        print(f"✗ Error generating Q3 graph: {e}")

def plot_efficiency_comparison():
    """Generate bonus efficiency comparison graph for all three questions"""
    try:
        # Read all data
        q1 = pd.read_csv('q1_molecular_dynamics_data.csv')
        q2_wave = pd.read_csv('q2_dna_alignment_data.csv')
        q2_wave = q2_wave[q2_wave['Method'] == 'Wavefront']
        q3_guided = pd.read_csv('q3_heat_diffusion_data.csv')
        q3_guided = q3_guided[q3_guided['Schedule'] == 'Guided']

        plt.figure(figsize=(10, 7))

        # Extract efficiency columns (convert from percentage)
        plt.plot(q1['Threads'], q1['Efficiency(%)'],
                marker='o', linewidth=2.5, markersize=10,
                label='Q1: Molecular Dynamics')
        plt.plot(q2_wave['Threads'], q2_wave['Efficiency(%)'],
                marker='s', linewidth=2.5, markersize=10,
                label='Q2: DNA Alignment (Wavefront)')
        plt.plot(q3_guided['Threads'], q3_guided['Efficiency(%)'],
                marker='^', linewidth=2.5, markersize=10,
                label='Q3: Heat Diffusion (Guided)')

        plt.axhline(y=100, color='gray', linestyle='--', linewidth=2,
                   alpha=0.7, label='Ideal Efficiency (100%)')
        plt.axhline(y=70, color='orange', linestyle=':', linewidth=1.5,
                   alpha=0.7, label='Good Efficiency Threshold (70%)')

        plt.xlabel('Threads', fontsize=14, fontweight='bold')
        plt.ylabel('Efficiency (%)', fontsize=14, fontweight='bold')
        plt.title('Parallel Efficiency Comparison Across All Questions',
                 fontsize=16, fontweight='bold', pad=20)
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=11, loc='upper right')
        plt.xticks(q1['Threads'])
        plt.ylim([0, 110])

        plt.tight_layout()
        plt.savefig('graphs/efficiency_comparison.png', dpi=300, bbox_inches='tight')
        plt.savefig('graphs/efficiency_comparison.pdf', bbox_inches='tight')
        print("✓ Generated bonus graph: graphs/efficiency_comparison.png")
        plt.close()

    except Exception as e:
        print(f"⚠ Could not generate efficiency comparison (optional): {e}")

def generate_summary_stats():
    """Generate a text file with key statistics for quick reference"""
    try:
        with open('graphs/summary_statistics.txt', 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("ASSIGNMENT 2: SUMMARY STATISTICS FOR REPORT\n")
            f.write("=" * 70 + "\n\n")

            # Q1
            q1 = pd.read_csv('q1_molecular_dynamics_data.csv')
            f.write("Q1: MOLECULAR DYNAMICS\n")
            f.write("-" * 70 + "\n")
            f.write(f"Best Speedup: {q1['Speedup'].max():.2f}x at {q1.loc[q1['Speedup'].idxmax(), 'Threads']} threads\n")
            f.write(f"Efficiency at 8 threads: {q1[q1['Threads']==8]['Efficiency(%)'].values[0]:.1f}%\n")
            f.write(f"Serial time: {q1[q1['Threads']==1]['Time(s)'].values[0]:.6f}s\n")
            f.write(f"Parallel time (8 threads): {q1[q1['Threads']==8]['Time(s)'].values[0]:.6f}s\n\n")

            # Q2
            q2 = pd.read_csv('q2_dna_alignment_data.csv')
            wave = q2[q2['Method'] == 'Wavefront']
            row = q2[q2['Method'] == 'Row-wise']
            f.write("Q2: DNA SEQUENCE ALIGNMENT\n")
            f.write("-" * 70 + "\n")
            f.write("Wavefront Method:\n")
            f.write(f"  Best Speedup: {wave['Speedup'].max():.2f}x at {wave.loc[wave['Speedup'].idxmax(), 'Threads']} threads\n")
            f.write(f"  Speedup at 8 threads: {wave[wave['Threads']==8]['Speedup'].values[0]:.2f}x\n")
            f.write("Row-wise Method:\n")
            f.write(f"  Best Speedup: {row['Speedup'].max():.2f}x at {row.loc[row['Speedup'].idxmax(), 'Threads']} threads\n")
            f.write(f"  Speedup at 8 threads: {row[row['Threads']==8]['Speedup'].values[0]:.2f}x\n\n")

            # Q3
            q3 = pd.read_csv('q3_heat_diffusion_data.csv')
            f.write("Q3: HEAT DIFFUSION SIMULATION\n")
            f.write("-" * 70 + "\n")
            for schedule in ['Static', 'Dynamic', 'Guided', 'Cache-Blocked']:
                data = q3[q3['Schedule'] == schedule]
                if not data.empty:
                    f.write(f"{schedule} Scheduling:\n")
                    speedup_8 = data[data['Threads']==8]['Speedup'].values[0]
                    eff_8 = data[data['Threads']==8]['Efficiency(%)'].values[0]
                    f.write(f"  Speedup at 8 threads: {speedup_8:.2f}x\n")
                    f.write(f"  Efficiency at 8 threads: {eff_8:.1f}%\n")

            f.write("\n" + "=" * 70 + "\n")
            f.write("KEY OBSERVATIONS:\n")
            f.write("=" * 70 + "\n")
            f.write("1. Q1 shows good scaling but limited by atomic operations\n")
            f.write("2. Q2 wavefront has poor scaling due to data dependencies\n")
            f.write("3. Q3 guided scheduling achieves best performance\n")
            f.write("4. All programs are cache-bound, not DRAM-bound\n")

        print("✓ Generated summary statistics: graphs/summary_statistics.txt")

    except Exception as e:
        print(f"⚠ Could not generate summary statistics: {e}")

def main():
    print("\n" + "=" * 70)
    print("ASSIGNMENT 2: AUTOMATIC GRAPH GENERATION")
    print("=" * 70 + "\n")

    create_output_directory()

    print("\nGenerating graphs...\n")
    plot_q1_molecular_dynamics()
    plot_q2_dna_alignment()
    plot_q3_heat_diffusion()
    plot_efficiency_comparison()

    print("\nGenerating summary statistics...\n")
    generate_summary_stats()

    print("\n" + "=" * 70)
    print("GENERATION COMPLETE")
    print("=" * 70)
    print("\nGenerated files in 'graphs/' directory:")
    print("  • q1_speedup.png (and .pdf)")
    print("  • q2_speedup.png (and .pdf)")
    print("  • q3_speedup.png (and .pdf)")
    print("  • efficiency_comparison.png (and .pdf) [BONUS]")
    print("  • summary_statistics.txt")
    print("\nYou can now insert these graphs directly into your report!")
    print("PNG files for Word documents, PDF files for LaTeX documents.\n")

if __name__ == "__main__":
    main()
