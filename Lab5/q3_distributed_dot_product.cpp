#include <mpi.h>
#include <cmath>
#include <cstdlib>
#include <iostream>

namespace
{
    constexpr long long kTotalElements = 500000000LL;
}

int main(int argc, char **argv)
{
    MPI_Init(&argc, &argv);

    int rank = 0;
    int size = 0;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    double multiplier = 1.0;
    if (rank == 0 && argc >= 2)
    {
        multiplier = std::atof(argv[1]);
    }

    MPI_Barrier(MPI_COMM_WORLD);
    const double t0 = MPI_Wtime();

    MPI_Bcast(&multiplier, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    const long long base = kTotalElements / size;
    const long long rem = kTotalElements % size;
    const long long local_n = base + ((rank < rem) ? 1LL : 0LL);

    double local_dot = 0.0;
    for (long long i = 0; i < local_n; ++i)
    {
        const double a = 1.0;
        const double b = 2.0 * multiplier;
        local_dot += a * b;
    }

    double global_dot = 0.0;
    MPI_Reduce(&local_dot, &global_dot, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

    const double local_elapsed = MPI_Wtime() - t0;
    double total_time = 0.0;
    MPI_Reduce(&local_elapsed, &total_time, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);

    if (rank == 0)
    {
        const double expected = static_cast<double>(kTotalElements) * 2.0 * multiplier;
        const double error = std::fabs(global_dot - expected);
        const bool ok = error < 1e-6;

        std::cout << "Q3 Distributed Dot Product (N=" << kTotalElements << ")\n";
        std::cout << "Multiplier broadcasted: " << multiplier << "\n";
        std::cout << "Validation: " << (ok ? "PASS" : "FAIL") << " error=" << error << "\n";
        std::cout
            << "RESULT_Q3 procs=" << size
            << " total_time=" << total_time
            << " multiplier=" << multiplier
            << " dot=" << global_dot
            << " expected=" << expected
            << " error=" << error
            << std::endl;
    }

    MPI_Finalize();
    return 0;
}
