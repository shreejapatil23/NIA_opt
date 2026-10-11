"""Experiment 2: feature selection on a real dataset.

Each algorithm is run N_RUNS times (different seeds) in parallel. We record
convergence, the subset size found, CV accuracy (used as fitness) and accuracy
on a held-out test split. A Wilcoxon rank-sum test compares algorithms.
"""
import os
import sys
import itertools
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import ranksums

from optimizers import ALGORITHMS
from problems import FeatureSelection

DATASET = sys.argv[1] if len(sys.argv) > 1 else "breast_cancer"
POP = 16
ITERS = 25
N_RUNS = 10
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(OUT, exist_ok=True)
COLORS = {"GA": "#1f77b4", "PSO": "#d62728", "GWO": "#2ca02c", "WOA": "#9467bd"}


def run_one(args):
    aname, seed = args
    prob = FeatureSelection(DATASET)
    opt = ALGORITHMS[aname](pop_size=POP, iters=ITERS, seed=seed)
    x, f, hist = opt.optimize(prob.fitness, prob.n_features, 0.0, 1.0)
    mask = prob.decode(x)
    return dict(algo=aname, seed=seed, fitness=f, hist=hist,
                n_sel=int(mask.sum()), cv_acc=prob.accuracy(mask),
                test_acc=prob.test_accuracy(mask), mask=mask)


def main():
    prob = FeatureSelection(DATASET)
    all_mask = np.ones(prob.n_features, dtype=bool)
    base_cv, base_test = prob.accuracy(all_mask), prob.test_accuracy(all_mask)
    print(f"Dataset: {DATASET}  features={prob.n_features}  "
          f"train={len(prob.y)}  test={len(prob.y_test)}")
    print(f"Baseline (all features): CV acc={base_cv:.4f}  test acc={base_test:.4f}\n")

    jobs = list(itertools.product(ALGORITHMS, range(N_RUNS)))
    with ProcessPoolExecutor() as ex:
        results = list(ex.map(run_one, jobs))

    by_algo = {a: [r for r in results if r["algo"] == a] for a in ALGORITHMS}

    # ------------------------------------------------------- results table
    lines = ["| Algorithm | Fitness (mean±std) | Features used | CV acc | Test acc |",
             "|---|---|---|---|---|",
             f"| All features | - | {prob.n_features} | {base_cv:.4f} | {base_test:.4f} |"]
    for a, rs in by_algo.items():
        fit = np.array([r["fitness"] for r in rs])
        ns = np.array([r["n_sel"] for r in rs])
        cv = np.array([r["cv_acc"] for r in rs])
        te = np.array([r["test_acc"] for r in rs])
        lines.append(f"| {a} | {fit.mean():.4f}±{fit.std():.4f} | "
                     f"{ns.mean():.1f}±{ns.std():.1f} | {cv.mean():.4f} | "
                     f"{te.mean():.4f}±{te.std():.4f} |")
    table = "\n".join(lines)

    # ---------------------------------------------------- statistical tests
    names = list(ALGORITHMS)
    stat_lines = ["| A | B | p-value | Significant (p<0.05) |", "|---|---|---|---|"]
    for a, b in itertools.combinations(names, 2):
        fa = [r["fitness"] for r in by_algo[a]]
        fb = [r["fitness"] for r in by_algo[b]]
        p = ranksums(fa, fb).pvalue
        stat_lines.append(f"| {a} | {b} | {p:.4f} | {'yes' if p < 0.05 else 'no'} |")
    stats = "\n".join(stat_lines)

    with open(os.path.join(OUT, f"featsel_{DATASET}_table.md"), "w") as fh:
        fh.write(table + "\n\nWilcoxon rank-sum test on final fitness:\n\n" + stats + "\n")
    print(table)
    print("\nWilcoxon rank-sum test on final fitness (lower fitness is better):\n")
    print(stats)

    # most frequently selected features across all runs
    freq = np.mean([r["mask"] for r in results], axis=0)
    top = np.argsort(freq)[::-1][:8]
    print("\nMost frequently selected features:")
    for i in top:
        print(f"  {prob.feature_names[i]:<28s} {freq[i]*100:5.1f}% of runs")

    # ---------------------------------------------------------------- plots
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.2))
    for a, rs in by_algo.items():
        h = np.array([r["hist"] for r in rs])
        m, s = h.mean(0), h.std(0)
        x = np.arange(1, len(m) + 1)
        axes[0].plot(x, m, label=a, color=COLORS[a], lw=2)
        axes[0].fill_between(x, m - s, m + s, color=COLORS[a], alpha=0.15)
    axes[0].set_title("Convergence (mean ± std over runs)")
    axes[0].set_xlabel("Iteration")
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
