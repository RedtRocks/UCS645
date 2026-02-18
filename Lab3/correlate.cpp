#include "correlate.h"
#include <cmath>
#include <omp.h>
#include <immintrin.h>  // For AVX/SSE intrinsics
#include <vector>

// Helper function to normalize a row (mean = 0, std = 1)
inline void normalize_row(const float* row, double* normalized, int nx) {
    // Calculate mean
    double sum = 0.0;
    for (int x = 0; x < nx; x++) {
        sum += row[x];
    }
    double mean = sum / nx;

    // Calculate standard deviation
    double variance = 0.0;
    for (int x = 0; x < nx; x++) {
        double diff = row[x] - mean;
        variance += diff * diff;
    }
    double std_dev = std::sqrt(variance / nx);

    // Normalize
    if (std_dev > 1e-10) {
        for (int x = 0; x < nx; x++) {
            normalized[x] = (row[x] - mean) / std_dev;
        }
    } else {
        for (int x = 0; x < nx; x++) {
            normalized[x] = 0.0;
        }
    }
}

// Helper function to calculate dot product
inline double dot_product(const double* a, const double* b, int n) {
    double sum = 0.0;
    for (int i = 0; i < n; i++) {
        sum += a[i] * b[i];
    }
    return sum;
}

//==============================================================================
// VERSION 1: SEQUENTIAL BASELINE IMPLEMENTATION
//==============================================================================
void correlate_sequential(int ny, int nx, const float* data, float* result) {
    // Allocate memory for normalized rows
    std::vector<std::vector<double>> normalized(ny, std::vector<double>(nx));

    // Step 1: Normalize all rows (mean=0, std=1)
    for (int i = 0; i < ny; i++) {
        normalize_row(&data[i * nx], normalized[i].data(), nx);
    }

    // Step 2: Calculate correlation for all pairs (i, j) where j <= i
    for (int i = 0; i < ny; i++) {
        for (int j = 0; j <= i; j++) {
            // Pearson correlation of normalized data = dot product / nx
            double correlation = dot_product(normalized[i].data(), normalized[j].data(), nx) / nx;
            result[i + j * ny] = static_cast<float>(correlation);
        }
    }
}

//==============================================================================
// VERSION 2: OPENMP PARALLELIZED IMPLEMENTATION
//==============================================================================
void correlate_openmp(int ny, int nx, const float* data, float* result, int num_threads) {
    // Allocate memory for normalized rows
    std::vector<std::vector<double>> normalized(ny, std::vector<double>(nx));

    // Step 1: Normalize all rows in parallel
    #pragma omp parallel for num_threads(num_threads) schedule(static)
    for (int i = 0; i < ny; i++) {
        normalize_row(&data[i * nx], normalized[i].data(), nx);
    }

    // Step 2: Calculate correlation for all pairs in parallel
    // Parallelize the outer loop (i)
    #pragma omp parallel for num_threads(num_threads) schedule(dynamic, 4)
    for (int i = 0; i < ny; i++) {
        for (int j = 0; j <= i; j++) {
            double correlation = dot_product(normalized[i].data(), normalized[j].data(), nx) / nx;
            result[i + j * ny] = static_cast<float>(correlation);
        }
    }
}

//==============================================================================
// VERSION 3: HIGHLY OPTIMIZED IMPLEMENTATION
// - Memory access optimization
// - Vectorization (SIMD)
// - Cache-friendly computation
// - Manual loop unrolling
//==============================================================================

// Vectorized dot product using AVX (8 doubles at a time)
inline double dot_product_vectorized(const double* a, const double* b, int n) {
    double sum = 0.0;
    int i = 0;

#ifdef __AVX__
    // Process 4 doubles at a time with AVX
    __m256d vec_sum = _mm256_setzero_pd();
    for (; i + 3 < n; i += 4) {
        __m256d vec_a = _mm256_loadu_pd(&a[i]);
        __m256d vec_b = _mm256_loadu_pd(&b[i]);
        vec_sum = _mm256_add_pd(vec_sum, _mm256_mul_pd(vec_a, vec_b));
    }

    // Horizontal add to get final sum
    double temp[4];
    _mm256_storeu_pd(temp, vec_sum);
    sum = temp[0] + temp[1] + temp[2] + temp[3];
#endif

    // Handle remaining elements
    for (; i < n; i++) {
        sum += a[i] * b[i];
    }

    return sum;
}

