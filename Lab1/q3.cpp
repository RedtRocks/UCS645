#include <iostream>
#include <omp.h>

static long num_steps = 100000000; // increase for better accuracy

int main()
{
    double step;
    double pi = 0.0;
    double sum = 0.0;

    step = 1.0 / (double)num_steps;

    for (int threads = 2; threads <= 256; threads *= 2)
    {
        omp_set_num_threads(threads);
        sum = 0.0;

        double start = omp_get_wtime();

#pragma omp parallel for reduction(+ : sum)
        for (long i = 0; i < num_steps; i++)
        {
            double x = (i + 0.5) * step;
            sum += 4.0 / (1.0 + x * x);
        }

        pi = step * sum;

        double end = omp_get_wtime();

        std::cout << "Threads: " << threads
                  << " | Pi: " << pi
                  << " | Time: " << (end - start) << " seconds\n";
    }

    return 0;
}
