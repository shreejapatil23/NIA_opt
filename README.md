# Nature-Inspired Optimizers: A Benchmarking Framework

Compares four nature-inspired algorithms on (1) standard and shifted benchmark
functions and (2) a real machine-learning task, feature selection on the
breast-cancer dataset. Random Search, Differential Evolution and three classical
feature-selection methods are included as baselines.

| Algorithm | Inspiration |
|---|---|
| **GA**  - Genetic Algorithm | Natural selection: selection, crossover, mutation |
| **PSO** - Particle Swarm Optimization | Bird flocking / fish schooling |
| **GWO** - Grey Wolf Optimizer | Wolf-pack hierarchy and hunting |
| **WOA** - Whale Optimization Algorithm | Humpback whale bubble-net hunting |

| Baseline | Why it is there |
|---|---|
| **Random Search** | The floor: an algorithm that can't beat random sampling isn't doing anything |
| **DE** - Differential Evolution (DE/rand/1/bin) | A standard, well-studied evolutionary reference |
| **Mutual info / RFE / L1 logistic** | Classical feature-selection methods (filter, wrapper, embedded): is a metaheuristic even needed? |

## Files

| File | Purpose |
|---|---|
| `optimizers.py` | GA, PSO, GWO, WOA + Random Search and DE, all sharing one interface |
| `problems.py` | Benchmark functions (incl. shifted ones), the feature-selection problem, classical selection methods |
| `stat_tests.py` | Mann-Whitney U tests, Holm correction, Friedman ranks |
| `run_benchmarks.py` | Experiment 1: 10 functions, dim 30, 20 runs each |
| `run_feature_selection.py` | Experiment 2: feature selection (10 runs each, held-out test set) |
| `results/` | Plots and tables produced by the two scripts |

## Run it

```bash
pip install -r requirements.txt
python run_benchmarks.py                       # ~1.5 min on 8 cores
python run_feature_selection.py breast_cancer  # ~1.5 min on 8 cores
python run_feature_selection.py wine           # optional second dataset
```

## Design

**Common interface.** Every optimizer is constructed with `pop_size`,
`max_evals` (or `iters`) and `seed`, and exposes `optimize(fitness, dim, lb, ub)`,
which returns `(best_x, best_fitness, history)`. Adding a new algorithm means
writing one class.

**Equal budgets.** Algorithms are compared on the same number of *fitness
evaluations*, not iterations, because they spend a different number of
evaluations per iteration (GA re-uses its 2 elites, for example). Schedules that
normally depend on the iteration count (GWO/WOA's `a`, PSO's inertia weight)
use the fraction of the budget spent instead. `history[i]` is the best fitness
after `i+1` evaluations, so convergence curves line up exactly, and the
starting population is included. Wall-clock time per run is reported as well.

**Benchmarks.** Sphere, Rastrigin, Ackley and Griewank have their optimum at the
centre of the search box. Rosenbrock (optimum at (1,…,1)), Schwefel (optimum
near the edge) and *shifted* versions of the first four, `f(x − o)` with a fixed
random `o` inside 80% of the bounds, test whether an algorithm still works when
the answer isn't in the middle.

**Feature selection.** A solution is a vector in [0,1]^n_features. Features
with value > 0.5 are selected. Fitness (minimized) is

    0.95 * (1 - CV accuracy) + 0.05 * (features used / total features)

CV accuracy is 5-fold cross-validated k-NN (k=5) on a 70% training split. The
remaining 30% is never seen by the optimizers and gives an honest final score.
The classical methods each produce a ranked family of subsets from the training
split; the subset with the best value of the *same* fitness is kept.

**Statistics.** Each algorithm runs multiple times with different seeds.
- Pairs of algorithms: Mann-Whitney U test (the Wilcoxon rank-sum test for
  independent runs), via `scipy.stats.mannwhitneyu`, which corrects for tied
  values. Ties are common in feature selection.
- Multiple comparisons: Holm-Bonferroni correction over all pairs, so the chance
  of *any* false "significant" result stays below 5%.
- Across functions: mean rank of each algorithm plus a Friedman test.

## Results

### Experiment 1: benchmark functions (dim 30, 6000 evaluations, population 30, 20 runs)

