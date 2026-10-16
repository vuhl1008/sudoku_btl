
from run import (
    validate_input,
    SAT_solving_with_pairwise,
    SAT_solving_with_sequential,
    CP_solving,
    cplexmip_solving,
    gurobi_solving,
)

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import multiprocessing as mp
import time
import psutil
import math
import queue


DATA_DIR = Path("data")
TIME_LIMIT = 300
REPEAT_RUNS = 5

OUTPUT_CSV = "results/benchmark_summary_all.csv"
DETAIL_CSV = "results/benchmark_details.csv"
INSTANCE_CSV = "results/benchmark_instance_averages.csv"
COMMON_RUNTIME_CSV = "results/benchmark_common_runtime.csv"

SOLVERS = {
    "SAT_pairwise": SAT_solving_with_pairwise,
    "SAT_sequential": SAT_solving_with_sequential,
    "CP": CP_solving,
    "CPLEX_MIP": cplexmip_solving,
    "Gurobi": gurobi_solving,
}


def worker(solver_func, board, output_queue):
    try:
        result = solver_func(board)
        output_queue.put({
            "ok": True,
            "result": result,
        })
    except Exception as exc:
        output_queue.put({
            "ok": False,
            "error": repr(exc),
        })


def process_memory_mb(process):
    try:
        processes = [process] + process.children(recursive=True)
    except (psutil.Error, OSError):
        processes = [process]

    total = 0.0

    for proc in processes:
        try:
            total += proc.memory_info().rss / (1024 ** 2)
        except (psutil.Error, OSError):
            pass

    return total


def run_one(solver_func, board, timeout=TIME_LIMIT):
    ctx = mp.get_context("fork")
    output_queue = ctx.Queue()

    process = ctx.Process(
        target=worker,
        args=(solver_func, board, output_queue),
    )

    start = time.perf_counter()
    process.start()

    child = psutil.Process(process.pid)
    peak_memory_mb = 0.0
    timed_out = False

    while process.is_alive():
        elapsed = time.perf_counter() - start

        try:
            peak_memory_mb = max(
                peak_memory_mb,
                process_memory_mb(child),
            )
        except (psutil.Error, OSError):
            pass

        if elapsed >= timeout:
            timed_out = True
            process.terminate()
            process.join(timeout=2)

            if process.is_alive():
                process.kill()
                process.join()

            break

        time.sleep(0.01)

    process.join()
    elapsed = time.perf_counter() - start

    try:
        message = output_queue.get(timeout=1)
    except queue.Empty:
        message = None

    output_queue.close()

    if timed_out:
        return {
            "solved": False,
            "status": "TIMEOUT",
            "construction_time": None,
            "solve_time": None,
            "total_time": elapsed,
            "peak_memory_mib": peak_memory_mb,
        }

    if message is None or not message["ok"]:
        error_message = (
            message.get("error", "Unknown error")
            if message is not None
            else "Worker exited without returning a result"
        )

        print(f"    Worker error: {error_message}")

        return {
            "solved": False,
            "status": "ERROR",
            "construction_time": None,
            "solve_time": None,
            "total_time": elapsed,
            "peak_memory_mib": peak_memory_mb,
        }

    result = message["result"]

    construction_time = result.get("construction_time")
    solve_time = result.get("solve_time")
    total_time = result.get("total_time", elapsed)

    status = str(result.get("status", "")).upper()

    solved = status in {
        "SAT",
        "FEASIBLE",
        "OPTIMAL",
        "OPTIMAL_SOLUTION",
    }

    return {
        "solved": solved,
        "status": status or "UNKNOWN",
        "construction_time": construction_time,
        "solve_time": solve_time,
        "total_time": total_time,
        "peak_memory_mib": peak_memory_mb,
    }


def average(values):
    values = [
        v for v in values
        if v is not None and not pd.isna(v)
    ]
    return sum(values) / len(values) if values else math.nan


