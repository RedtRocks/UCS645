CXX = mpic++
CXXFLAGS = -std=c++17 -O2 -Wall -Wextra

TARGETS = q1_ring_comm q2_array_sum q3_max_min q4_dot_product

all: $(TARGETS)

q1_ring_comm: q1_ring_comm.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

q2_array_sum: q2_array_sum.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

q3_max_min: q3_max_min.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

q4_dot_product: q4_dot_product.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

run-q1: q1_ring_comm
	mpirun -np 4 ./q1_ring_comm

run-q2: q2_array_sum
	mpirun -np 4 ./q2_array_sum

run-q3: q3_max_min
	mpirun -np 4 ./q3_max_min

run-q4: q4_dot_product
	mpirun -np 4 ./q4_dot_product

clean:
	rm -f $(TARGETS)
