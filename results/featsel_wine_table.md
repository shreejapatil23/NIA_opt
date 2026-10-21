Budget: 400 fitness evaluations per run, population 16, 10 runs.

| Method | Fitness (mean±std) | Features used | CV acc | Test acc | Time/run (s) |
|---|---|---|---|---|---|
| All features | 0.1108 | 13 | 0.9360 | 0.9630 | - |
| GA | 0.0417±0.0110 | 5.9±1.4 | 0.9800 | 0.9685±0.0249 | 1.4 |
| PSO | 0.0398±0.0046 | 5.2±0.7 | 0.9792 | 0.9741±0.0277 | 2.7 |
| GWO | 0.0348±0.0055 | 5.3±0.9 | 0.9848 | 0.9648±0.0241 | 3.2 |
| WOA | 0.0546±0.0130 | 6.3±1.6 | 0.9680 | 0.9611±0.0255 | 1.2 |
| Random (baseline) | 0.0433±0.0042 | 5.5±1.5 | 0.9767 | 0.9648±0.0375 | 11.5 |
| DE (baseline) | 0.0402±0.0059 | 5.5±0.7 | 0.9800 | 0.9704±0.0289 | 5.0 |
| Mutual info (top-k) | 0.0420 | 5 | 0.9760 | 0.9630 | 0.2 |
| RFE (logistic) | 0.0383 | 6 | 0.9840 | 1.0000 | 0.2 |
| L1 logistic | 0.0383 | 6 | 0.9840 | 1.0000 | 0.4 |

Mann-Whitney U tests on final fitness (Holm-corrected over all pairs):

| A | B | p (raw) | p (Holm) | Result (alpha=0.05) |
|---|---|---|---|---|
| GA | PSO | 9.39e-01 | 1.00e+00 | no difference |
| GA | GWO | 2.67e-01 | 1.00e+00 | no difference |
| GA | WOA | 3.40e-02 | 3.74e-01 | no difference |
| GA | Random | 3.06e-01 | 1.00e+00 | no difference |
| GA | DE | 8.20e-01 | 1.00e+00 | no difference |
| PSO | GWO | 8.50e-02 | 6.80e-01 | no difference |
| PSO | WOA | 6.94e-03 | 9.02e-02 | no difference |
| PSO | Random | 8.69e-02 | 6.80e-01 | no difference |
| PSO | DE | 8.18e-01 | 1.00e+00 | no difference |
| GWO | WOA | 1.08e-03 | 1.63e-02 | GWO better |
| GWO | Random | 4.91e-03 | 6.87e-02 | no difference |
| GWO | DE | 5.42e-02 | 5.42e-01 | no difference |
| WOA | Random | 7.50e-02 | 6.75e-01 | no difference |
| WOA | DE | 1.22e-02 | 1.47e-01 | no difference |
| Random | DE | 2.24e-01 | 1.00e+00 | no difference |
