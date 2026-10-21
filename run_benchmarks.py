"""Experiment 1: validate the optimizers on benchmark functions.

Every algorithm (plus the Random Search and DE baselines) gets the same budget
of fitness evaluations on each function and is run N_RUNS times. Outputs:

- results/benchmark_convergence.png  convergence vs. evaluations
- results/benchmark_table.md         mean / std / best / time, Friedman ranks
- results/benchmark_stats.md         pairwise Mann-Whitney tests (Holm-corrected)
"""
import itertools
import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from optimizers import ALL
from problems import BENCHMARKS
from stat_tests import friedman, pairwise_table

DIM = 30
POP = 30
MAX_EVALS = 6000          # = 30 individuals x 200 generations
N_RUNS = 20
CURVE_POINTS = 200        # convergence curves are stored at this resolution
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

COLORS = {"GA": "#1f77b4", "PSO": "#d62728", "GWO": "#2ca02c", "WOA": "#9467bd",
          "DE": "#ff7f0e", "Random": "#7f7f7f"}
CENTRED = ["Sphere", "Rastrigin", "Ackley", "Griewank"]


def run_one(job):
    fname, aname, seed = job
    func, lb, ub = BENCHMARKS[fname]
    opt = ALL[aname](pop_size=POP, max_evals=MAX_EVALS, seed=seed)
    t0 = time.perf_counter()
    _, best_f, hist = opt.optimize(func, DIM, lb, ub)
    secs = time.perf_counter() - t0
    assert len(hist) == MAX_EVALS
    idx = np.linspace(0, MAX_EVALS - 1, CURVE_POINTS).astype(int)
    return fname, aname, best_f, hist[idx], secs


def main():
    os.makedirs(OUT, exist_ok=True)
    jobs = list(itertools.product(BENCHMARKS, ALL, range(N_RUNS)))
    print(f"{len(jobs)} runs ({len(BENCHMARKS)} functions x {len(ALL)} algorithms "
          f"x {N_RUNS} seeds), {MAX_EVALS} evaluations each, dim={DIM} ...")
    with ProcessPoolExecutor() as ex:
        results = list(ex.map(run_one, jobs, chunksize=4))

    finals, curves, times = {}, {}, {}
    for fname, aname, bf, h, s in results:
        finals.setdefault((fname, aname), []).append(bf)
        curves.setdefault((fname, aname), []).append(h)
        times.setdefault((fname, aname), []).append(s)

    # ------------------------------------------------------------- plot
    ncol = 5
    nrow = int(np.ceil(len(BENCHMARKS) / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(4.2 * ncol, 3.6 * nrow))
    x = np.linspace(1, MAX_EVALS, CURVE_POINTS)
    for ax, fname in zip(axes.flat, BENCHMARKS):
        for aname in ALL:
            ls = "--" if aname in ("DE", "Random") else "-"
            ax.semilogy(x, np.mean(curves[(fname, aname)], axis=0) + 1e-300,
                        label=aname, color=COLORS[aname], lw=1.8, ls=ls)
        ax.set_title(fname)
        ax.set_xlabel("Fitness evaluations")
        ax.grid(alpha=0.3)
    for ax in axes.flat[len(BENCHMARKS):]:
        ax.axis("off")
    for ax in axes[:, 0]:
        ax.set_ylabel("Mean best fitness (log)")
    axes.flat[0].legend(fontsize=8)
    fig.suptitle(f"Convergence, dim={DIM}, mean of {N_RUNS} runs "
                 f"(dashed = baselines)")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "benchmark_convergence.png"), dpi=150)

    # ---------------------------------------------------- results table
    names = list(ALL)
    lines = [f"Budget: {MAX_EVALS} fitness evaluations per run, dim={DIM}, "
             f"population {POP}, {N_RUNS} runs.\n",
             "| Function | Algorithm | Mean | Std | Best | Time/run (s) |",
             "|---|---|---|---|---|---|"]
    for fname in BENCHMARKS:
        for a in names:
            v = np.array(finals[(fname, a)])
            lines.append(f"| {fname} | {a} | {v.mean():.3e} | {v.std():.3e} | "
                         f"{v.min():.3e} | {np.mean(times[(fname, a)]):.2f} |")

    # compact mean table (what goes in the README)
    summary = ["| Function | " + " | ".join(names) + " |",
               "|---|" + "---|" * len(names)]
    for fname in BENCHMARKS:
        means = {a: np.mean(finals[(fname, a)]) for a in names}
        best = min(means.values())
        cells = [f"**{means[a]:.1e}**" if np.isclose(means[a], best, rtol=1e-9, atol=1e-12)
                 else f"{means[a]:.1e}" for a in names]
        summary.append(f"| {fname} | " + " | ".join(cells) + " |")

    # Friedman ranks over functions (by mean final fitness), overall and per group
    def ranks_for(funcs):
        scores = {a: [np.mean(finals[(f, a)]) for f in funcs] for a in names}
        return friedman(scores)

    off = [f for f in BENCHMARKS if f not in CENTRED]
    r_all, p_all = ranks_for(list(BENCHMARKS))
    r_cen, _ = ranks_for(CENTRED)
    r_off, _ = ranks_for(off)
    rank_lines = ["| Algorithm | Mean rank, all functions | Optimum at centre "
                  f"({len(CENTRED)}) | Optimum off-centre ({len(off)}) |",
                  "|---|---|---|---|"]
    for a in sorted(names, key=r_all.get):
        rank_lines.append(f"| {a} | {r_all[a]:.2f} | {r_cen[a]:.2f} | {r_off[a]:.2f} |")
    rank_lines.append(f"\nFriedman test over all {len(BENCHMARKS)} functions: "
                      f"p = {p_all:.2e} (1 = best rank).")

    with open(os.path.join(OUT, "benchmark_table.md"), "w") as fh:
        fh.write("## Mean final fitness (lower is better)\n\n" + "\n".join(summary)
                 + "\n\n## Mean rank across functions\n\n" + "\n".join(rank_lines)
                 + "\n\n## Full results\n\n" + "\n".join(lines) + "\n")

    # ------------------------------------------- pairwise tests per function
    stat_out = ["# Pairwise Mann-Whitney U tests on final fitness\n",
                "Holm correction is applied within each function "
                f"({len(names) * (len(names) - 1) // 2} pairs).\n"]
    for fname in BENCHMARKS:
        samples = {a: finals[(fname, a)] for a in names}
        stat_out.append(f"## {fname}\n\n{pairwise_table(samples)}\n")
    with open(os.path.join(OUT, "benchmark_stats.md"), "w") as fh:
        fh.write("\n".join(stat_out))

    print("\n".join(summary))
    print("\n" + "\n".join(rank_lines))
    print(f"\nSaved to {OUT}")


if __name__ == "__main__":
    main()
