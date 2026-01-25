#include <iostream>
#include <vector>
#include <omp.h>

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

    // Test with increasing number of threads
    for (int threads = 2; threads <= 32; threads *= 2)
    {
        omp_set_num_threads(threads);

        double start = omp_get_wtime();

#pragma omp parallel for
        for (int i = 0; i < N; i++)
        {
            X[i] = a * X[i] + Y[i];
        }

        double end = omp_get_wtime();

        std::cout << "Threads: " << threads
                  << " | Time: " << (end - start) << " seconds\n";
    }

    return 0;
}
