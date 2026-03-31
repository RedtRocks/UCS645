#!/usr/bin/env python3

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt


def parse_float(value):
    if value in ("", "NA", "N/A", None):
        return None
    return float(value)


def load_results(path):
    rows = []
    with open(path, "r", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                {
                    "question": row["question"],
                    "method": row["method"],
                    "processes": int(row["processes"]),
                    "time": parse_float(row["time_seconds"]),
                    "speedup": parse_float(row["speedup"]),
                    "efficiency": parse_float(row["efficiency"]),
                    "notes": row["notes"],
                }
            )
    return rows


def rows_for(rows, question, method=None):
    out = [r for r in rows if r["question"] == question]
    if method is not None:
        out = [r for r in out if r["method"] == method]
    out.sort(key=lambda r: r["processes"])
    return out


def print_table(title, rows, include_speedup=True, include_eff=True):
    print("\n" + "=" * 90)
    print(title)
    print("=" * 90)

    header = ["Question", "Method", "Proc", "Time(s)"]
    if include_speedup:
        header.append("Speedup")
    if include_eff:
        header.append("Efficiency(%)")
    header.append("Notes")
    print(" | ".join(header))
    print("-" * 90)

    for r in rows:
        fields = [
            r["question"],
            r["method"],
            str(r["processes"]),
            f"{r['time']:.6f}" if r["time"] is not None else "NA",
        ]
        if include_speedup:
            fields.append(f"{r['speedup']:.6f}" if r["speedup"] is not None else "NA")
        if include_eff:
            fields.append(f"{r['efficiency']:.6f}" if r["efficiency"] is not None else "NA")
        fields.append(r["notes"])
        print(" | ".join(fields))


def plot_q1(rows):
    q1 = rows_for(rows, "Q1")
    if not q1:
        return

    procs = [r["processes"] for r in q1]
    times = [r["time"] for r in q1]
    speedups = [r["speedup"] for r in q1]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    axes[0].plot(procs, times, marker="o", linewidth=2)
    axes[0].set_title("Q1 DAXPY: Time vs Processes")
    axes[0].set_xlabel("Processes")
    axes[0].set_ylabel("Time (s)")
    axes[0].grid(alpha=0.3)

    axes[1].plot(procs, speedups, marker="s", linewidth=2, label="Measured")
    axes[1].plot(procs, procs, linestyle="--", label="Ideal")
    axes[1].set_title("Q1 DAXPY: Speedup")
    axes[1].set_xlabel("Processes")
    axes[1].set_ylabel("Speedup")
    axes[1].grid(alpha=0.3)
    axes[1].legend()

    fig.tight_layout()
    fig.savefig("q1_daxpy_scaling.png", dpi=150)
    plt.close(fig)


def plot_q2(rows):
    q2_my = rows_for(rows, "Q2", "MyBcast")
    q2_mpi = rows_for(rows, "Q2", "MPI_Bcast")
    if not q2_my or not q2_mpi:
        return

    my_map = {r["processes"]: r["time"] for r in q2_my}
    mpi_map = {r["processes"]: r["time"] for r in q2_mpi}
    procs = sorted(set(my_map.keys()) & set(mpi_map.keys()))

    my_times = [my_map[p] for p in procs]
    mpi_times = [mpi_map[p] for p in procs]
    ratios = [my_map[p] / mpi_map[p] for p in procs]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    axes[0].plot(procs, my_times, marker="o", linewidth=2, label="MyBcast")
    axes[0].plot(procs, mpi_times, marker="s", linewidth=2, label="MPI_Bcast")
    axes[0].set_title("Q2 Broadcast Race: Time Comparison")
    axes[0].set_xlabel("Processes")
    axes[0].set_ylabel("Time (s)")
    axes[0].grid(alpha=0.3)
    axes[0].legend()

    axes[1].plot(procs, ratios, marker="^", linewidth=2)
    axes[1].axhline(1.0, linestyle="--", color="black", alpha=0.5)
    axes[1].set_title("Q2 Ratio: MyBcast / MPI_Bcast")
    axes[1].set_xlabel("Processes")
    axes[1].set_ylabel("Ratio")
    axes[1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig("q2_broadcast_race.png", dpi=150)
    plt.close(fig)


def plot_q3(rows):
    q3 = rows_for(rows, "Q3")
    if not q3:
        return

    procs = [r["processes"] for r in q3]
    times = [r["time"] for r in q3]
    speedups = [r["speedup"] for r in q3]
    effs = [r["efficiency"] for r in q3]

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

    axes[0].plot(procs, times, marker="o", linewidth=2)
    axes[0].set_title("Q3 Dot Product: Time")
    axes[0].set_xlabel("Processes")
    axes[0].set_ylabel("Time (s)")
    axes[0].grid(alpha=0.3)

    axes[1].plot(procs, speedups, marker="s", linewidth=2, label="Measured")
    axes[1].plot(procs, procs, linestyle="--", label="Ideal")
    axes[1].set_title("Q3 Dot Product: Speedup")
    axes[1].set_xlabel("Processes")
    axes[1].set_ylabel("Speedup")
    axes[1].grid(alpha=0.3)
    axes[1].legend()

    axes[2].plot(procs, effs, marker="^", linewidth=2)
    axes[2].axhline(100.0, linestyle="--", color="black", alpha=0.5)
    axes[2].set_title("Q3 Dot Product: Efficiency")
    axes[2].set_xlabel("Processes")
    axes[2].set_ylabel("Efficiency (%)")
    axes[2].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig("q3_dot_product_scaling.png", dpi=150)
    plt.close(fig)


def main():
    csv_path = Path("timing_results_q5.csv")
    if not csv_path.exists():
        raise SystemExit("timing_results_q5.csv not found. Run ./run_tests.sh first.")

    rows = load_results(csv_path)

    print_table("Assignment 5 Timing Summary", rows)

    plot_q1(rows)
    plot_q2(rows)
    plot_q3(rows)

    print("\nGenerated graphs:")
    print(" - q1_daxpy_scaling.png")
    print(" - q2_broadcast_race.png")
    print(" - q3_dot_product_scaling.png")


if __name__ == "__main__":
    main()
