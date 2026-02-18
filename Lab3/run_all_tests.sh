#!/bin/bash
# ============================================================================
# AUTOMATED PERFORMANCE TESTING PIPELINE
# One-command execution of: compile, test, analyze, export
# ============================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo ""
    echo -e "${BLUE}=========================================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}=========================================================================${NC}"
    echo ""
}

print_step() {
    echo -e "${GREEN}[*]${NC} $1"
}

print_error() {
    echo -e "${RED}[!]${NC} $1"
}

print_info() {
    echo -e "${YELLOW}[i]${NC} $1"
}

print_header "PERFORMANCE TESTING AUTOMATION PIPELINE"

# Check if we're in the right directory
if [ ! -f "main.cpp" ] || [ ! -f "correlate.cpp" ] || [ ! -f "Makefile" ]; then
    print_error "This script must be run in the Lab3 directory"
    exit 1
fi

print_info "Working directory: $(pwd)"
print_info "System: $(uname -a | cut -d' ' -f1-3)"
print_info "Cores available: $(nproc)"
print_info "Memory: $(free -h | grep Mem | awk '{print $2}')"

# ========== PHASE 1: COMPILATION ==========
print_header "PHASE 1: COMPILATION"

print_step "Checking compiler..."
g++ --version | head -1

print_step "Cleaning previous builds..."
make clean > /dev/null 2>&1

print_step "Compiling..."
if make > /dev/null 2>&1; then
    print_step "✓ Compilation successful"
else
    print_error "Compilation failed"
    make
    exit 1
fi

# ========== PHASE 2: QUICK VERIFICATION ==========
print_header "PHASE 2: QUICK VERIFICATION"

print_step "Running quick test (50x500)..."
./correlate 50 500 1 1 > /dev/null

if [ $? -eq 0 ]; then
    print_step "✓ Verification test passed"
else
    print_error "Verification test failed"
    exit 1
fi

# ========== PHASE 3: DATA COLLECTION ==========
print_header "PHASE 3: PERFORMANCE DATA COLLECTION"

print_info "This phase will run approximately 10-30 minutes depending on your system"
print_step "Starting performance tests..."

chmod +x collect_performance_data.sh
./collect_performance_data.sh

if [ -f "performance_data/performance_summary.txt" ]; then
    print_step "✓ Data collection completed"
    lines=$(wc -l < performance_data/performance_summary.txt)
    print_info "Generated $lines lines of performance data"
else
    print_error "Data collection failed"
    exit 1
fi

# ========== PHASE 4: QUICK SUMMARY ==========
print_header "PHASE 4: QUICK SUMMARY GENERATION"

print_step "Generating quick summary report..."
chmod +x generate_quick_summary.sh
./generate_quick_summary.sh > /dev/null

if [ -f "performance_data/QUICK_SUMMARY.txt" ]; then
    print_step "✓ Quick summary generated"
    cat performance_data/QUICK_SUMMARY.txt
else
    print_error "Summary generation failed"
fi

# ========== PHASE 5: ANALYSIS ==========
print_header "PHASE 5: ANALYSIS & REPORT GENERATION"

# Check if Python and required packages are available
if command -v python3 &> /dev/null; then
    print_step "Running performance analysis with Python..."
    
    if python3 analyze_performance.py; then
        print_step "✓ Analysis completed"
    else
        print_error "Analysis failed (Python dependencies may be missing)"
        print_info "Trying manual analysis instead..."
    fi
else
    print_info "Python3 not found, skipping graphing"
fi

# ========== PHASE 6: CSV EXPORT ==========
print_header "PHASE 6: DATA EXPORT"

if command -v python3 &> /dev/null; then
    print_step "Exporting to CSV format..."
    python3 export_to_csv.py
fi

# ========== PHASE 7: SUMMARY ==========
print_header "FINAL SUMMARY"

print_info "Performance testing pipeline complete!"
echo ""
echo "Generated Files:"
echo "  Performance Data:"
echo "    - performance_data/performance_summary.txt (detailed results)"
echo "    - performance_data/detailed_execution.log (complete log)"
echo "    - performance_data/QUICK_SUMMARY.txt (quick reference)"
echo ""
echo "  Analysis:"
echo "    - performance_data/analysis_report.txt (text report)"
echo "    - performance_data/performance_graphs.png (graphs, if matplotlib available)"
echo ""
echo "  Export:"
echo "    - performance_data/performance_data.csv (detailed data)"
echo "    - performance_data/performance_summary.csv (summary data)"
echo ""
echo "Next Steps:"
echo "  1. Review the quick summary:"
echo "     cat performance_data/QUICK_SUMMARY.txt"
echo ""
echo "  2. View the detailed analysis report:"
echo "     cat performance_data/analysis_report.txt"
echo ""
echo "  3. Download CSV files to Windows for Excel analysis:"
echo "     cp performance_data/*.csv /path/to/shared/folder/"
echo ""
echo "  4. View performance graphs:"
echo "     eog performance_data/performance_graphs.png"
echo ""
echo "  5. Create your performance report using these results"
echo ""

print_header "SUCCESS"
print_step "All tests completed successfully!"

