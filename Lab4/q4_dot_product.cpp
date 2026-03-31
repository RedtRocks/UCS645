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

    const int n = 8;
    std::vector<int> vec_a;
    std::vector<int> vec_b;

    if (rank == 0) {
        vec_a = {1, 2, 3, 4, 5, 6, 7, 8};
        vec_b = {8, 7, 6, 5, 4, 3, 2, 1};
    }

    std::vector<int> counts(size, n / size);
    for (int i = 0; i < (n % size); ++i) {
        counts[i]++;
    }

    std::vector<int> displs(size, 0);
    for (int i = 1; i < size; ++i) {
        displs[i] = displs[i - 1] + counts[i - 1];
    }

    std::vector<int> local_a(counts[rank]);
    std::vector<int> local_b(counts[rank]);

    MPI_Scatterv(
        rank == 0 ? vec_a.data() : nullptr,
        counts.data(),
        displs.data(),
        MPI_INT,
        local_a.data(),
        counts[rank],
        MPI_INT,
        0,
        MPI_COMM_WORLD
    );

    MPI_Scatterv(
        rank == 0 ? vec_b.data() : nullptr,
        counts.data(),
        displs.data(),
        MPI_INT,
        local_b.data(),
        counts[rank],
        MPI_INT,
        0,
        MPI_COMM_WORLD
    );

    int local_dot = 0;
    for (int i = 0; i < counts[rank]; ++i) {
        local_dot += local_a[i] * local_b[i];
    }

    int global_dot = 0;
    MPI_Reduce(&local_dot, &global_dot, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        std::cout << "Dot product = " << global_dot << std::endl;
        std::cout << "Expected    = 120" << std::endl;
    }

    MPI_Finalize();
    return 0;
}
