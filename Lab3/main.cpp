#include <iostream>
#include <iomanip>
#include <cstdlib>
#include <ctime>
#include <cmath>
#include <chrono>
#include <omp.h>
#include "correlate.h"

using namespace std;
using namespace std::chrono;

// Function to initialize matrix with random data
void initialize_matrix(float* data, int ny, int nx) {
    srand(42); // Fixed seed for reproducibility
    for (int y = 0; y < ny; y++) {
        for (int x = 0; x < nx; x++) {
            data[x + y * nx] = static_cast<float>(rand()) / RAND_MAX * 100.0f - 50.0f;
        }
    }
}

// Function to verify results match (within tolerance)
bool verify_results(const float* result1, const float* result2, int ny, float tolerance = 1e-4) {
    bool all_match = true;
    int mismatches = 0;

    for (int i = 0; i < ny; i++) {
        for (int j = 0; j <= i; j++) {
            float diff = fabs(result1[i + j * ny] - result2[i + j * ny]);
            if (diff > tolerance) {
                if (mismatches < 5) {  // Print first 5 mismatches
                    cout << "Mismatch at (" << i << "," << j << "): "
                         << result1[i + j * ny] << " vs " << result2[i + j * ny]
                         << " (diff: " << diff << ")" << endl;
                }
                mismatches++;
                all_match = false;
            }
        }
    }

    if (mismatches > 0) {
        cout << "Total mismatches: " << mismatches << " out of " << (ny * (ny + 1) / 2) << endl;
    }

    return all_match;
}

// Print sample results
void print_sample_results(const float* result, int ny, int sample_size = 5) {
    cout << "\nSample correlation matrix (first " << min(sample_size, ny) << "x" << min(sample_size, ny) << "):\n";
    cout << fixed << setprecision(4);

    int size = min(sample_size, ny);
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            if (j <= i) {
                cout << setw(8) << result[i + j * ny] << " ";
            } else {
                cout << setw(8) << "---" << " ";
            }
        }
        cout << endl;
    }
}

// Print usage instructions
void print_usage(const char* program_name) {
    cout << "Usage: " << program_name << " <ny> <nx> [num_threads] [version]\n\n";
    cout << "Parameters:\n";
    cout << "  ny          - Number of rows (vectors) in the matrix\n";
    cout << "  nx          - Number of columns (elements per vector)\n";
    cout << "  num_threads - Number of OpenMP threads (default: max available)\n";
    cout << "  version     - Which version to run:\n";
    cout << "                  1 = Sequential only\n";
    cout << "                  2 = OpenMP only\n";
    cout << "                  3 = Optimized only\n";
    cout << "                  all = All versions (default)\n\n";
    cout << "Examples:\n";
    cout << "  " << program_name << " 100 1000          # 100 vectors, 1000 elements each\n";
    cout << "  " << program_name << " 500 5000 4        # Use 4 threads\n";
    cout << "  " << program_name << " 1000 10000 8 3    # Run only optimized version with 8 threads\n";
}

