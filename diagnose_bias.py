"""Diagnose search biases: does an algorithm do well because of WHERE the
optimum is, rather than because it searches well?

Two controlled comparisons, each changing only the optimum's position:

1. Centre bias   - Sphere with optimum at the origin vs. at a random point.
2. Diagonal bias - optimum ON the main diagonal (all coordinates equal) vs. off
                   it. Sphere shifted to (60, ..., 60) vs. a random point, and
                   Schwefel (optimum at (420.97, ..., 420.97)) vs. the same
                   function with random coordinate sign flips.

An unbiased algorithm scores about the same within each pair.
Output: results/bias_diagnostics.md
"""
import itertools
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from optimizers import ALL
from problems import Shifted, SignFlipped, schwefel, sphere

DIM = 30
POP = 30
MAX_EVALS = 6000
N_RUNS = 10
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


class OnDiagonal:
    """Sphere with optimum at (c, ..., c)."""

    def __init__(self, c):
        self.c = c

    def __call__(self, x):
        return sphere(x - self.c)


PROBLEMS = {
    "Sphere, optimum at centre": (sphere, -100.0, 100.0),
    "Sphere, optimum at random point": (Shifted(sphere, -100, 100, seed=11), -100.0, 100.0),
    "Sphere, optimum at (60,...,60)": (OnDiagonal(60.0), -100.0, 100.0),
    "Schwefel, optimum on diagonal": (schwefel, -500.0, 500.0),
    "Schwefel, signs flipped": (SignFlipped(schwefel, seed=12), -500.0, 500.0),
}


def run_one(job):
    pname, aname, seed = job
    func, lb, ub = PROBLEMS[pname]
    _, f, _ = ALL[aname](pop_size=POP, max_evals=MAX_EVALS, seed=seed).optimize(func, DIM, lb, ub)
    return pname, aname, f


def main():
    os.makedirs(OUT, exist_ok=True)
    jobs = list(itertools.product(PROBLEMS, ALL, range(N_RUNS)))
    with ProcessPoolExecutor() as ex:
        res = list(ex.map(run_one, jobs, chunksize=4))
    mean = {}
    for p, a, f in res:
        mean.setdefault((p, a), []).append(f)
    mean = {k: np.mean(v) for k, v in mean.items()}

    names = list(ALL)
    lines = [f"# Bias diagnostics\n\ndim={DIM}, {MAX_EVALS} evaluations, "
             f"{N_RUNS} runs, mean final fitness (all optima = 0). Within each "
             "group only the optimum's position changes.\n",
             "| Problem | " + " | ".join(names) + " |",
             "|---|" + "---|" * len(names)]
    for p in PROBLEMS:
        lines.append(f"| {p} | " + " | ".join(f"{mean[(p, a)]:.1e}" for a in names) + " |")
    text = "\n".join(lines) + "\n"
    with open(os.path.join(OUT, "bias_diagnostics.md"), "w") as fh:
        fh.write(text)
    print(text)


if __name__ == "__main__":
    main()
