#include <mpi.h>
#include <algorithm>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <vector>

int main(int argc, char **argv)
{
    MPI_Init(&argc, &argv);

    int rank = 0;
    int size = 0;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    std::srand(static_cast<unsigned int>(std::time(nullptr)) + rank * 97U);

    const int kCount = 10;
    std::vector<int> local_values(kCount);
    for (int i = 0; i < kCount; ++i)
    {
        local_values[i] = std::rand() % 1001;
    }

    const int local_max = *std::max_element(local_values.begin(), local_values.end());
    const int local_min = *std::min_element(local_values.begin(), local_values.end());

    int global_max = 0;
    int global_min = 0;
    MPI_Reduce(&local_max, &global_max, 1, MPI_INT, MPI_MAX, 0, MPI_COMM_WORLD);
    MPI_Reduce(&local_min, &global_min, 1, MPI_INT, MPI_MIN, 0, MPI_COMM_WORLD);

    int max_pair[2] = {local_max, rank};
    int min_pair[2] = {local_min, rank};
    int global_max_pair[2] = {0, 0};
    int global_min_pair[2] = {0, 0};

    MPI_Reduce(max_pair, global_max_pair, 1, MPI_2INT, MPI_MAXLOC, 0, MPI_COMM_WORLD);
    MPI_Reduce(min_pair, global_min_pair, 1, MPI_2INT, MPI_MINLOC, 0, MPI_COMM_WORLD);

    std::cout << "Process " << rank << " values:";
    for (int v : local_values)
    {
        std::cout << ' ' << v;
    }
    std::cout << " | local_min=" << local_min << " local_max=" << local_max << std::endl;

    if (rank == 0)
    {
        std::cout << "Global maximum = " << global_max
                  << " (from process " << global_max_pair[1] << ")" << std::endl;
        std::cout << "Global minimum = " << global_min
                  << " (from process " << global_min_pair[1] << ")" << std::endl;
    }

    MPI_Finalize();
    return 0;
}