def plot_time(data, size_order, common_runtime_df):
    plot_data = data[
        ["size", "solver", "avg_total_time"]
    ].copy()

    common_rows = common_runtime_df[
        common_runtime_df["size"] == "36x36"
    ]

    for _, row in common_rows.iterrows():
        mask = (
            (plot_data["size"] == "36x36")
            & (plot_data["solver"] == row["solver"])
        )

        plot_data.loc[mask, "avg_total_time"] = (
            row["avg_total_time"]
        )

    pivot_data = plot_data.pivot(
        index="size",
        columns="solver",
        values="avg_total_time",
    )

    pivot_data = pivot_data.reindex(size_order)

    ax = pivot_data.plot(
        kind="bar",
        figsize=(11, 6),
        width=0.8,
    )

    ax.set_xlabel("Sudoku size")
    ax.set_ylabel("Average total time (seconds)")
    ax.set_title("Solver Runtime Comparison Across Sudoku Sizes")
    ax.set_yscale("log")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    ax.legend(title="Solver")

    plt.xticks(rotation=0)
    plt.tight_layout()

    plt.savefig(
        "results/solver_performance_time.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()


def plot_memory(data, size_order):
    pivot_data = data.pivot(
        index="size",
        columns="solver",
        values="avg_peak_memory_mib",
    )

    pivot_data = pivot_data.reindex(size_order)

    ax = pivot_data.plot(
        kind="bar",
        figsize=(11, 6),
        width=0.8,
    )

    ax.set_xlabel("Sudoku size")
    ax.set_ylabel("Average peak memory (MiB)")
    ax.set_title("Solver Memory Usage Across Sudoku Sizes")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    ax.legend(title="Solver")

    plt.xticks(rotation=0)
    plt.tight_layout()

    plt.savefig(
        "results/solver_performance_memory.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()


def build_common_runtime(instance_df, solver_names):
    size_df = instance_df[
        instance_df["size"] == "36x36"
    ].copy()

    columns = [
        "size",
        "solver",
        "common_instances",
        "avg_total_time",
    ]

    if size_df.empty:
        common_df = pd.DataFrame(columns=columns)
        common_df.to_csv(COMMON_RUNTIME_CSV, index=False)
        return common_df

    solved = size_df.pivot(
        index="instance",
        columns="solver",
        values="_solved_runs",
    )

    for solver_name in solver_names:
        if solver_name not in solved.columns:
            solved[solver_name] = 0

    common_instances = solved.index[
        (solved[solver_names] > 0).all(axis=1)
    ].tolist()

    common_rows = size_df[
        size_df["instance"].isin(common_instances)
    ]

    rows = []

    for solver_name in solver_names:
        solver_rows = common_rows[
            common_rows["solver"] == solver_name
        ]

        rows.append({
            "size": "36x36",
            "solver": solver_name,
            "common_instances": len(common_instances),
            "avg_total_time": average(
                solver_rows["avg_total_time"].tolist()
            ),
        })

    common_df = pd.DataFrame(rows, columns=columns)
    common_df.to_csv(COMMON_RUNTIME_CSV, index=False)

    print(f"\n36x36 common instances: {len(common_instances)}")
    print(common_instances)
    print("\nRuntime on common 36x36 instances:")
    print(common_df.to_string(index=False))

    return common_df


def main():
    Path("results").mkdir(parents=True, exist_ok=True)

    size_order = [
        "9x9",
        "16x16",
        "25x25",
        "36x36",
    ]

    folders = {
        folder.name: folder
        for folder in DATA_DIR.iterdir()
        if folder.is_dir()
    }

    folders = [
        folders[size]
        for size in size_order
        if size in folders
    ]

    if not folders:
        raise RuntimeError(
            f"No Sudoku size folders found in {DATA_DIR}"
        )

    detail_rows = []
    instance_average_rows = []
    summary_rows = []

    for folder in folders:
        print("\n" + "=" * 60)
        print(f"BENCHMARK SIZE: {folder.name}")
        print("=" * 60)

        files = sorted(
            p for p in folder.iterdir()
            if p.is_file()
        )[:10]

        if not files:
            print(f"No input files in {folder}, skipping.")
            continue

        for file in files:
            print(f"\nProcessing {file.name}")

            try:
                board = validate_input(file)
            except Exception as exc:
                print(f"  Input error: {exc}")
                continue

            for solver_name, solver_func in SOLVERS.items():
                run_results = []

                for run_id in range(1, REPEAT_RUNS + 1):
                    print(
                        f"  {solver_name}: "
                        f"run {run_id}/{REPEAT_RUNS}",
                        flush=True,
                    )

                    try:
                        item = run_one(
                            solver_func,
                            board,
                            timeout=TIME_LIMIT,
                        )
                    except Exception as exc:
                        print(f"    ERROR: {exc}")

                        item = {
                            "solved": False,
                            "status": "ERROR",
                            "construction_time": None,
                            "solve_time": None,
                            "total_time": None,
                            "peak_memory_mib": None,
                        }

                    item["size"] = folder.name
                    item["instance"] = file.name
                    item["solver"] = solver_name
                    item["run"] = run_id

                    run_results.append(item)
                    detail_rows.append(item.copy())

                    print(
                        f"    solved={item['solved']}, "
                        f"status={item['status']}, "
                        f"time={item['total_time']}, "
                        f"peak RAM={item['peak_memory_mib']}"
                    )

                    if item["status"] == "TIMEOUT":
                        break

                successful_runs = [
                    r for r in run_results
                    if r["solved"]
                ]

                instance_row = {
                    "size": folder.name,
                    "instance": file.name,
                    "solver": solver_name,
                    "_solved_runs": len(successful_runs),
                    "_total_runs": len(run_results),
                }

                for key in [
                    "construction_time",
                    "solve_time",
                    "total_time",
                    "peak_memory_mib",
                ]:
                    instance_row[f"avg_{key}"] = average([
                        r[key] for r in successful_runs
                    ])

                instance_average_rows.append(instance_row)

                print(
                    f"  Instance average total time: "
                    f"{instance_row['avg_total_time']}"
                )

    detail_df = pd.DataFrame(detail_rows)
    detail_df.to_csv(DETAIL_CSV, index=False)

    instance_df = pd.DataFrame(instance_average_rows)

    instance_csv_df = instance_df.drop(
        columns=["_solved_runs", "_total_runs"],
        errors="ignore",
    )

    instance_csv_df.to_csv(INSTANCE_CSV, index=False)

    for size in size_order:
        size_df = instance_df[
            instance_df["size"] == size
        ]

        if size_df.empty:
            continue

        for solver_name in SOLVERS:
            solver_df = size_df[
                size_df["solver"] == solver_name
            ]

            if solver_df.empty:
                continue

            solved_instances = int(
                (solver_df["_solved_runs"] > 0).sum()
            )

            total_instances = len(solver_df)

            row = {
                "size": size,
                "solver": solver_name,
                "solved_instances": solved_instances,
                "total_instances": total_instances,
            }

            for metric in [
                "construction_time",
                "solve_time",
                "total_time",
                "peak_memory_mib",
            ]:
                row[f"avg_{metric}"] = average(
                    solver_df[f"avg_{metric}"].tolist()
                )

            row["success_rate_percent"] = (
                100 * solved_instances / total_instances
                if total_instances
                else math.nan
            )

            summary_rows.append(row)

    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(OUTPUT_CSV, index=False)

    common_runtime_df = build_common_runtime(
        instance_df,
        list(SOLVERS.keys()),
    )

    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(summary_df.to_string(index=False))

    plot_time(
        summary_df,
        size_order,
        common_runtime_df,
    )

    plot_memory(summary_df, size_order)

    print(f"\nSaved detailed runs to {DETAIL_CSV}")
    print(f"Saved instance averages to {INSTANCE_CSV}")
    print(f"Saved summary to {OUTPUT_CSV}")
    print(f"Saved common runtime to {COMMON_RUNTIME_CSV}")
    print("Saved runtime and memory plots in results/")


if __name__ == "__main__":
    main()
