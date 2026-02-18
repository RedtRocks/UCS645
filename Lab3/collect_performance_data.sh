#!/bin/bash
# ============================================================================
# PERFORMANCE DATA COLLECTION SCRIPT FOR UBUNTU
# Gathers detailed metrics during execution for comprehensive analysis
# ============================================================================

set -e

OUTPUT_DIR="performance_data"
mkdir -p $OUTPUT_DIR

SUMMARY_FILE="$OUTPUT_DIR/performance_summary.txt"
CSV_FILE="$OUTPUT_DIR/performance_metrics.csv"
DETAILED_LOG="$OUTPUT_DIR/detailed_execution.log"

# Initialize CSV with headers
echo "Test,Configuration,Threads,MatrixSize,SequentialTime,OpenMPTime,OptimizedTime,OpenMPSpeedup,OptimizedSpeedup,Efficiency_OMP,Efficiency_Opt" > $CSV_FILE

# Get system information
echo "=========================================================================" | tee $SUMMARY_FILE
echo "PERFORMANCE ANALYSIS - SYSTEM INFORMATION" | tee -a $SUMMARY_FILE
echo "=========================================================================" | tee -a $SUMMARY_FILE
echo "Date: $(date)" | tee -a $SUMMARY_FILE
echo "System: $(uname -a)" | tee -a $SUMMARY_FILE
echo "Hostname: $(hostname)" | tee -a $SUMMARY_FILE
echo "CPU: $(lscpu | grep 'Model name' | cut -d: -f2 | xargs)" | tee -a $SUMMARY_FILE
echo "Cores: $(nproc)" | tee -a $SUMMARY_FILE
echo "Memory: $(free -h | grep Mem | awk '{print $2}')" | tee -a $SUMMARY_FILE
echo "=========================================================================" | tee -a $SUMMARY_FILE
echo "" | tee -a $SUMMARY_FILE

# Compile if needed
if [ ! -f correlate ]; then
    echo "Compiling program..." | tee -a $SUMMARY_FILE
    g++ -std=c++11 -Wall -Wextra -O3 -march=native -mtune=native -fopenmp -mavx -mavx2 -mfma -c main.cpp -o main.o
    g++ -std=c++11 -Wall -Wextra -O3 -march=native -mtune=native -fopenmp -mavx -mavx2 -mfma -c correlate.cpp -o correlate.o
    g++ -std=c++11 -Wall -Wextra -O3 -march=native -mtune=native -fopenmp -mavx -mavx2 -mfma -o correlate main.o correlate.o
    echo "Compilation complete." | tee -a $SUMMARY_FILE
    echo "" | tee -a $SUMMARY_FILE
fi

# === TEST SUITE ===
run_test() {
    local test_name=$1
    local ny=$2
    local nx=$3
    local threads=$4
    local version=$5
    
    echo "=========================================================================" | tee -a $SUMMARY_FILE
    echo "TEST: $test_name" | tee -a $SUMMARY_FILE
    echo "Matrix: ${ny}x${nx}, Threads: $threads, Version: $version" | tee -a $SUMMARY_FILE
    echo "=========================================================================" | tee -a $SUMMARY_FILE
    
    # Run the test and capture output
    ./correlate $ny $nx $threads $version 2>&1 | tee -a $DETAILED_LOG | tee -a $SUMMARY_FILE
    
    echo "" | tee -a $SUMMARY_FILE
}

# ===== TEST MATRIX 1: VARYING MATRIX SIZES =====
echo "=========================================================================" | tee -a $SUMMARY_FILE
echo "PHASE 1: MATRIX SIZE SCALING (4 threads, all versions)" | tee -a $SUMMARY_FILE
echo "=========================================================================" | tee -a $SUMMARY_FILE
echo "" | tee -a $SUMMARY_FILE

declare -a sizes=("50 500" "100 1000" "200 2000" "300 3000" "500 5000")

for size in "${sizes[@]}"; do
    read -r ny nx <<< "$size"
    run_test "Matrix Size ${ny}x${nx}" $ny $nx 4 "all"
done

# ===== TEST MATRIX 2: VARYING THREAD COUNTS =====
echo "=========================================================================" | tee -a $SUMMARY_FILE
echo "PHASE 2: THREAD SCALING (500x5000 matrix, all versions)" | tee -a $SUMMARY_FILE
echo "=========================================================================" | tee -a $SUMMARY_FILE
echo "" | tee -a $SUMMARY_FILE

declare -a threads_array=(1 2 4 8)

for t in "${threads_array[@]}"; do
    run_test "Thread Count $t" 500 5000 $t "all"
done

# ===== TEST MATRIX 3: VERSION COMPARISON =====
echo "=========================================================================" | tee -a $SUMMARY_FILE
echo "PHASE 3: VERSION COMPARISON (200x2000, 8 threads)" | tee -a $SUMMARY_FILE
echo "=========================================================================" | tee -a $SUMMARY_FILE
echo "" | tee -a $SUMMARY_FILE

declare -a versions=(1 2 3)
for v in "${versions[@]}"; do
    run_test "Version $v Only" 200 2000 8 "$v"
done

# ===== TEST MATRIX 4: LARGE MATRIX =====
echo "=========================================================================" | tee -a $SUMMARY_FILE
echo "PHASE 4: LARGE MATRIX STRESS TEST (1000x10000, 8 threads)" | tee -a $SUMMARY_FILE
echo "=========================================================================" | tee -a $SUMMARY_FILE
echo "" | tee -a $SUMMARY_FILE

run_test "Large Matrix" 1000 10000 8 "all"

echo "" | tee -a $SUMMARY_FILE
echo "=========================================================================" | tee -a $SUMMARY_FILE
echo "TESTING COMPLETE" | tee -a $SUMMARY_FILE
echo "=========================================================================" | tee -a $SUMMARY_FILE
echo "" | tee -a $SUMMARY_FILE
echo "Output Files:" | tee -a $SUMMARY_FILE
echo "  - $SUMMARY_FILE" | tee -a $SUMMARY_FILE
echo "  - $DETAILED_LOG" | tee -a $SUMMARY_FILE
echo "" | tee -a $SUMMARY_FILE

