CXX = mpic++
CXXFLAGS = -std=c++17 -O2 -Wall -Wextra

TARGETS = \
	q1_daxpy \
	q2_broadcast_race \
	q3_distributed_dot_product \
	q4_master_slave_primes \
	q5_master_slave_perfect_numbers

all: $(TARGETS)

q1_daxpy: q1_daxpy.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

q2_broadcast_race: q2_broadcast_race.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

q3_distributed_dot_product: q3_distributed_dot_product.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

q4_master_slave_primes: q4_master_slave_primes.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

q5_master_slave_perfect_numbers: q5_master_slave_perfect_numbers.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

run-q1: q1_daxpy
	mpirun -np 4 ./q1_daxpy

run-q2: q2_broadcast_race
	mpirun -np 4 ./q2_broadcast_race

run-q3: q3_distributed_dot_product
	mpirun -np 4 ./q3_distributed_dot_product 1.0

run-q4: q4_master_slave_primes
	mpirun -np 4 ./q4_master_slave_primes 1000

run-q5: q5_master_slave_perfect_numbers
	mpirun -np 4 ./q5_master_slave_perfect_numbers 10000

clean:
	rm -f $(TARGETS)
