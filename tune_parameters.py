"""Choose parameter settings for GA, PSO and DE on separate TUNING problems.

Tuning on the same functions used to report results would flatter whichever
algorithm we tuned most. So the candidates are compared on different problems:
dimension 10 (not 30), different shift vectors, random sign flips, and a
smaller budget. The winner for each algorithm (best mean rank across the tuning
problems) becomes its default in optimizers.py.

GWO and WOA have no free parameters in their standard form (WOA's spiral
constant b = 1 is fixed in the paper), so they are not tuned.

Output: results/tuning.md
"""
import itertools
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np
from scipy.stats import rankdata

from optimizers import DE, GA, PSO
from problems import (Shifted, SignFlipped, ackley, griewank, rastrigin,
                      rosenbrock, schwefel, sphere)

DIM = 10
POP = 30
MAX_EVALS = 3000
N_RUNS = 10
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

# Different seeds from the benchmark set in problems.py (which uses 1-5).
TUNING_PROBLEMS = {
    "Sphere": (SignFlipped(Shifted(sphere, -100, 100, seed=101), seed=201), -100.0, 100.0),
    "Rastrigin": (SignFlipped(Shifted(rastrigin, -5.12, 5.12, seed=102), seed=202), -5.12, 5.12),
    "Ackley": (SignFlipped(Shifted(ackley, -32, 32, seed=103), seed=203), -32.0, 32.0),
    "Griewank": (SignFlipped(Shifted(griewank, -600, 600, seed=104), seed=204), -600.0, 600.0),
    "Rosenbrock": (SignFlipped(Shifted(rosenbrock, -30, 30, seed=105), seed=205), -30.0, 30.0),
    "Schwefel": (SignFlipped(schwefel, seed=206), -500.0, 500.0),
}

CANDIDATES = {
    "GA": {
        "fixed step 0.1": (GA, dict(sigma_final=None)),
        "step 0.1 -> 1e-2": (GA, dict(sigma_final=1e-2)),
        "step 0.1 -> 1e-3": (GA, dict(sigma_final=1e-3)),
        "step 0.1 -> 1e-4": (GA, dict(sigma_final=1e-4)),
    },
    "PSO": {
        f"{name}, wall: {b}": (PSO, dict(boundary=b, **kw))
        for (name, kw), b in itertools.product(
            [("inertia 0.9->0.4, c=1.5", dict(w_max=0.9, w_min=0.4, c1=1.5, c2=1.5)),
             ("constriction w=0.7298, c=1.4962", dict(w_max=0.7298, w_min=0.7298,
                                                      c1=1.49618, c2=1.49618))],
            PSO.BOUNDARIES)
    },
    "DE": {
        "rand/1, F=0.5, CR=0.9": (DE, dict(strategy="rand/1")),
        "best/1, F=0.5, CR=0.9": (DE, dict(strategy="best/1")),
        "current-to-best/1, F=0.5, CR=0.9": (DE, dict(strategy="current-to-best/1")),
    },
}


def run_one(job):
    algo, label, pname, seed = job
    cls, kw = CANDIDATES[algo][label]
    func, lb, ub = TUNING_PROBLEMS[pname]
    _, f, _ = cls(pop_size=POP, max_evals=MAX_EVALS, seed=seed, **kw).optimize(func, DIM, lb, ub)
    return algo, label, pname, f


def main():
    os.makedirs(OUT, exist_ok=True)
    jobs = [(a, l, p, s) for a in CANDIDATES for l in CANDIDATES[a]
            for p, s in itertools.product(TUNING_PROBLEMS, range(N_RUNS))]
    with ProcessPoolExecutor() as ex:
        res = list(ex.map(run_one, jobs, chunksize=8))
    mean = {}
    for a, l, p, f in res:
        mean.setdefault((a, l, p), []).append(f)
    mean = {k: np.mean(v) for k, v in mean.items()}

    out = [f"# Parameter tuning\n\nTuning problems: shifted + sign-flipped functions, "
           f"dim={DIM}, {MAX_EVALS} evaluations, population {POP}, {N_RUNS} runs. "
           "Mean final fitness; rank 1 = best within each algorithm.\n"]
    for a, cands in CANDIDATES.items():
        labels = list(cands)
        ranks = np.array([rankdata([mean[(a, l, p)] for l in labels])
                          for p in TUNING_PROBLEMS])
        mean_rank = ranks.mean(axis=0)
        winner = labels[int(np.argmin(mean_rank))]
        out.append(f"## {a}\n")
        out.append("| Setting | " + " | ".join(TUNING_PROBLEMS) + " | Mean rank |")
        out.append("|---|" + "---|" * (len(TUNING_PROBLEMS) + 1))
        for j, l in enumerate(labels):
            cells = [f"{mean[(a, l, p)]:.2e}" for p in TUNING_PROBLEMS]
            name = f"**{l}**" if l == winner else l
            out.append(f"| {name} | " + " | ".join(cells) + f" | {mean_rank[j]:.2f} |")
        out.append(f"\nChosen: **{winner}**\n")
    text = "\n".join(out)
    with open(os.path.join(OUT, "tuning.md"), "w") as fh:
        fh.write(text)
    print(text)


if __name__ == "__main__":
    main()
