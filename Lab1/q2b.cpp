#include <stdio.h>
#include <omp.h>

#define N 1000
static double A[N][N], B[N][N], C[N][N];

int main()
{
    int num_threads = 1;

    omp_set_num_threads(num_threads);

    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
        {
            A[i][j] = 1.0;
            B[i][j] = 1.0;
            C[i][j] = 0.0;
        }

    double start = omp_get_wtime();

#pragma omp parallel for collapse(2)
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            for (int k = 0; k < N; k++)
            {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }

    double end = omp_get_wtime();

    printf("Q2 Matrix Multiply 2D | Threads = %d | Time = %f seconds\n",
           num_threads, end - start);

    return 0;
}
