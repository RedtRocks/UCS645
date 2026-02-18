# ============================================================================
# Makefile for Vector Correlation Assignment
# ============================================================================

# Compiler
CXX = g++

# Compiler flags
CXXFLAGS = -std=c++11 -Wall -Wextra
OPTFLAGS = -O3 -march=native -mtune=native
OMPFLAGS = -fopenmp
SIMDFLAGS = -mavx -mavx2 -mfma

# Combine flags
CXXFLAGS += $(OPTFLAGS) $(OMPFLAGS) $(SIMDFLAGS)

# Target executable
TARGET = correlate

# Source files
SOURCES = main.cpp correlate.cpp

# Object files
OBJECTS = $(SOURCES:.cpp=.o)

# Header files
HEADERS = correlate.h

# ============================================================================
# Default target - builds the optimized executable
# ============================================================================
all: $(TARGET)
	@echo ""
	@echo "========================================="
	@echo "Build complete!"
	@echo "Run with: ./$(TARGET) <ny> <nx> [threads]"
	@echo "Example: ./$(TARGET) 100 1000 4"
	@echo "========================================="

# ============================================================================
# Link object files to create executable
# ============================================================================
$(TARGET): $(OBJECTS)
	@echo "Linking $@..."
	$(CXX) $(CXXFLAGS) -o $@ $(OBJECTS)

# ============================================================================
# Compile source files to object files
# ============================================================================
%.o: %.cpp $(HEADERS)
	@echo "Compiling $<..."
	$(CXX) $(CXXFLAGS) -c $< -o $@

# ============================================================================
# Clean build files
# ============================================================================
clean:
	@echo "Cleaning build files..."
	rm -f $(OBJECTS) $(TARGET)
	@echo "Clean complete."

# ============================================================================
# Run the program with default parameters
# ============================================================================
run: $(TARGET)
	@echo "Running with default parameters (100x1000)..."
	./$(TARGET) 100 1000

# ============================================================================
# Run performance tests with various sizes
# ============================================================================
test-small: $(TARGET)
	@echo "========================================="
	@echo "Test: Small matrix (100x1000)"
	@echo "========================================="
	./$(TARGET) 100 1000

test-medium: $(TARGET)
	@echo "========================================="
	@echo "Test: Medium matrix (500x5000)"
	@echo "========================================="
	./$(TARGET) 500 5000

test-large: $(TARGET)
	@echo "========================================="
	@echo "Test: Large matrix (1000x10000)"
	@echo "========================================="
	./$(TARGET) 1000 10000

# ============================================================================
# Run all tests
# ============================================================================
test-all: test-small test-medium test-large

# ============================================================================
# Perf stats for sequential version
# ============================================================================
perf-sequential: $(TARGET)
	@echo "========================================="
	@echo "Running perf stats on SEQUENTIAL version"
	@echo "Matrix: 500x5000"
	@echo "========================================="
	perf stat -e cycles,instructions,cache-references,cache-misses,branches,branch-misses \
		./$(TARGET) 500 5000 1 1

# ============================================================================
# Perf stats for OpenMP version with varying threads
# ============================================================================
perf-openmp-1: $(TARGET)
	@echo "========================================="
	@echo "Perf stats: OpenMP with 1 thread"
	@echo "========================================="
	perf stat -e cycles,instructions,cache-references,cache-misses \
		./$(TARGET) 500 5000 1 2

perf-openmp-2: $(TARGET)
	@echo "========================================="
	@echo "Perf stats: OpenMP with 2 threads"
	@echo "========================================="
	perf stat -e cycles,instructions,cache-references,cache-misses \
		./$(TARGET) 500 5000 2 2

perf-openmp-4: $(TARGET)
	@echo "========================================="
	@echo "Perf stats: OpenMP with 4 threads"
	@echo "========================================="
	perf stat -e cycles,instructions,cache-references,cache-misses \
		./$(TARGET) 500 5000 4 2

perf-openmp-8: $(TARGET)
	@echo "========================================="
	@echo "Perf stats: OpenMP with 8 threads"
	@echo "========================================="
	perf stat -e cycles,instructions,cache-references,cache-misses \
		./$(TARGET) 500 5000 8 2

# ============================================================================
# Perf stats for Optimized version with varying threads
# ============================================================================
perf-optimized-1: $(TARGET)
	@echo "========================================="
	@echo "Perf stats: Optimized with 1 thread"
	@echo "========================================="
	perf stat -e cycles,instructions,cache-references,cache-misses \
		./$(TARGET) 500 5000 1 3

