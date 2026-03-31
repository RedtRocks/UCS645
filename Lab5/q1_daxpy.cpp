#include <mpi.h>
#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <vector>

namespace
{
    constexpr int kVectorSize = 1 << 16;

    void init_vectors(std::vector<double> &x, std::vector<double> &y)
    {
        for (int i = 0; i < kVectorSize; ++i)
        {
            x[i] = 1.0 + static_cast<double>(i % 100);
            y[i] = 2.0 + static_cast<double>(i % 50);
        }
    }
}

int main(int argc, char **argv)
{
    MPI_Init(&argc, &argv);

    int rank = 0;
    int size = 0;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const double a = (argc >= 2) ? std::atof(argv[1]) : 2.5;

    std::vector<int> counts(size, 0);
    std::vector<int> displs(size, 0);
    const int base = kVectorSize / size;
    const int rem = kVectorSize % size;

    int offset = 0;
    for (int i = 0; i < size; ++i)
    {
        counts[i] = base + ((i < rem) ? 1 : 0);
        displs[i] = offset;
        offset += counts[i];
    }

    const int local_n = counts[rank];
    std::vector<double> local_x(local_n);
    std::vector<double> local_y(local_n);

    std::vector<double> x;
    std::vector<double> y;
    std::vector<double> x_serial;

    double serial_time = 0.0;

    if (rank == 0)
    {
        x.resize(kVectorSize);
        y.resize(kVectorSize);
        x_serial.resize(kVectorSize);

        init_vectors(x, y);
        x_serial = x;

        const double t0 = MPI_Wtime();
        for (int i = 0; i < kVectorSize; ++i)
        {
            x_serial[i] = a * x_serial[i] + y[i];
        }
        serial_time = MPI_Wtime() - t0;
    }

    MPI_Bcast(&serial_time, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    MPI_Barrier(MPI_COMM_WORLD);
    const double p0 = MPI_Wtime();

    MPI_Scatterv(
        rank == 0 ? x.data() : nullptr,
        counts.data(),
        displs.data(),
        MPI_DOUBLE,
        local_x.data(),
        local_n,
        MPI_DOUBLE,
        0,
        MPI_COMM_WORLD);

    MPI_Scatterv(
        rank == 0 ? y.data() : nullptr,
        counts.data(),
        displs.data(),
        MPI_DOUBLE,
        local_y.data(),
        local_n,
        MPI_DOUBLE,
        0,
        MPI_COMM_WORLD);

    for (int i = 0; i < local_n; ++i)
    {
        local_x[i] = a * local_x[i] + local_y[i];
    }

    MPI_Gatherv(
        local_x.data(),
        local_n,
        MPI_DOUBLE,
        rank == 0 ? x.data() : nullptr,
        counts.data(),
        displs.data(),
        MPI_DOUBLE,
        0,
        MPI_COMM_WORLD);

    const double local_parallel_elapsed = MPI_Wtime() - p0;
    double parallel_time = 0.0;
    MPI_Reduce(
        &local_parallel_elapsed,
        &parallel_time,
        1,
        MPI_DOUBLE,
        MPI_MAX,
        0,
        MPI_COMM_WORLD);

    if (rank == 0)
    {
        double max_err = 0.0;
        bool ok = true;
        for (int i = 0; i < kVectorSize; ++i)
        {
            const double err = std::fabs(x[i] - x_serial[i]);
            max_err = std::max(max_err, err);
            if (err > 1e-9)
            {
                ok = false;
            }
        }

        const double speedup = serial_time / parallel_time;
        const double efficiency = (speedup / static_cast<double>(size)) * 100.0;

        std::cout << "Q1 DAXPY (N=" << kVectorSize << ", a=" << a << ")\n";
        std::cout << "Validation: " << (ok ? "PASS" : "FAIL") << " max_error=" << max_err << "\n";
        std::cout
            << "RESULT_Q1 procs=" << size
            << " serial_time=" << serial_time
            << " parallel_time=" << parallel_time
            << " speedup=" << speedup
            << " efficiency=" << efficiency
            << std::endl;
    }

    MPI_Finalize();
    return 0;
}
