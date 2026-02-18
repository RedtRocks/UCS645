# Setup Guide for Ubuntu VirtualBox

## Files Included
- **Source Code**: `main.cpp`, `correlate.cpp`, `correlate.h`
- **Build System**: `Makefile` (uses g++)
- **Compilation Scripts**: `compile_and_test.sh`
- **Test Scripts**: `run_comprehensive_tests.sh`
- **Documentation**: `README.md`, `QUICKSTART.md`, `IMPLEMENTATION_SUMMARY.md`, `Assignment_3.pdf`

## Prerequisites on Ubuntu

Install required packages:
```bash
sudo apt-get update
sudo apt-get install build-essential

# Optional: Install performance analysis tools
sudo apt-get install linux-tools-generic
```

## Compilation

### Option 1: Using Make (Recommended)
```bash
make clean
make
```

### Option 2: Using Shell Script
```bash
bash compile_and_test.sh
```

### Option 3: Manual Compilation
```bash
g++ -std=c++11 -Wall -Wextra -O3 -march=native -mtune=native -fopenmp -mavx -mavx2 -mfma -c main.cpp -o main.o
g++ -std=c++11 -Wall -Wextra -O3 -march=native -mtune=native -fopenmp -mavx -mavx2 -mfma -c correlate.cpp -o correlate.o
g++ -std=c++11 -Wall -Wextra -O3 -march=native -mtune=native -fopenmp -mavx -mavx2 -mfma -o correlate main.o correlate.o
```

## Running the Program

### Basic Usage
```bash
./correlate <ny> <nx> [num_threads] [version]
```

### Examples
```bash
# Run all versions with default threads on 100x1000 matrix
./correlate 100 1000

# Use 4 threads
./correlate 500 5000 4

# Run only sequential version
./correlate 100 1000 1 1

# Run only OpenMP version with 8 threads
./correlate 500 5000 8 2

# Run only optimized version with 4 threads
./correlate 1000 10000 4 3
```

## Testing

### Quick Tests
```bash
make test-small
make test-medium
make test-large
```

### Comprehensive Testing
```bash
bash run_comprehensive_tests.sh
```

Results will be saved to `performance_results.txt`

## Cleaning

Remove compiled binaries and object files:
```bash
make clean
```

## Notes for Ubuntu/Linux

- The code is fully compatible with Linux/Ubuntu
- All headers are standard C++11 (portable)
- OpenMP is available via `-fopenmp` flag
- AVX intrinsics work with modern GCC on x86_64 processors
- The Makefile works natively on Linux without modifications
- All shell scripts (`.sh`) are compatible with Ubuntu's bash shell
- Windows-specific files (`.exe`, `.bat`) have been removed

## Performance Tips for VirtualBox

1. **Allocate sufficient CPU cores**: In VirtualBox settings, increase the number of CPUs to utilize multi-threading
2. **Allocate sufficient RAM**: Recommend at least 4GB for large matrix tests
3. **Disable pause on virtualization**: May improve performance slightly

## Troubleshooting

If compilation fails with "AVX not supported":
- GCC might not have AVX support enabled for your target CPU
- Edit the Makefile and remove `-mavx -mavx2 -mfma` flags
- Or use a generic target: `-march=x86-64` instead of `-march=native`

