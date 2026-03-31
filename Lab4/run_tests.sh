#!/bin/bash

# Lab4 MPI Comprehensive Testing Script
# Runs all 4 programs across multiple processor counts and captures timing

set -e

OUTPUT_FILE="timing_results.csv"
PROGRAMS=("q1_ring_comm" "q2_array_sum" "q3_max_min" "q4_dot_product")
PROC_COUNTS=(1 2 4 8)
TIMEOUT_SECONDS=30

echo "====================================="
echo "Lab4 MPI Performance Testing"
echo "====================================="
echo

# Check if programs are built
for prog in "${PROGRAMS[@]}"; do
    if [ ! -f "./$prog" ]; then
        echo "Error: $prog not found. Please run 'make' first."
        exit 1
    fi
done

echo "Building CSV header..."
echo "Program,Processes,Time_Seconds,Speedup,Efficiency" > "$OUTPUT_FILE"

run_mpi_timed() {
    local np=$1
    local prog=$2
    timeout "$TIMEOUT_SECONDS" mpirun -np "$np" "./$prog" > /dev/null 2>&1
}

# Baseline times for speedup calculation (single process)
declare -A baseline_times

echo
echo "Running baseline tests (1 process)..."
for prog in "${PROGRAMS[@]}"; do
    echo -n "  $prog ... "
    start_time=$(date +%s.%N)
    if ! run_mpi_timed 1 "$prog"; then
        echo "failed (timeout or runtime error)"
        exit 1
    fi
    end_time=$(date +%s.%N)
    exec_time=$(echo "$end_time - $start_time" | bc)
    baseline_times[$prog]=$exec_time
    echo "done (${exec_time}s)"
    echo "$prog,1,$exec_time,1.0,100.0" >> "$OUTPUT_FILE"
done

echo
echo "Running multi-process scaling tests..."
for prog in "${PROGRAMS[@]}"; do
    echo "  Testing $prog..."
    baseline=${baseline_times[$prog]}
    
    for np in "${PROC_COUNTS[@]}"; do
        if [ $np -eq 1 ]; then
            continue  # Skip single process (already done)
        fi
        
        echo -n "    np=$np ... "
        start_time=$(date +%s.%N)
        if ! run_mpi_timed "$np" "$prog"; then
            echo "failed (timeout or runtime error)"
            exit 1
        fi
        end_time=$(date +%s.%N)
        exec_time=$(echo "$end_time - $start_time" | bc)
        speedup=$(awk -v t1="$baseline" -v tp="$exec_time" 'BEGIN { printf "%.6f", t1 / tp }')
        efficiency=$(awk -v t1="$baseline" -v tp="$exec_time" -v p="$np" 'BEGIN { printf "%.3f", (t1 / (p * tp)) * 100 }')
        
        echo "done (${exec_time}s, speedup ${speedup}x)"
        echo "$prog,$np,$exec_time,$speedup,$efficiency" >> "$OUTPUT_FILE"
    done
    echo
done

echo "====================================="
echo "Results saved to: $OUTPUT_FILE"
echo "====================================="
echo
echo "Sample output:"
head -6 "$OUTPUT_FILE" | column -t -s, 

echo
echo "Next: Run 'python3 analyze_results.py' to generate graphs and tables"