| Function | GA | PSO | GWO | WOA | Random | DE |
|---|---|---|---|---|---|---|
| Sphere | 5.9e+00 | 1.9e+01 | 4.1e-10 | **4.6e-31** | 4.5e+04 | 5.3e+01 |
| Rastrigin | 2.3e+01 | 8.0e+01 | 9.4e+00 | **1.1e-14** | 3.6e+02 | 2.1e+02 |
| Ackley | 1.3e+00 | 2.7e+00 | 4.4e-06 | **1.0e-14** | 2.0e+01 | 3.8e+00 |
| Griewank | 1.1e+00 | 1.1e+00 | **9.7e-03** | 4.5e-02 | 4.0e+02 | 1.5e+00 |
| Rosenbrock | 3.0e+02 | 9.5e+03 | 2.8e+01 | **2.5e+01** | 1.1e+08 | 2.0e+04 |
| Schwefel | 2.7e+03 | 4.9e+03 | 6.8e+03 | **1.4e+02** | 8.6e+03 | 7.3e+03 |
| Shifted Sphere | **9.7e+00** | 2.7e+03 | 1.6e+03 | 3.5e+04 | 5.7e+04 | 2.2e+02 |
| Shifted Rastrigin | **4.5e+01** | 9.9e+01 | 1.2e+02 | 3.1e+02 | 3.9e+02 | 2.1e+02 |
| Shifted Ackley | **1.6e+00** | 8.0e+00 | 9.5e+00 | 1.9e+01 | 2.0e+01 | 3.7e+00 |
| Shifted Griewank | **1.1e+00** | 2.6e+01 | 1.6e+01 | 3.2e+02 | 5.2e+02 | 2.2e+00 |

Mean final fitness, lower is better (all optima are 0).

| Algorithm | Mean rank, all 10 | Optimum at centre (4) | Optimum off-centre (6) |
|---|---|---|---|
| GA | **2.10** | 3.00 | **1.50** |
| GWO | 2.60 | 1.75 | 3.17 |
| WOA | 2.70 | **1.25** | 3.67 |
| PSO | 3.60 | 4.00 | 3.33 |
| DE | 4.00 | 5.00 | 3.33 |
| Random | 6.00 | 6.00 | 6.00 |

Friedman test over all 10 functions: p = 3.1e-05. Std, best and time per run
are in `results/benchmark_table.md`; Holm-corrected pairwise tests for every
function are in `results/benchmark_stats.md`; curves are in
`results/benchmark_convergence.png`.

### Experiment 2: feature selection, breast cancer (400 evaluations, population 16, 10 runs)

| Method | Fitness | Features used (of 30) | CV accuracy | Held-out test accuracy |
|---|---|---|---|---|
| All features | 0.0810 | 30 | 0.967 | 0.947 |
| GA | 0.0350 | 11.7 ± 2.2 | 0.984 | 0.939 ± 0.006 |
| PSO | 0.0343 | 12.3 ± 2.3 | 0.986 | 0.944 ± 0.008 |
| **GWO** | **0.0249** | 7.5 ± 2.2 | 0.987 | 0.939 ± 0.010 |
| WOA | 0.0419 | 11.3 ± 2.2 | 0.976 | 0.938 ± 0.012 |
| Random search | 0.0385 | 10.4 ± 2.5 | 0.978 | 0.947 ± 0.009 |
| DE | 0.0286 | 9.9 ± 1.5 | 0.987 | 0.940 ± 0.009 |
| Mutual info (top-k) | 0.0484 | 19 | 0.982 | 0.953 |
| RFE (logistic) | 0.0250 | 5 | 0.982 | 0.947 |
| L1 logistic | 0.0282 | 4 | 0.977 | 0.947 |

- GWO reaches the best mean fitness. After Holm correction it is significantly
  better than GA, WOA and Random Search, but **not** significantly better than
  PSO (p = 0.052) or DE (p = 0.071).
- GA, PSO and WOA are **not** significantly better than Random Search.
- The features chosen most often were *worst texture* (87.5% of runs) and
  *worst concave points* (82.5%), then *worst perimeter* and *worst radius* (60%).
- On the wine dataset (`results/featsel_wine_table.md`) no pair of algorithms
  differs significantly after correction.

## Findings and caveats (say these in the presentation, they show maturity)

