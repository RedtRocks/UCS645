#!/bin/bash
# ============================================================================
# Compilation and Testing Script for Windows/Non-Make Environments
# ============================================================================

echo "========================================="
echo "Assignment 3: Vector Correlation"
echo "Compilation and Testing Script"
echo "========================================="
echo ""

# Clean old build files
echo "Cleaning old build files..."
rm -f *.o correlate
echo "Done."
echo ""

# Compile
echo "Compiling source files..."
echo "  - Compiling main.cpp..."
g++ -std=c++11 -Wall -O3 -march=native -fopenmp -mavx -c main.cpp -o main.o

if [ $? -ne 0 ]; then
    echo "Error compiling main.cpp"
    exit 1
fi

echo "  - Compiling correlate.cpp..."
g++ -std=c++11 -Wall -O3 -march=native -fopenmp -mavx -c correlate.cpp -o correlate.o

if [ $? -ne 0 ]; then
    echo "Error compiling correlate.cpp"
    exit 1
fi

echo "  - Linking..."
g++ -std=c++11 -O3 -fopenmp main.o correlate.o -o correlate

if [ $? -ne 0 ]; then
    echo "Error linking"
    exit 1
fi

echo "Compilation successful!"
echo ""

# Run tests
echo "========================================="
echo "Running Tests"
echo "========================================="
echo ""

echo "--- Test 1: Small matrix (100x1000) ---"
./correlate 100 1000
echo ""

echo "--- Test 2: Medium matrix (200x2000) ---"
./correlate 200 2000
echo ""

echo "========================================="
echo "Testing Complete!"
echo "========================================="
echo ""
echo "To run manually:"
echo "  ./correlate <ny> <nx> [threads] [version]"
echo ""
echo "Examples:"
echo "  ./correlate 100 1000          # Run all versions"
echo "  ./correlate 500 5000 4        # Use 4 threads"
echo "  ./correlate 1000 10000 8 3    # Run optimized version only with 8 threads"
