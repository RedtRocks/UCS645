#include <mpi.h>
#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <vector>

namespace
{

    bool is_perfect(int n)
    {
        if (n < 2)
        {
            return false;
        }

        int sum = 1;
        const int limit = static_cast<int>(std::sqrt(static_cast<double>(n)));
        for (int d = 2; d <= limit; ++d)
        {
            if (n % d == 0)
            {
                sum += d;
                const int q = n / d;
                if (q != d)
                {
                    sum += q;
                }
            }
        }

        return sum == n;
    }

    void run_serial(int max_value)
    {
        std::vector<int> perfects;
        for (int n = 2; n <= max_value; ++n)
        {
            if (is_perfect(n))
            {
                perfects.push_back(n);
            }
        }

        std::cout << "Q5 Perfect numbers up to " << max_value << " (serial mode)\n";
        std::cout << "Perfect numbers found: " << perfects.size() << "\n";
        std::cout << "Perfect numbers:";
        for (int p : perfects)
        {
            std::cout << ' ' << p;
        }
        std::cout << "\n";
        std::cout << "RESULT_Q5 max=" << max_value << " perfect_found=" << perfects.size() << std::endl;
    }

    void run_master(int size, int max_value)
    {
        std::vector<int> perfects;

        int next_value = 2;
        int active_slaves = size - 1;

        while (active_slaves > 0)
        {
            int reply = 0;
            MPI_Status status;
            MPI_Recv(&reply, 1, MPI_INT, MPI_ANY_SOURCE, 0, MPI_COMM_WORLD, &status);

            const int src = status.MPI_SOURCE;
            if (reply > 1)
            {
                perfects.push_back(reply);
            }

            if (next_value <= max_value)
            {
                int work_item = next_value;
                ++next_value;
                MPI_Send(&work_item, 1, MPI_INT, src, 1, MPI_COMM_WORLD);
            }
            else
            {
                const int stop = 0;
                MPI_Send(&stop, 1, MPI_INT, src, 1, MPI_COMM_WORLD);
                --active_slaves;
            }
        }

        std::sort(perfects.begin(), perfects.end());

        std::cout << "Q5 Perfect numbers up to " << max_value << " (master/slave mode)\n";
        std::cout << "Perfect numbers found: " << perfects.size() << "\n";
        std::cout << "Perfect numbers:";
        for (int p : perfects)
        {
            std::cout << ' ' << p;
        }
        std::cout << "\n";
        std::cout << "RESULT_Q5 max=" << max_value << " perfect_found=" << perfects.size() << std::endl;
    }

    void run_slave()
    {
        int request = 0;
        MPI_Send(&request, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);

        while (true)
        {
            int n = 0;
            MPI_Recv(&n, 1, MPI_INT, 0, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

            if (n == 0)
            {
                break;
            }

            const int result = is_perfect(n) ? n : -n;
            MPI_Send(&result, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
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

    const int max_value = (argc >= 2) ? std::atoi(argv[1]) : 10000;

    if (max_value < 2)
    {
        if (rank == 0)
        {
            std::cerr << "Maximum value must be >= 2." << std::endl;
        }
        MPI_Finalize();
        return 1;
    }

    if (size == 1)
    {
        if (rank == 0)
        {
            run_serial(max_value);
        }
        MPI_Finalize();
        return 0;
    }

    if (rank == 0)
    {
        run_master(size, max_value);
    }
    else
    {
        run_slave();
    }

    MPI_Finalize();
    return 0;
}
