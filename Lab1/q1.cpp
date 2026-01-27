#include <iostream>
#include <vector>
#include <omp.h>
#include <algorithm> // For std::max

#define N (1 << 16)

int main()
{
    std::vector<double> X(N), Y(N);
    double a = 2.5;

    // Initialize vectors
    for (int i = 0; i < N; i++)
    {
        X[i] = i * 1.0;
        Y[i] = i * 2.0;
    }

    std::cout << "DAXPY OpenMP Performance\n";
    std::cout << "Vector size: " << N << "\n\n";

    double base_time = 0.0; // Time for the smallest number of threads
    double max_speedup = 0.0;
    int optimal_threads = 2;

    for (int threads = 2; threads <= 256; threads *= 2)
    {
        omp_set_num_threads(threads);

        double start = omp_get_wtime();

#pragma omp parallel for
        for (int i = 0; i < N; i++)
        {
            X[i] = a * X[i] + Y[i];
        }

        double end = omp_get_wtime();
        double elapsed_time = end - start;

        if (threads == 2)
        {
            base_time = elapsed_time; // Record the base time for 2 threads
        }

        double speedup = base_time / elapsed_time;
        if (speedup > max_speedup)
        {
            max_speedup = speedup;
            optimal_threads = threads;
        }

        std::cout << "Threads: " << threads
                  << " | Time: " << elapsed_time << " seconds"
                  << " | Speedup: " << speedup << "\n";
    }

    std::cout << "\nMaximum Speedup: " << max_speedup
              << " achieved with " << optimal_threads << " threads.\n";

    return 0;
}
