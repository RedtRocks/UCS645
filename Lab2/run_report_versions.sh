#!/bin/bash

# Assignment 2 - Report Version Compilation and Execution Script
# This script compiles and runs the enhanced versions that generate report-ready output

echo "========================================================================"
echo "Assignment 2: OpenMP Performance Evaluation - Report Generation"
echo "========================================================================"
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Create output directory
mkdir -p output
mkdir -p graphs

echo -e "${YELLOW}Compiling Report Versions...${NC}\n"

# Compile Q1
echo -e "${BLUE}Compiling Q1: Molecular Dynamics (Report Version)...${NC}"
g++ -O3 -fopenmp -std=c++17 q1_molecular_dynamics_report.cpp -o q1_report 2>output/q1_compile.log
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Q1 compiled successfully${NC}"
else
    echo -e "${RED}✗ Q1 compilation failed${NC}"
    cat output/q1_compile.log
    exit 1
fi

# Compile Q2
echo -e "${BLUE}Compiling Q2: DNA Sequence Alignment (Report Version)...${NC}"
g++ -O3 -fopenmp -std=c++17 q2_dna_alignment_report.cpp -o q2_report 2>output/q2_compile.log
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Q2 compiled successfully${NC}"
else
    echo -e "${RED}✗ Q2 compilation failed${NC}"
    cat output/q2_compile.log
    exit 1
fi

# Compile Q3
echo -e "${BLUE}Compiling Q3: Heat Diffusion (Report Version)...${NC}"
g++ -O3 -fopenmp -std=c++17 q3_heat_diffusion_report.cpp -o q3_report 2>output/q3_compile.log
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Q3 compiled successfully${NC}"
else
    echo -e "${RED}✗ Q3 compilation failed${NC}"
    cat output/q3_compile.log
    exit 1
fi

echo ""
echo -e "${GREEN}All programs compiled successfully!${NC}"
echo ""

# Run programs
echo "========================================================================"
echo "RUNNING EXPERIMENTS"
echo "========================================================================"
echo ""

# Q1
echo -e "${YELLOW}Running Q1: Molecular Dynamics...${NC}"
echo "This may take a few minutes..."
./q1_report | tee output/q1_report_output.txt
echo ""

# Q2
echo -e "${YELLOW}Running Q2: DNA Sequence Alignment...${NC}"
./q2_report | tee output/q2_report_output.txt
echo ""

# Q3
echo -e "${YELLOW}Running Q3: Heat Diffusion Simulation...${NC}"
echo "Testing all scheduling strategies..."
./q3_report | tee output/q3_report_output.txt
echo ""

# Summary
echo "========================================================================"
echo "EXECUTION COMPLETE"
echo "========================================================================"
echo ""
echo "Output files created in 'output/' directory:"
echo "  - output/q1_report_output.txt (with perf stats and VTune metrics)"
echo "  - output/q2_report_output.txt (both parallelization methods)"
echo "  - output/q3_report_output.txt (all scheduling strategies)"
echo ""
echo "CSV files for graphing (copy these to your graphing tool):"
echo "  - q1_molecular_dynamics_data.csv"
echo "  - q2_dna_alignment_data.csv"
echo "  - q3_heat_diffusion_data.csv"
echo ""
echo -e "${GREEN}All data ready for report creation!${NC}"
echo ""
echo "Next steps for your report:"
echo "  1. Copy the execution tables from output/*.txt files"
echo "  2. Use CSV files to create graphs (Excel, Python, MATLAB, etc.)"
echo "  3. Copy perf stats sections for your report"
echo "  4. Copy VTune metrics tables"
echo "  5. Write your analysis based on the provided summaries"
echo ""
echo "See REPORT_TEMPLATE.md for detailed instructions on creating your report"
echo ""
