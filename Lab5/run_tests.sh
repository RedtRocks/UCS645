#!/usr/bin/env bash

set -euo pipefail

TIMEOUT_SECONDS="${TIMEOUT_SECONDS:-180}"
CSV_FILE="timing_results_q5.csv"
Q4_OUTPUT="q4_output.txt"
Q5_OUTPUT="q5_output.txt"

Q1_PROCS=(1 2 4 8)
Q2_PROCS=(2 4 8 16)
Q3_PROCS=(1 2 4 8)

extract_value() {
    local line="$1"
    local key="$2"
    echo "$line" | tr ' ' '\n' | awk -F'=' -v k="$key" '$1==k {print $2}'
}

run_with_timeout() {
    local proc_count="$1"
    shift
    timeout "${TIMEOUT_SECONDS}s" mpirun -np "${proc_count}" "$@"
}

for bin in q1_daxpy q2_broadcast_race q3_distributed_dot_product q4_master_slave_primes q5_master_slave_perfect_numbers; do
    if [ ! -x "./$bin" ]; then
        echo "Error: binary $bin not found. Run 'make' first."
        exit 1
    fi
done

echo "question,method,processes,time_seconds,speedup,efficiency,notes" > "$CSV_FILE"

echo "Running Q1 (DAXPY scaling)..."
for p in "${Q1_PROCS[@]}"; do
    output="$(run_with_timeout "$p" ./q1_daxpy)"
    line="$(echo "$output" | grep 'RESULT_Q1' | tail -1)"

    parallel_time="$(extract_value "$line" "parallel_time")"
    speedup="$(extract_value "$line" "speedup")"
    efficiency="$(extract_value "$line" "efficiency")"

    echo "Q1,DAXPY,$p,$parallel_time,$speedup,$efficiency,serial_vs_parallel" >> "$CSV_FILE"
    echo "  np=$p time=$parallel_time speedup=$speedup efficiency=$efficiency"
done

echo

echo "Running Q2 (Broadcast race)..."
for p in "${Q2_PROCS[@]}"; do
    output="$(run_with_timeout "$p" ./q2_broadcast_race)"
    line="$(echo "$output" | grep 'RESULT_Q2' | tail -1)"

    my_time="$(extract_value "$line" "mybcast_time")"
    mpi_time="$(extract_value "$line" "mpibcast_time")"
    ratio="$(extract_value "$line" "my_over_mpi")"

    echo "Q2,MyBcast,$p,$my_time,NA,NA,my_over_mpi=$ratio" >> "$CSV_FILE"
    echo "Q2,MPI_Bcast,$p,$mpi_time,NA,NA,my_over_mpi=$ratio" >> "$CSV_FILE"
    echo "  np=$p my=$my_time mpi=$mpi_time ratio(my/mpi)=$ratio"
done

echo

echo "Running Q3 (Distributed dot-product scaling)..."
q3_t1=""
for p in "${Q3_PROCS[@]}"; do
    output="$(run_with_timeout "$p" ./q3_distributed_dot_product 1.0)"
    line="$(echo "$output" | grep 'RESULT_Q3' | tail -1)"

    total_time="$(extract_value "$line" "total_time")"

    if [ "$p" -eq 1 ]; then
        q3_t1="$total_time"
        speedup="1.0"
        efficiency="100.0"
    else
        speedup="$(awk -v t1="$q3_t1" -v tp="$total_time" 'BEGIN { printf "%.6f", t1/tp }')"
        efficiency="$(awk -v s="$speedup" -v p="$p" 'BEGIN { printf "%.6f", (s/p)*100.0 }')"
    fi

    echo "Q3,DotProduct,$p,$total_time,$speedup,$efficiency,multiplier=1.0" >> "$CSV_FILE"
    echo "  np=$p time=$total_time speedup=$speedup efficiency=$efficiency"
done

echo

echo "Running Q4 and Q5 functional checks..."
q4_start="$(date +%s.%N)"
run_with_timeout 4 ./q4_master_slave_primes 1000 | tee "$Q4_OUTPUT"
q4_end="$(date +%s.%N)"
q4_time="$(awk -v s="$q4_start" -v e="$q4_end" 'BEGIN { printf "%.6f", e-s }')"
echo "Q4,MasterSlavePrimes,4,$q4_time,NA,NA,max=1000" >> "$CSV_FILE"

q5_start="$(date +%s.%N)"
run_with_timeout 4 ./q5_master_slave_perfect_numbers 10000 | tee "$Q5_OUTPUT"
q5_end="$(date +%s.%N)"
q5_time="$(awk -v s="$q5_start" -v e="$q5_end" 'BEGIN { printf "%.6f", e-s }')"
echo "Q5,MasterSlavePerfect,4,$q5_time,NA,NA,max=10000" >> "$CSV_FILE"

echo

echo "Done. Results written to $CSV_FILE"
