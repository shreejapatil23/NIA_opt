# Nature-Inspired Optimizers: A Benchmarking Framework

Compares four nature-inspired algorithms on (1) standard benchmark functions and
(2) a real machine-learning task, feature selection on the breast-cancer dataset.

| Algorithm | Inspiration |
|---|---|
| **GA**  - Genetic Algorithm | Natural selection: selection, crossover, mutation |
| **PSO** - Particle Swarm Optimization | Bird flocking / fish schooling |
| **GWO** - Grey Wolf Optimizer | Wolf-pack hierarchy and hunting |
| **WOA** - Whale Optimization Algorithm | Humpback whale bubble-net hunting |

## Files

| File | Purpose |
|---|---|
| `optimizers.py` | The four algorithms, all sharing one interface |
| `problems.py` | Benchmark functions + the feature-selection problem |
| `run_benchmarks.py` | Experiment 1: Sphere, Rastrigin, Ackley (dim 30, 20 runs each) |
| `run_feature_selection.py` | Experiment 2: feature selection (10 runs each, held-out test set) |
| `results/` | Plots and tables produced by the two scripts |

## Run it

```bash
pip install numpy scipy scikit-learn matplotlib
python run_benchmarks.py                     # ~35 s
python run_feature_selection.py breast_cancer  # ~3 min on 2 cores
python run_feature_selection.py wine           # optional second dataset
```

## Design

**Common interface.** Every optimizer is constructed with `pop_size`, `iters`,
`seed` and exposes `optimize(fitness, dim, lb, ub)`, which returns
`(best_x, best_fitness, history)`. `history` is the best fitness after each
iteration and is what the convergence plots use. Adding a new algorithm means
writing one class.

**Feature selection.** A solution is a vector in [0,1]^30. Features with value
> 0.5 are selected. Fitness (minimized) is

    0.95 * (1 - CV accuracy) + 0.05 * (features used / total features)

CV accuracy is 5-fold cross-validated k-NN (k=5) on a 70% training split. The
remaining 30% is never seen by the optimizers and gives an honest final score.

**Statistics.** Each algorithm runs multiple times with different seeds.
Algorithms are compared with a Wilcoxon rank-sum test (independent runs).

## Results

### Experiment 1: benchmark functions (dim=30, 200 iterations, population 30, 20 runs)

| Function | GA | PSO | GWO | WOA |
|---|---|---|---|---|
| Sphere | 7.2e+00 | 1.2e+01 | 4.2e-10 | **6.6e-30** |
| Rastrigin | 2.5e+01 | 7.8e+01 | 1.1e+01 | **2.8e-15** |
| Ackley | 1.4e+00 | 2.6e+00 | 3.1e-06 | **1.3e-14** |

Mean final fitness, lower is better. Full table with std and best in
`results/benchmark_table.md`; curves in `results/benchmark_convergence.png`.

### Experiment 2: feature selection, breast cancer (10 runs, population 16, 25 iterations)

| Algorithm | Features used (of 30) | CV accuracy | Held-out test accuracy |
|---|---|---|---|
| All features | 30 | 0.967 | 0.947 |
| GA | 11.8 ± 2.3 | 0.984 | 0.939 ± 0.006 |
| PSO | 11.7 ± 2.9 | 0.984 | 0.942 ± 0.007 |
| **GWO** | **7.3 ± 1.6** | 0.986 | 0.936 ± 0.008 |
| WOA | 11.0 ± 2.8 | 0.975 | 0.937 ± 0.010 |

- GWO reaches the best fitness, and the difference from every other algorithm is
  statistically significant (p < 0.005). GA and PSO are statistically
  indistinguishable (p = 0.97). WOA is the worst here.
- GWO uses about 75% fewer features than the full set.
- The features chosen most often were *worst concave points* and
  *worst texture* (87.5% of runs), then *worst perimeter* (67.5%).

## Findings and caveats (say these in the presentation, they show maturity)

1. **The ranking changes with the problem.** WOA wins on the benchmark
   functions but is worst at feature selection, where GWO wins. No single
   algorithm is best everywhere (the "no free lunch" idea).
2. **Benchmark results flatter some algorithms.** Sphere, Rastrigin and Ackley
   all have their optimum at the origin, which is the centre of the search
   space. WOA and GWO are known to be biased toward the centre, so the near-zero
   WOA scores partly reflect the test functions, not just the algorithm. A shifted
   or rotated benchmark would be a fairer test (future work).
3. **Selection overfits the cross-validation score.** Every algorithm improves CV
   accuracy (0.967 to about 0.98) but the held-out test accuracy is about 1 point
   *lower* than using all features (0.947). On 171 test samples that is
   roughly 1-2 patients, so the honest conclusion is: *far fewer features at
   about the same accuracy*, not *better accuracy*.
4. **PSO is the weakest on the benchmark functions** with the standard
   settings used here (inertia weight 0.9 to 0.4, c1 = c2 = 1.5). It converges
   but slowly within 200 iterations; parameter tuning would help. My first PSO
   attempt used c1 = c2 = 2, which is unstable for much of the run, and I fixed
   that before the final results.
5. Experiment 2 uses a small budget (10 runs, 25 iterations) so it
   finishes in minutes. More runs and iterations would tighten the statistics.

## Presentation outline (10 minutes, 8 slides)

1. **Title and motivation.** Why nature-inspired algorithms? Hard problems
   (non-convex, no gradient) where classical methods struggle.
2. **The four algorithms.** One line of biology each, plus one line on the update
   rule. Use the table at the top of this file.
3. **Framework design.** The common interface, so a fair comparison is possible.
   Show the `optimize()` signature.
4. **Experiment 1: benchmarks.** Show `benchmark_convergence.png`. WOA and GWO
   converge fastest; GA and PSO are slower.
5. **Experiment 2: feature selection.** Explain the encoding (vector in [0,1],
   threshold 0.5) and the fitness formula.
6. **Results.** Show `featsel_breast_cancer.png`: GWO converges fastest and
   selects the fewest features. Mention the p-values.
7. **Limitations (caveats 2 and 3 above).** Centre bias, and CV vs held-out accuracy.
8. **Conclusion and future work.** No single winner; next steps are shifted
   benchmarks, Differential Evolution, and multi-objective NSGA-II (accuracy vs
   subset size).

## Likely questions from examiners

- *Why Wilcoxon and not a t-test?* Final fitness values are not normally
  distributed with so few runs, and the rank-sum test makes no normality assumption.
- *Why a held-out set?* Because the optimizer tunes feature choice directly
  against CV accuracy, which makes CV accuracy optimistic.
- *Why does fitness include a feature-count term?* Without it, nothing stops the
  optimizer from just selecting all features.
- *How do the algorithms balance exploration and exploitation?* GWO and WOA shrink
  a coefficient `a` from 2 to 0 over the run (explore first, exploit later); PSO
  decreases its inertia weight; GA relies on mutation rate and elitism.
