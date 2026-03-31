#include <mpi.h>
#include <iostream>
#include <numeric>
#include <vector>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int rank = 0;
    int size = 0;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int n = 100;
    std::vector<int> full_array;
    if (rank == 0) {
        full_array.resize(n);
        for (int i = 0; i < n; ++i) {
            full_array[i] = i + 1;
        }
    }

    std::vector<int> counts(size, n / size);
    for (int i = 0; i < (n % size); ++i) {
        counts[i]++;
    }

    std::vector<int> displs(size, 0);
    for (int i = 1; i < size; ++i) {
        displs[i] = displs[i - 1] + counts[i - 1];
    }

    std::vector<int> local(counts[rank]);
    MPI_Scatterv(
        rank == 0 ? full_array.data() : nullptr,
        counts.data(),
        displs.data(),
        MPI_INT,
        local.data(),
        counts[rank],
        MPI_INT,
        0,
        MPI_COMM_WORLD
    );

    const int local_sum = std::accumulate(local.begin(), local.end(), 0);
    int global_sum = 0;
    MPI_Reduce(&local_sum, &global_sum, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        const double average = static_cast<double>(global_sum) / n;
        std::cout << "Global sum = " << global_sum << std::endl;
        std::cout << "Expected   = 5050" << std::endl;
        std::cout << "Average    = " << average << std::endl;
    }

    MPI_Finalize();
    return 0;
}