1. **The benchmark win for WOA and GWO is largely centre bias.** On the four
   centred functions WOA ranks first (1.25) and GWO second. Move the same
   functions' optimum away from the centre and WOA drops to 3.67, on Shifted
   Sphere barely better than random search (3.5e4 vs 5.7e4). GA, which has no
   built-in pull toward the origin, wins all four shifted functions. The
   original Sphere/Rastrigin/Ackley results said more about where the test
   functions put their optimum than about the algorithms.
2. **The ranking changes with the problem.** WOA wins the centred benchmarks,
   GA the shifted ones, GWO feature selection. No single algorithm is best
   everywhere (the "no free lunch" idea).
3. **A classical method matches the best metaheuristic on feature selection.**
   RFE with logistic regression reaches the same fitness as GWO (0.0250 vs
   0.0249 on average), with 5 features instead of 7.5, in under a second of
   deterministic computation instead of ~8 s per run. L1-logistic gets 4
   features. On this small dataset the metaheuristics are not needed; their
   case would be stronger on problems where no good ranking method exists.
4. **Selection overfits the cross-validation score.** Every optimizer improves
   CV accuracy (0.967 to about 0.98) but held-out test accuracy is not better
   than using all features (0.947). On 171 test samples one point is about 1-2
   patients, so the honest conclusion is: *far fewer features at about the same
   accuracy*, not *better accuracy*.
5. **PSO and DE are weak at this budget** with standard settings (PSO: inertia
   0.9 to 0.4, c1 = c2 = 1.5; DE: F = 0.5, CR = 0.9). Both converge slowly in
   6000 evaluations in 30 dimensions; parameter tuning would help.
6. **Timings depend on caching.** Fitness values of already-seen feature subsets
   are cached, so algorithms that revisit subsets (GA, WOA) run faster than
   Random Search, which almost never repeats a subset. The evaluation budget,
   not wall time, is the fair comparison.
7. Experiment 2 uses a small budget (10 runs, 400 evaluations) so it finishes in
   minutes. More runs would tighten the statistics; with 10 runs and 15
   comparisons, only large differences survive the Holm correction.

## Presentation outline (10 minutes, 8 slides)

1. **Title and motivation.** Why nature-inspired algorithms? Hard problems
   (non-convex, no gradient) where classical methods struggle.
2. **The four algorithms.** One line of biology each, plus one line on the update
   rule. Use the table at the top of this file.
3. **Framework design.** The common interface and the equal evaluation budget,
   so a fair comparison is possible. Show the `optimize()` signature.
4. **Experiment 1: benchmarks.** Show `benchmark_convergence.png`. WOA and GWO
   win on centred functions; GA wins once the optimum is shifted.
5. **Experiment 2: feature selection.** Explain the encoding (vector in [0,1],
   threshold 0.5) and the fitness formula.
6. **Results.** Show `featsel_breast_cancer.png`: GWO converges fastest and
   selects the fewest features. Compare with Random Search and RFE.
7. **Limitations (findings 1, 3 and 4 above).** Centre bias, classical methods
   are competitive, CV vs held-out accuracy.
8. **Conclusion and future work.** No single winner; next steps are CEC
   benchmark suites, tuned parameters, and multi-objective NSGA-II (accuracy vs
   subset size).

## Likely questions from examiners

- *Why Mann-Whitney and not a t-test?* Final fitness values are not normally
  distributed with so few runs, and the rank-based test makes no normality
  assumption. `mannwhitneyu` is used rather than `ranksums` because it corrects
  for tied values.
- *Why the Holm correction?* With 15 pairwise tests at p < 0.05, you would expect
  some false positives by chance. Holm keeps the overall error rate at 5%.
- *Why compare on evaluations rather than iterations?* Evaluating the fitness is
  the expensive step, and algorithms use different numbers of evaluations per
  iteration.
- *Why shifted functions?* To check whether good results come from the
  algorithm or from the optimum sitting at the centre of the search space.
- *Why a held-out set?* Because the optimizer tunes feature choice directly
  against CV accuracy, which makes CV accuracy optimistic.
- *Why does fitness include a feature-count term?* Without it, nothing stops the
  optimizer from just selecting all features.
- *How do the algorithms balance exploration and exploitation?* GWO and WOA shrink
  a coefficient `a` from 2 to 0 over the run (explore first, exploit later); PSO
  decreases its inertia weight; GA relies on mutation rate and elitism.
