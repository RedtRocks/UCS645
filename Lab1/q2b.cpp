#include <iostream>
#include <vector>
#include <omp.h>

#define N 1000
#define REPEAT 5

int main()
{
    std::vector<double> A(N * N), B(N * N), C(N * N);

    // Initialize matrices
    for (int i = 0; i < N * N; i++)
    {
        A[i] = 1.0;
        B[i] = 2.0;
    }

    std::cout << "Matrix Multiplication - 2D Threading\n";

    for (int threads = 2; threads <= 128; threads *= 2)
    {
        omp_set_num_threads(threads);

        double start = omp_get_wtime();

        for (int r = 0; r < REPEAT; r++)
        {
#pragma omp parallel for collapse(2) schedule(static)
            for (int i = 0; i < N; i++)
            {
                for (int j = 0; j < N; j++)
                {
                    double sum = 0.0;
                    for (int k = 0; k < N; k++)
                    {
                        sum += A[i * N + k] * B[k * N + j];
                    }
                    C[i * N + j] = sum;
                }
            }
        }

        double end = omp_get_wtime();

        std::cout << "Threads: " << threads
                  << " | Time: " << (end - start) << " seconds\n";
    }

    return 0;
}
