# Sudoku Solver Benchmark

A Python project for modeling and solving Sudoku puzzles using different constraint-solving approaches. The project evaluates solver performance across multiple grid sizes, focusing on execution time, memory consumption, and solving success rate.

## Overview

Sudoku can be formulated as a constraint satisfaction problem and solved using several mathematical and computational approaches. This project implements and compares five solver configurations:

- **SAT with Pairwise Encoding** — encodes at-most-one constraints using pairwise exclusion clauses.
- **SAT with Sequential Encoding** — uses sequential-counter encoding for at-most-one constraints.
- **Constraint Programming (CP)** — models Sudoku using IBM ILOG CP Optimizer.
- **Mixed-Integer Programming (MIP)** — formulates Sudoku as a binary integer optimization model using IBM ILOG CPLEX.
- **Gurobi** — solves a binary integer programming formulation using the Gurobi Optimizer.

The goal is to investigate how solver formulations affect computational performance as Sudoku instances become larger and more challenging.

## Benchmark Setup

The benchmark contains 40 Sudoku instances across four grid sizes.

| Grid size | Number of instances |
|---|---:|
| 9 × 9 | 10 |
| 16 × 16 | 10 |
| 25 × 25 | 10 |
| 36 × 36 | 10 |
| **Total** | **40** |

The instances include different difficulty levels. All solver configurations are evaluated using the same benchmark set.

The evaluation considers:

- Model construction time
- Solving time
- Total execution time
- Peak memory usage
- Number and percentage of instances solved within the time limit

A time limit is used to handle instances that cannot be solved within the allocated time.

## Project Structure

The project is organized into a main entry point, solver implementations, modeling components, and benchmark data.

```text
sudoku-btl
├── data/
├── results/
├── src/
│   ├── modeling/
│   │   ├── ILP_modeling/
│   │   │   │── CplexMIP_modeling.py
│   │   │   └── Gurobi_modeling.py
│   │   ├── SAT_encoding/
│   │   │   │── pairwise_encoding.py
│   │   │   └── sequential_encoding.py
│   │   └── CP_modeling.py
│   ├── processing/
│   │   │── parse_input.py
│   │   └── validator.py
│   └── solver/
│       ├── ILP_solver/
│       │   │── CplexMIP_solver.py
│       │   └── gurobi_solver.py
│       │── CP_solver.py
│       └── SAT_solver.py
│── benchmark.py
│── requirements.txt
└── run.py
```

The directory tree above is a simplified overview. Refer to the repository for the complete file structure and available datasets.

## Requirements

- Python 3
- Python packages required by the selected solver
- **PySAT** for SAT-based solving
- **IBM ILOG CPLEX CP Optimizer** and its Python interface for CP
- **IBM ILOG CPLEX** and its Python interface for MIP
- **Gurobi Optimizer** and its Python interface for Gurobi-based solving

CPLEX and Gurobi may require separate installation, licensing, and environment configuration. Installing Python packages alone may not be sufficient to run these solvers.

## Installation

Clone the repository:

```bash
git clone https://github.com/vuhl1008/sudoku_btl.git
cd sudoku_btl
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the Python dependencies required by the project. If a dependency file is provided in the repository, install from it:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, install the required packages according to the solver implementations you intend to run.

## Running the Project

Run the main entry point from the repository root:

```bash
python benchmark.py
```

The exact command-line arguments and benchmark options depend on the current implementation. Check `main.py` for the supported arguments and configuration options.

## Experimental Results

The experiments compare solver performance across increasing Sudoku grid sizes. The results are analyzed using both computational cost and solving success rate.

The benchmark results show that sequential SAT encoding reduces runtime and memory usage compared with pairwise encoding on larger instances. CP achieves low average runtime on the largest instances solved by all configurations, while the SAT configurations solve all tested 36 × 36 instances under the experimental time limit.

These findings illustrate that solver performance depends on the formulation and evaluation criteria; runtime alone does not fully characterize solver effectiveness.

## Reproducibility

The same benchmark instances are used to compare the solver configurations. Results may depend on the hardware, software versions, solver settings, and license limitations.

For reproducible experiments, record the Python and solver versions, execution environment, time limit, and benchmark configuration.

## Source Code

The source code is available at:

https://github.com/vuhl1008/sudoku_btl
