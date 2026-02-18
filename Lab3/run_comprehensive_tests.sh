#!/bin/bash
# ============================================================================
# Comprehensive Performance Testing Script
# Generates data for report writing
# ============================================================================

OUTPUT_FILE="performance_results.txt"

echo "=========================================================================" | tee $OUTPUT_FILE
echo "ASSIGNMENT 3: COMPREHENSIVE PERFORMANCE TESTING" | tee -a $OUTPUT_FILE
echo "Date: $(date)" | tee -a $OUTPUT_FILE
echo "System: $(uname -a 2>/dev/null || echo 'Windows')" | tee -a $OUTPUT_FILE
echo "CPU Cores: $(nproc 2>/dev/null || echo 'Unknown')" | tee -a $OUTPUT_FILE
echo "=========================================================================" | tee -a $OUTPUT_FILE
echo "" | tee -a $OUTPUT_FILE

# Ensure program is compiled
if [ ! -f correlate ]; then
    echo "Compiling program..." | tee -a $OUTPUT_FILE
    g++ -std=c++11 -O3 -fopenmp -mavx -c main.cpp correlate.cpp
    g++ -o correlate main.o correlate.o -fopenmp
    echo "Compilation complete." | tee -a $OUTPUT_FILE
    echo "" | tee -a $OUTPUT_FILE
fi

# Test 1: Varying Matrix Sizes (4 threads)
echo "=========================================================================" | tee -a $OUTPUT_FILE
echo "TEST 1: VARYING MATRIX SIZES (4 threads)" | tee -a $OUTPUT_FILE
echo "=========================================================================" | tee -a $OUTPUT_FILE
echo "" | tee -a $OUTPUT_FILE

for size in "100 1000" "200 2000" "300 3000" "500 5000"; do
    set -- $size
    ny=$1
    nx=$2
    echo "--- Testing ${ny}x${nx} matrix ---" | tee -a $OUTPUT_FILE
    ./correlate $ny $nx 4 all | tee -a $OUTPUT_FILE
    echo "" | tee -a $OUTPUT_FILE
done

# Test 2: Varying Thread Counts (500x5000 matrix)
echo "=========================================================================" | tee -a $OUTPUT_FILE
echo "TEST 2: VARYING THREAD COUNTS (500x5000 matrix)" | tee -a $OUTPUT_FILE
echo "=========================================================================" | tee -a $OUTPUT_FILE
echo "" | tee -a $OUTPUT_FILE

for threads in 1 2 4 8; do
    echo "--- Testing with $threads thread(s) ---" | tee -a $OUTPUT_FILE
    ./correlate 500 5000 $threads all | tee -a $OUTPUT_FILE
    echo "" | tee -a $OUTPUT_FILE
done

# Test 3: OpenMP vs Optimized Comparison
echo "=========================================================================" | tee -a $OUTPUT_FILE
echo "TEST 3: COMPARISON - OPENMP VS OPTIMIZED" | tee -a $OUTPUT_FILE
echo "=========================================================================" | tee -a $OUTPUT_FILE
echo "" | tee -a $OUTPUT_FILE

echo "Matrix: 500x5000, Threads: 8" | tee -a $OUTPUT_FILE
echo "" | tee -a $OUTPUT_FILE

echo "--- OpenMP Version ---" | tee -a $OUTPUT_FILE
./correlate 500 5000 8 2 | tee -a $OUTPUT_FILE
echo "" | tee -a $OUTPUT_FILE

echo "--- Optimized Version ---" | tee -a $OUTPUT_FILE
./correlate 500 5000 8 3 | tee -a $OUTPUT_FILE
echo "" | tee -a $OUTPUT_FILE

# Test 4: Large Matrix Performance
echo "=========================================================================" | tee -a $OUTPUT_FILE
echo "TEST 4: LARGE MATRIX PERFORMANCE" | tee -a $OUTPUT_FILE
echo "=========================================================================" | tee -a $OUTPUT_FILE
echo "" | tee -a $OUTPUT_FILE

echo "Testing 1000x10000 matrix with 8 threads" | tee -a $OUTPUT_FILE
./correlate 1000 10000 8 all | tee -a $OUTPUT_FILE
echo "" | tee -a $OUTPUT_FILE

# Summary
echo "=========================================================================" | tee -a $OUTPUT_FILE
echo "TESTING COMPLETE" | tee -a $OUTPUT_FILE
echo "=========================================================================" | tee -a $OUTPUT_FILE
echo "" | tee -a $OUTPUT_FILE
echo "Results have been saved to: $OUTPUT_FILE" | tee -a $OUTPUT_FILE
echo "" | tee -a $OUTPUT_FILE
echo "You can now use these results to:" | tee -a $OUTPUT_FILE
echo "1. Create performance graphs" | tee -a $OUTPUT_FILE
echo "2. Analyze speedup and efficiency" | tee -a $OUTPUT_FILE
echo "3. Write your report" | tee -a $OUTPUT_FILE
echo "" | tee -a $OUTPUT_FILE

# Create CSV file for easy graphing
CSV_FILE="performance_data.csv"
echo "Configuration,Threads,SequentialTime,OpenMPTime,OptimizedTime,OpenMPSpeedup,OptimizedSpeedup" > $CSV_FILE

# Parse results and create CSV (simplified version)
echo "Note: You can manually extract data from $OUTPUT_FILE to create graphs" | tee -a $OUTPUT_FILE

echo "" | tee -a $OUTPUT_FILE
echo "=========================================================================" | tee -a $OUTPUT_FILE