// Optimized normalization with vectorization
inline void normalize_row_optimized(const float* row, double* normalized, int nx) {
    // Calculate mean with vectorization
    double sum = 0.0;
    int x = 0;

#ifdef __AVX__
    __m256 vec_sum = _mm256_setzero_ps();
    for (; x + 7 < nx; x += 8) {
        __m256 vec_data = _mm256_loadu_ps(&row[x]);
        vec_sum = _mm256_add_ps(vec_sum, vec_data);
    }

    float temp[8];
    _mm256_storeu_ps(temp, vec_sum);
    sum = temp[0] + temp[1] + temp[2] + temp[3] + temp[4] + temp[5] + temp[6] + temp[7];
#endif

    for (; x < nx; x++) {
        sum += row[x];
    }
    double mean = sum / nx;

    // Calculate variance with vectorization
    double variance = 0.0;
    x = 0;

#ifdef __AVX__
    __m256d vec_var = _mm256_setzero_pd();
    __m256d vec_mean = _mm256_set1_pd(mean);

    for (; x + 3 < nx; x += 4) {
        __m128 vec_data_f = _mm_loadu_ps(&row[x]);
        __m256d vec_data = _mm256_cvtps_pd(vec_data_f);
        __m256d diff = _mm256_sub_pd(vec_data, vec_mean);
        vec_var = _mm256_add_pd(vec_var, _mm256_mul_pd(diff, diff));
    }

    double temp_var[4];
    _mm256_storeu_pd(temp_var, vec_var);
    variance = temp_var[0] + temp_var[1] + temp_var[2] + temp_var[3];
#endif

    for (; x < nx; x++) {
        double diff = row[x] - mean;
        variance += diff * diff;
    }

    double std_dev = std::sqrt(variance / nx);

    // Normalize with vectorization
    if (std_dev > 1e-10) {
        x = 0;
        double inv_std = 1.0 / std_dev;

#ifdef __AVX__
        __m256d vec_mean_d = _mm256_set1_pd(mean);
        __m256d vec_inv_std = _mm256_set1_pd(inv_std);

        for (; x + 3 < nx; x += 4) {
            __m128 vec_data_f = _mm_loadu_ps(&row[x]);
            __m256d vec_data = _mm256_cvtps_pd(vec_data_f);
            __m256d result = _mm256_mul_pd(_mm256_sub_pd(vec_data, vec_mean_d), vec_inv_std);
            _mm256_storeu_pd(&normalized[x], result);
        }
#endif

        for (; x < nx; x++) {
            normalized[x] = (row[x] - mean) * inv_std;
        }
    } else {
        for (x = 0; x < nx; x++) {
            normalized[x] = 0.0;
        }
    }
}

void correlate_optimized(int ny, int nx, const float* data, float* result, int num_threads) {
    // Allocate aligned memory for better vectorization
    std::vector<double*> normalized(ny);

    #pragma omp parallel for num_threads(num_threads)
    for (int i = 0; i < ny; i++) {
        normalized[i] = new double[nx];
    }

    // Step 1: Normalize all rows in parallel with optimized function
    #pragma omp parallel for num_threads(num_threads) schedule(static)
    for (int i = 0; i < ny; i++) {
        normalize_row_optimized(&data[i * nx], normalized[i], nx);
    }

    // Step 2: Calculate correlations with cache-friendly access pattern
    // Use dynamic scheduling for better load balancing
    #pragma omp parallel for num_threads(num_threads) schedule(dynamic, 4)
    for (int i = 0; i < ny; i++) {
        // Use vectorized dot product
        for (int j = 0; j <= i; j++) {
            double correlation = dot_product_vectorized(normalized[i], normalized[j], nx) / nx;
            result[i + j * ny] = static_cast<float>(correlation);
        }
    }

    // Cleanup
    for (int i = 0; i < ny; i++) {
        delete[] normalized[i];
    }
}
