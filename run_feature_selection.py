"""Experiment 2: feature selection on a real dataset.

Each algorithm (plus the Random Search and DE baselines) is run N_RUNS times
with the same budget of fitness evaluations. We record convergence, subset
size, CV accuracy (used as fitness), held-out test accuracy and run time.
Three classical feature-selection methods are run once each for comparison.
Algorithms are compared with Mann-Whitney U tests, Holm-corrected.
"""
import itertools
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from optimizers import ALGORITHMS, ALL
from problems import FeatureSelection
from stat_tests import pairwise_table

DATASET = sys.argv[1] if len(sys.argv) > 1 else "breast_cancer"
POP = 16
MAX_EVALS = 400           # = 16 individuals x 25 generations
N_RUNS = 10
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
COLORS = {"GA": "#1f77b4", "PSO": "#d62728", "GWO": "#2ca02c", "WOA": "#9467bd",
          "DE": "#ff7f0e", "Random": "#7f7f7f"}


def run_one(args):
    aname, seed = args
    prob = FeatureSelection(DATASET)
    opt = ALL[aname](pop_size=POP, max_evals=MAX_EVALS, seed=seed)
    t0 = time.perf_counter()
    x, f, hist = opt.optimize(prob.fitness, prob.n_features, 0.0, 1.0)
    secs = time.perf_counter() - t0
    mask = prob.decode(x)
    return dict(algo=aname, seed=seed, fitness=f, hist=hist, secs=secs,
                n_sel=int(mask.sum()), cv_acc=prob.accuracy(mask),
                test_acc=prob.test_accuracy(mask), mask=mask)


def main():
    os.makedirs(OUT, exist_ok=True)
    prob = FeatureSelection(DATASET)
    all_mask = np.ones(prob.n_features, dtype=bool)
    base_cv, base_test = prob.accuracy(all_mask), prob.test_accuracy(all_mask)
    print(f"Dataset: {DATASET}  features={prob.n_features}  "
          f"train={len(prob.y)}  test={len(prob.y_test)}")
    print(f"Baseline (all features): CV acc={base_cv:.4f}  test acc={base_test:.4f}\n")

    jobs = list(itertools.product(ALL, range(N_RUNS)))
    with ProcessPoolExecutor() as ex:
        results = list(ex.map(run_one, jobs))
    by_algo = {a: [r for r in results if r["algo"] == a] for a in ALL}
    names = list(ALL)

    # ------------------------------------------------------- results table
    lines = [f"Budget: {MAX_EVALS} fitness evaluations per run, population {POP}, "
             f"{N_RUNS} runs.\n",
             "| Method | Fitness (mean±std) | Features used | CV acc | Test acc | Time/run (s) |",
             "|---|---|---|---|---|---|",
             f"| All features | {prob.mask_fitness(all_mask):.4f} | {prob.n_features} | "
             f"{base_cv:.4f} | {base_test:.4f} | - |"]
    for a, rs in by_algo.items():
        fit = np.array([r["fitness"] for r in rs])
        ns = np.array([r["n_sel"] for r in rs])
        cv = np.array([r["cv_acc"] for r in rs])
        te = np.array([r["test_acc"] for r in rs])
        tm = np.mean([r["secs"] for r in rs])
        label = a if a in ALGORITHMS else f"{a} (baseline)"
        lines.append(f"| {label} | {fit.mean():.4f}±{fit.std():.4f} | "
                     f"{ns.mean():.1f}±{ns.std():.1f} | {cv.mean():.4f} | "
                     f"{te.mean():.4f}±{te.std():.4f} | {tm:.1f} |")

    # classical (deterministic) feature-selection methods: one run each
    for label, method in prob.classical_methods().items():
        t0 = time.perf_counter()
        mask = method()
        secs = time.perf_counter() - t0
        lines.append(f"| {label} | {prob.mask_fitness(mask):.4f} | {int(mask.sum())} | "
                     f"{prob.accuracy(mask):.4f} | {prob.test_accuracy(mask):.4f} | "
                     f"{secs:.1f} |")
    table = "\n".join(lines)

    # ---------------------------------------------------- statistical tests
    stats = pairwise_table({a: [r["fitness"] for r in by_algo[a]] for a in names})
    with open(os.path.join(OUT, f"featsel_{DATASET}_table.md"), "w") as fh:
        fh.write(table + "\n\nMann-Whitney U tests on final fitness "
                 "(Holm-corrected over all pairs):\n\n" + stats + "\n")
    print(table)
    print("\nMann-Whitney U tests on final fitness, Holm-corrected "
          "(lower fitness is better):\n")
    print(stats)

    # most frequently selected features across runs of the four NIA algorithms
    freq = np.mean([r["mask"] for r in results if r["algo"] in ALGORITHMS], axis=0)
    top = np.argsort(freq)[::-1][:8]
    print("\nMost frequently selected features (GA/PSO/GWO/WOA runs):")
    for i in top:
        print(f"  {prob.feature_names[i]:<28s} {freq[i]*100:5.1f}% of runs")

    # ---------------------------------------------------------------- plots
    fig, axes = plt.subplots(1, 3, figsize=(18, 4.4))
    for a, rs in by_algo.items():
        h = np.array([r["hist"] for r in rs])
        m, s = h.mean(0), h.std(0)
        x = np.arange(1, len(m) + 1)
        ls = "--" if a not in ALGORITHMS else "-"
        axes[0].plot(x, m, label=a, color=COLORS[a], lw=2, ls=ls)
        axes[0].fill_between(x, m - s, m + s, color=COLORS[a], alpha=0.12)
    axes[0].set_title("Convergence (mean ± std over runs)")
    axes[0].set_xlabel("Fitness evaluations")
    axes[0].set_ylabel("Best fitness (lower is better)")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    axes[1].boxplot([[r["test_acc"] for r in by_algo[a]] for a in names],
                    tick_labels=names)
    axes[1].axhline(base_test, color="k", ls="--", lw=1, label="all features")
    axes[1].set_title("Held-out test accuracy")
    axes[1].set_ylabel("Accuracy")
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    axes[2].boxplot([[r["n_sel"] for r in by_algo[a]] for a in names],
                    tick_labels=names)
    axes[2].axhline(prob.n_features, color="k", ls="--", lw=1, label="all features")
    axes[2].set_title("Number of features selected")
    axes[2].set_ylabel("Features")
    axes[2].legend()
    axes[2].grid(alpha=0.3)

    fig.tight_layout()
    path = os.path.join(OUT, f"featsel_{DATASET}.png")
    fig.savefig(path, dpi=150)
    print(f"\nSaved plots and tables to {OUT}")


if __name__ == "__main__":
    main()