perf-optimized-4: $(TARGET)
	@echo "========================================="
	@echo "Perf stats: Optimized with 4 threads"
	@echo "========================================="
	perf stat -e cycles,instructions,cache-references,cache-misses \
		./$(TARGET) 500 5000 4 3

perf-optimized-8: $(TARGET)
	@echo "========================================="
	@echo "Perf stats: Optimized with 8 threads"
	@echo "========================================="
	perf stat -e cycles,instructions,cache-references,cache-misses \
		./$(TARGET) 500 5000 8 3

# ============================================================================
# Run all perf tests
# ============================================================================
perf-all: perf-sequential perf-openmp-1 perf-openmp-2 perf-openmp-4 perf-openmp-8 \
          perf-optimized-1 perf-optimized-4 perf-optimized-8

# ============================================================================
# Benchmark script - tests various matrix sizes and thread counts
# ============================================================================
benchmark: $(TARGET)
	@echo "========================================="
	@echo "BENCHMARK: Testing various configurations"
	@echo "========================================="
	@echo ""
	@echo "--- Matrix 100x1000 ---"
	@./$(TARGET) 100 1000 1 all
	@echo ""
	@echo "--- Matrix 200x2000 ---"
	@./$(TARGET) 200 2000 4 all
	@echo ""
	@echo "--- Matrix 500x5000 ---"
	@./$(TARGET) 500 5000 8 all
	@echo ""
	@echo "========================================="
	@echo "Benchmark complete!"
	@echo "========================================="

# ============================================================================
# Thread scaling test - measure speedup with different thread counts
# ============================================================================
scaling-test: $(TARGET)
	@echo "========================================="
	@echo "THREAD SCALING TEST (Matrix: 500x5000)"
	@echo "========================================="
	@for threads in 1 2 4 8; do \
		echo ""; \
		echo "--- Testing with $$threads thread(s) ---"; \
		./$(TARGET) 500 5000 $$threads 2; \
	done
	@echo ""
	@echo "========================================="
	@echo "Scaling test complete!"
	@echo "========================================="

# ============================================================================
# Size scaling test - measure performance with different matrix sizes
# ============================================================================
size-scaling: $(TARGET)
	@echo "========================================="
	@echo "SIZE SCALING TEST (4 threads)"
	@echo "========================================="
	@for size in "100 1000" "200 2000" "300 3000" "500 5000"; do \
		echo ""; \
		echo "--- Testing matrix $$size ---"; \
		./$(TARGET) $$size 4 all; \
	done
	@echo ""
	@echo "========================================="
	@echo "Size scaling test complete!"
	@echo "========================================="

# ============================================================================
# Help target
# ============================================================================
help:
	@echo "========================================="
	@echo "Available Makefile targets:"
	@echo "========================================="
	@echo "  make              - Build the program"
	@echo "  make clean        - Remove build files"
	@echo "  make run          - Run with default parameters"
	@echo ""
	@echo "Testing:"
	@echo "  make test-small   - Test with 100x1000 matrix"
	@echo "  make test-medium  - Test with 500x5000 matrix"
	@echo "  make test-large   - Test with 1000x10000 matrix"
	@echo "  make test-all     - Run all tests"
	@echo ""
	@echo "Performance analysis:"
	@echo "  make perf-sequential      - Perf stats for sequential"
	@echo "  make perf-openmp-[1|2|4|8]  - Perf stats for OpenMP"
	@echo "  make perf-optimized-[1|4|8] - Perf stats for optimized"
	@echo "  make perf-all             - Run all perf tests"
	@echo ""
	@echo "Benchmarks:"
	@echo "  make benchmark    - Comprehensive benchmark"
	@echo "  make scaling-test - Thread scaling analysis"
	@echo "  make size-scaling - Matrix size scaling"
	@echo ""
	@echo "========================================="

# ============================================================================
# Phony targets (not actual files)
# ============================================================================
.PHONY: all clean run test-small test-medium test-large test-all \
        perf-sequential perf-openmp-1 perf-openmp-2 perf-openmp-4 perf-openmp-8 \
        perf-optimized-1 perf-optimized-4 perf-optimized-8 perf-all \
        benchmark scaling-test size-scaling help
