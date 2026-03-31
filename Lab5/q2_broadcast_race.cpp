#include <mpi.h>
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <vector>

namespace
{
    constexpr long long kDefaultArraySize = 10000000LL;

    void fill_buffer(std::vector<double> &buffer, double seed)
    {
        for (long long i = 0; i < static_cast<long long>(buffer.size()); ++i)
        {
            buffer[static_cast<size_t>(i)] = seed + static_cast<double>(i) * 1e-6;
        }
    }

    bool validate_samples(const std::vector<double> &buffer, double seed)
    {
        if (buffer.empty())
        {
            return true;
        }

        const long long n = static_cast<long long>(buffer.size());
        const long long idx[3] = {0, n / 2, n - 1};

        for (long long i : idx)
        {
            const double expected = seed + static_cast<double>(i) * 1e-6;
            const double got = buffer[static_cast<size_t>(i)];
            if (std::fabs(got - expected) > 1e-12)
            {
                return false;
            }
        }
        return true;
    }

    void my_bcast_linear(double *data, int count, int root, MPI_Comm comm)
    {
        int rank = 0;
        int size = 0;
        MPI_Comm_rank(comm, &rank);
        MPI_Comm_size(comm, &size);

        if (rank == root)
        {
            for (int dest = 0; dest < size; ++dest)
            {
                if (dest == root)
                {
                    continue;
                }
                MPI_Send(data, count, MPI_DOUBLE, dest, 100, comm);
            }
        }
        else
        {
            MPI_Recv(data, count, MPI_DOUBLE, root, 100, comm, MPI_STATUS_IGNORE);
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

    const long long array_size = (argc >= 2) ? std::atoll(argv[1]) : kDefaultArraySize;
    if (array_size <= 0 || array_size > std::numeric_limits<int>::max())
    {
        if (rank == 0)
        {
            std::cerr << "Array size must be in range [1, INT_MAX]." << std::endl;
        }
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    std::vector<double> data(static_cast<size_t>(array_size), 0.0);

    if (rank == 0)
    {
        fill_buffer(data, 1.0);
    }

    MPI_Barrier(MPI_COMM_WORLD);
    const double t0 = MPI_Wtime();
    my_bcast_linear(data.data(), static_cast<int>(array_size), 0, MPI_COMM_WORLD);
    MPI_Barrier(MPI_COMM_WORLD);
    const double my_local_time = MPI_Wtime() - t0;

    int my_ok_local = validate_samples(data, 1.0) ? 1 : 0;
    int my_ok_global = 0;
    MPI_Reduce(&my_ok_local, &my_ok_global, 1, MPI_INT, MPI_LAND, 0, MPI_COMM_WORLD);

    if (rank == 0)
    {
        fill_buffer(data, 3.0);
    }

    MPI_Barrier(MPI_COMM_WORLD);
    const double t1 = MPI_Wtime();
    MPI_Bcast(data.data(), static_cast<int>(array_size), MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Barrier(MPI_COMM_WORLD);
    const double mpi_local_time = MPI_Wtime() - t1;

    int mpi_ok_local = validate_samples(data, 3.0) ? 1 : 0;
    int mpi_ok_global = 0;
    MPI_Reduce(&mpi_ok_local, &mpi_ok_global, 1, MPI_INT, MPI_LAND, 0, MPI_COMM_WORLD);

    double my_time = 0.0;
    double mpi_time = 0.0;
    MPI_Reduce(&my_local_time, &my_time, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
    MPI_Reduce(&mpi_local_time, &mpi_time, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);

    if (rank == 0)
    {
        const double ratio = my_time / mpi_time;
        std::cout << "Q2 Broadcast Race (array_size=" << array_size << ")\n";
        std::cout << "Validation MyBcast: " << (my_ok_global ? "PASS" : "FAIL") << "\n";
        std::cout << "Validation MPI_Bcast: " << (mpi_ok_global ? "PASS" : "FAIL") << "\n";
        std::cout
            << "RESULT_Q2 procs=" << size
            << " mybcast_time=" << my_time
            << " mpibcast_time=" << mpi_time
            << " my_over_mpi=" << ratio
            << std::endl;
    }

    MPI_Finalize();
    return 0;
}
