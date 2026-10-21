# Bias diagnostics

dim=30, 6000 evaluations, 10 runs, mean final fitness (all optima = 0). Within each group only the optimum's position changes.

| Problem | GA | PSO | GWO | WOA | Random | DE |
|---|---|---|---|---|---|---|
| Sphere, optimum at centre | 6.7e+00 | 7.9e+00 | 1.6e-10 | 1.2e-32 | 4.4e+04 | 5.6e+01 |
| Sphere, optimum at random point | 9.2e+00 | 1.1e+01 | 1.7e+03 | 3.4e+04 | 5.9e+04 | 2.7e+02 |
| Sphere, optimum at (60,...,60) | 1.5e+01 | 7.7e+00 | 2.4e+03 | 9.5e+00 | 7.3e+04 | 1.0e+02 |
| Schwefel, optimum on diagonal | 2.6e+03 | 5.0e+03 | 6.4e+03 | 1.9e+02 | 8.7e+03 | 7.6e+03 |
| Schwefel, signs flipped | 2.9e+03 | 5.1e+03 | 6.7e+03 | 8.1e+03 | 8.4e+03 | 7.4e+03 |
