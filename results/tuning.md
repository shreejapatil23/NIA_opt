# Parameter tuning

Tuning problems: shifted + sign-flipped functions, dim=10, 3000 evaluations, population 30, 10 runs. Mean final fitness; rank 1 = best within each algorithm.

## GA

| Setting | Sphere | Rastrigin | Ackley | Griewank | Rosenbrock | Schwefel | Mean rank |
|---|---|---|---|---|---|---|---|
| **fixed step 0.1** | 6.76e-01 | 5.48e+00 | 5.13e-01 | 5.72e-01 | 5.24e+01 | 6.30e+02 | 2.17 |
| step 0.1 -> 1e-2 | 5.10e-02 | 1.65e+01 | 6.95e-02 | 3.15e-01 | 2.21e+02 | 1.47e+03 | 2.33 |
| step 0.1 -> 1e-3 | 1.96e-03 | 1.97e+01 | 2.17e-02 | 1.03e-01 | 4.51e+02 | 1.76e+03 | 2.33 |
| step 0.1 -> 1e-4 | 8.08e+01 | 1.65e+01 | 3.70e+00 | 8.25e-02 | 8.94e+02 | 1.89e+03 | 3.17 |

Chosen: **fixed step 0.1**

## PSO

| Setting | Sphere | Rastrigin | Ackley | Griewank | Rosenbrock | Schwefel | Mean rank |
|---|---|---|---|---|---|---|---|
| inertia 0.9->0.4, c=1.5, wall: clip | 1.18e+02 | 1.38e+01 | 1.19e-01 | 1.37e-01 | 4.91e+04 | 1.16e+03 | 3.67 |
| inertia 0.9->0.4, c=1.5, wall: zero | 1.34e-04 | 1.28e+01 | 1.22e-01 | 1.32e-01 | 4.81e+01 | 1.22e+03 | 2.50 |
| **inertia 0.9->0.4, c=1.5, wall: reflect** | 1.02e-04 | 9.30e+00 | 3.50e-01 | 1.20e-01 | 6.23e+01 | 1.03e+03 | 2.17 |
| constriction w=0.7298, c=1.4962, wall: clip | 2.02e+02 | 1.75e+01 | 3.41e-01 | 4.43e-01 | 4.52e+02 | 1.09e+03 | 5.00 |
| constriction w=0.7298, c=1.4962, wall: zero | 5.90e+01 | 1.56e+01 | 1.73e-01 | 4.59e-01 | 1.11e+02 | 1.05e+03 | 3.83 |
| constriction w=0.7298, c=1.4962, wall: reflect | 2.07e-02 | 1.67e+01 | 3.20e-01 | 3.30e-01 | 3.54e+01 | 1.28e+03 | 3.83 |

Chosen: **inertia 0.9->0.4, c=1.5, wall: reflect**

## DE

| Setting | Sphere | Rastrigin | Ackley | Griewank | Rosenbrock | Schwefel | Mean rank |
|---|---|---|---|---|---|---|---|
| **rand/1, F=0.5, CR=0.9** | 4.32e-01 | 3.80e+01 | 5.64e-01 | 7.72e-01 | 7.84e+01 | 1.66e+03 | 1.67 |
| best/1, F=0.5, CR=0.9 | 7.94e+02 | 3.16e+01 | 6.97e+00 | 5.70e+00 | 6.07e+04 | 1.17e+03 | 2.17 |
| current-to-best/1, F=0.5, CR=0.9 | 1.66e+02 | 3.34e+01 | 4.11e+00 | 9.90e-01 | 1.00e+05 | 1.23e+03 | 2.17 |

Chosen: **rand/1, F=0.5, CR=0.9**
