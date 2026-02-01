#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define N (1 << 24) // 16 million elements

int main()
{
    int num_threads = 1;

    omp_set_num_threads(num_threads);

    double *X = (double *)malloc(N * sizeof(double));
    double *Y = (double *)malloc(N * sizeof(double));
    double a = 2.5;

    for (int i = 0; i < N; i++)
    {
        X[i] = 1.0;
        Y[i] = 2.0;
    }

    double start = omp_get_wtime();

#pragma omp parallel for
    for (int i = 0; i < N; i++)
    {
        X[i] = a * X[i] + Y[i];
    }

    double end = omp_get_wtime();

    printf("Q1 DAXPY | Threads = %d | Time = %f seconds\n",
           num_threads, end - start);

    free(X);
    free(Y);
    return 0;
}
