"""Experiment 1: validate the optimizers on benchmark functions.

Runs each algorithm N_RUNS times per function, saves convergence plots and a
results table (mean / std / best of final fitness).
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from optimizers import ALGORITHMS
from problems import BENCHMARKS

DIM = 30
POP = 30
ITERS = 200
N_RUNS = 20
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(OUT, exist_ok=True)

COLORS = {"GA": "#1f77b4", "PSO": "#d62728", "GWO": "#2ca02c", "WOA": "#9467bd"}


def main():
    rows = []
    finals = {}          # (func, algo) -> array of final fitness values
    fig, axes = plt.subplots(1, len(BENCHMARKS), figsize=(5 * len(BENCHMARKS), 4))
    for ax, (fname, (func, lb, ub)) in zip(axes, BENCHMARKS.items()):
        for aname, cls in ALGORITHMS.items():
            hists, fin = [], []
            for seed in range(N_RUNS):
                opt = cls(pop_size=POP, iters=ITERS, seed=seed)
                _, bf, h = opt.optimize(func, DIM, lb, ub)
                hists.append(h)
                fin.append(bf)
            finals[(fname, aname)] = np.array(fin)
            ax.semilogy(np.mean(hists, axis=0) + 1e-300, label=aname,
                        color=COLORS[aname], lw=2)
            rows.append((fname, aname, np.mean(fin), np.std(fin), np.min(fin)))
        ax.set_title(f"{fname} (dim={DIM})")
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Mean best fitness (log)")
        ax.grid(alpha=0.3)
        ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "benchmark_convergence.png"), dpi=150)

    lines = ["| Function | Algorithm | Mean | Std | Best |",
             "|---|---|---|---|---|"]
    for f, a, m, s, b in rows:
        lines.append(f"| {f} | {a} | {m:.3e} | {s:.3e} | {b:.3e} |")
    table = "\n".join(lines)
    with open(os.path.join(OUT, "benchmark_table.md"), "w") as fh:
        fh.write(table + "\n")
    print(table)
    print(f"\nSaved to {OUT}")


if __name__ == "__main__":
    main()
