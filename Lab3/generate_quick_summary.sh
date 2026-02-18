#!/bin/bash
# ============================================================================
# QUICK SUMMARY REPORT GENERATOR
# Extracts key metrics and creates an easily readable summary
# ============================================================================

DATA_DIR="performance_data"

if [ ! -d "$DATA_DIR" ]; then
    echo "Error: $DATA_DIR directory not found"
    echo "Run collect_performance_data.sh first"
    exit 1
fi

SUMMARY_FILE="$DATA_DIR/QUICK_SUMMARY.txt"

echo "Generating quick summary report..."

{
    echo "========================================================================="
    echo "PERFORMANCE TEST SUMMARY"
    echo "========================================================================="
    echo ""
    
    echo "TEST EXECUTION DETAILS"
    echo "---------"
    grep -E "Date:|System:|CPU:|Cores:|Memory:" "$DATA_DIR/performance_summary.txt" | head -5
    echo ""
    
    echo "EXECUTION TIME STATISTICS"
    echo "---------"
    echo ""
    echo "Sequential Version Times:"
    grep -A1 "VERSION 1: SEQUENTIAL" "$DATA_DIR/performance_summary.txt" | grep "Execution time" | head -5
    echo ""
    
    echo "OpenMP Version Times (with speedup):"
    grep -B1 "Speedup:" "$DATA_DIR/performance_summary.txt" | grep -E "Execution time|Speedup" | head -10
    echo ""
    
    echo "Optimized Version Times (with speedup):"
    grep "Optimized Version" -A 20 "$DATA_DIR/performance_summary.txt" | grep -E "Execution time|Speedup" | head -10
    echo ""
    
    echo "EFFICIENCY METRICS"
    echo "---------"
    echo ""
    grep "Efficiency:" "$DATA_DIR/performance_summary.txt" | sort -u
    echo ""
    
    echo "THROUGHPUT (Correlations/Second)"
    echo "---------"
    echo ""
    grep "Throughput:" "$DATA_DIR/performance_summary.txt" | head -10
    echo ""
    
    echo "VERIFICATION STATUS"
    echo "---------"
    echo ""
    passed=$(grep -c "Verifying correctness... PASSED" "$DATA_DIR/performance_summary.txt")
    failed=$(grep -c "Verifying correctness... FAILED" "$DATA_DIR/performance_summary.txt")
    echo "Tests Passed: $passed"
    echo "Tests Failed: $failed"
    echo ""
    
    echo "KEY FINDINGS"
    echo "---------"
    echo ""
    
    # Extract best performers
    echo "Best Sequential Time:"
    grep "VERSION 1:" -A 3 "$DATA_DIR/performance_summary.txt" | grep "Execution time" | sort -k3 -n | head -1
    
    echo ""
    echo "Best OpenMP Speedup:"
    grep "Speedup:" "$DATA_DIR/performance_summary.txt" | grep -v "====" | sort -t: -k2 -rn | head -3
    
    echo ""
    echo "========================================================================="
    
} > "$SUMMARY_FILE"

cat "$SUMMARY_FILE"
echo ""
echo "Summary saved to: $SUMMARY_FILE"