int main(int argc, char* argv[]) {
    // Parse command-line arguments
    if (argc < 3) {
        print_usage(argv[0]);
        return 1;
    }

    int ny = atoi(argv[1]);
    int nx = atoi(argv[2]);
    int num_threads = (argc >= 4) ? atoi(argv[3]) : omp_get_max_threads();
    string version_str = (argc >= 5) ? string(argv[4]) : "all";

    if (ny <= 0 || nx <= 0) {
        cerr << "Error: ny and nx must be positive integers\n";
        return 1;
    }

    if (num_threads <= 0) {
        num_threads = omp_get_max_threads();
    }

    cout << "=========================================================================\n";
    cout << "VECTOR CORRELATION COMPUTATION\n";
    cout << "=========================================================================\n";
    cout << "Matrix dimensions: " << ny << " rows x " << nx << " columns\n";
    cout << "Total elements: " << (ny * nx) << "\n";
    cout << "Correlation pairs to compute: " << (ny * (ny + 1) / 2) << "\n";
    cout << "Available threads: " << omp_get_max_threads() << "\n";
    cout << "Using threads: " << num_threads << "\n";
    cout << "=========================================================================\n\n";

    // Allocate memory
    cout << "Allocating memory...\n";
    float* data = new float[ny * nx];
    float* result_seq = new float[ny * ny];
    float* result_omp = new float[ny * ny];
    float* result_opt = new float[ny * ny];

    // Initialize data
    cout << "Initializing matrix with random data...\n";
    initialize_matrix(data, ny, nx);

    bool run_seq = (version_str == "all" || version_str == "1");
    bool run_omp = (version_str == "all" || version_str == "2");
    bool run_opt = (version_str == "all" || version_str == "3");

    // =======================================================================
    // VERSION 1: SEQUENTIAL BASELINE
    // =======================================================================
    if (run_seq) {
        cout << "\n--- VERSION 1: SEQUENTIAL BASELINE ---\n";

        auto start = high_resolution_clock::now();
        correlate_sequential(ny, nx, data, result_seq);
        auto end = high_resolution_clock::now();

        double time_seq = duration<double>(end - start).count();

        cout << "Execution time: " << fixed << setprecision(6) << time_seq << " seconds\n";
        cout << "Throughput: " << fixed << setprecision(2)
             << (ny * (ny + 1) / 2) / time_seq << " correlations/second\n";

        print_sample_results(result_seq, ny);
    }

    // =======================================================================
    // VERSION 2: OPENMP PARALLELIZED
    // =======================================================================
    if (run_omp) {
        cout << "\n--- VERSION 2: OPENMP PARALLELIZED (" << num_threads << " threads) ---\n";

        auto start = high_resolution_clock::now();
        correlate_openmp(ny, nx, data, result_omp, num_threads);
        auto end = high_resolution_clock::now();

        double time_omp = duration<double>(end - start).count();

        cout << "Execution time: " << fixed << setprecision(6) << time_omp << " seconds\n";
        cout << "Throughput: " << fixed << setprecision(2)
             << (ny * (ny + 1) / 2) / time_omp << " correlations/second\n";

        if (run_seq) {
            double time_seq = 0.0;
            auto start_ref = high_resolution_clock::now();
            correlate_sequential(ny, nx, data, result_seq);
            auto end_ref = high_resolution_clock::now();
            time_seq = duration<double>(end_ref - start_ref).count();

            double speedup = time_seq / time_omp;
            double efficiency = (speedup / num_threads) * 100.0;

            cout << "Speedup: " << fixed << setprecision(2) << speedup << "x\n";
            cout << "Efficiency: " << fixed << setprecision(1) << efficiency << "%\n";

            // Verify correctness
            cout << "Verifying correctness... ";
            if (verify_results(result_seq, result_omp, ny)) {
                cout << "PASSED\n";
            } else {
                cout << "FAILED\n";
            }
        }

        print_sample_results(result_omp, ny);
    }

    // =======================================================================
    // VERSION 3: HIGHLY OPTIMIZED
    // =======================================================================
    if (run_opt) {
        cout << "\n--- VERSION 3: HIGHLY OPTIMIZED (" << num_threads << " threads + SIMD) ---\n";

        auto start = high_resolution_clock::now();
        correlate_optimized(ny, nx, data, result_opt, num_threads);
        auto end = high_resolution_clock::now();

        double time_opt = duration<double>(end - start).count();

        cout << "Execution time: " << fixed << setprecision(6) << time_opt << " seconds\n";
        cout << "Throughput: " << fixed << setprecision(2)
             << (ny * (ny + 1) / 2) / time_opt << " correlations/second\n";

        if (run_seq) {
            double time_seq = 0.0;
            auto start_ref = high_resolution_clock::now();
            correlate_sequential(ny, nx, data, result_seq);
            auto end_ref = high_resolution_clock::now();
            time_seq = duration<double>(end_ref - start_ref).count();

            double speedup = time_seq / time_opt;
            double efficiency = (speedup / num_threads) * 100.0;

            cout << "Speedup: " << fixed << setprecision(2) << speedup << "x\n";
            cout << "Efficiency: " << fixed << setprecision(1) << efficiency << "%\n";

            // Verify correctness
            cout << "Verifying correctness... ";
            if (verify_results(result_seq, result_opt, ny)) {
                cout << "PASSED\n";
            } else {
                cout << "FAILED\n";
            }
        } else if (run_omp) {
            // Compare with OpenMP version
            cout << "Verifying correctness... ";
            if (verify_results(result_omp, result_opt, ny)) {
                cout << "PASSED\n";
            } else {
                cout << "FAILED\n";
            }
        }

        print_sample_results(result_opt, ny);
    }

    // =======================================================================
    // PERFORMANCE SUMMARY
    // =======================================================================
    if (version_str == "all") {
        cout << "\n=========================================================================\n";
        cout << "PERFORMANCE SUMMARY\n";
        cout << "=========================================================================\n";

        // Re-run for accurate comparison
        auto start_seq = high_resolution_clock::now();
        correlate_sequential(ny, nx, data, result_seq);
        auto end_seq = high_resolution_clock::now();
        double time_seq = duration<double>(end_seq - start_seq).count();

        auto start_omp = high_resolution_clock::now();
        correlate_openmp(ny, nx, data, result_omp, num_threads);
        auto end_omp = high_resolution_clock::now();
        double time_omp = duration<double>(end_omp - start_omp).count();

        auto start_opt = high_resolution_clock::now();
        correlate_optimized(ny, nx, data, result_opt, num_threads);
        auto end_opt = high_resolution_clock::now();
        double time_opt = duration<double>(end_opt - start_opt).count();

        cout << fixed << setprecision(6);
        cout << "Sequential:  " << time_seq << " s  (baseline)\n";
        cout << "OpenMP:      " << time_omp << " s  (speedup: "
             << setprecision(2) << (time_seq / time_omp) << "x)\n";
        cout << "Optimized:   " << time_opt << " s  (speedup: "
             << setprecision(2) << (time_seq / time_opt) << "x)\n";
        cout << "\nOptimized vs OpenMP: " << setprecision(2)
             << (time_omp / time_opt) << "x faster\n";
        cout << "=========================================================================\n";
    }

    // Cleanup
    delete[] data;
    delete[] result_seq;
    delete[] result_omp;
    delete[] result_opt;

    return 0;
}
