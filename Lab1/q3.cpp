#include <stdio.h>
#include <omp.h>

static long num_steps = 100000000;

int main()
{
    int num_threads = 1;

    omp_set_num_threads(num_threads);

    double step = 1.0 / (double)num_steps;
    double sum = 0.0;

    double start = omp_get_wtime();

#pragma omp parallel for reduction(+ : sum)
    for (long i = 0; i < num_steps; i++)
    {
        double x = (i + 0.5) * step;
        sum += 4.0 / (1.0 + x * x);
    }

    double pi = step * sum;
    double end = omp_get_wtime();

    printf("Q3 Pi Calculation | Threads = %d | Pi = %.12f | Time = %f seconds\n",
           num_threads, pi, end - start);

    return 0;
}
