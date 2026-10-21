Budget: 400 fitness evaluations per run, population 16, 10 runs.

| Method | Fitness (mean±std) | Features used | CV acc | Test acc | Time/run (s) |
|---|---|---|---|---|---|
| All features | 0.1108 | 13 | 0.9360 | 0.9630 | - |
| GA | 0.0417±0.0110 | 5.9±1.4 | 0.9800 | 0.9685±0.0249 | 1.8 |
| PSO | 0.0424±0.0055 | 5.5±0.8 | 0.9776 | 0.9722±0.0265 | 3.5 |
| GWO | 0.0375±0.0076 | 4.8±0.7 | 0.9800 | 0.9556±0.0170 | 4.2 |
| WOA | 0.0546±0.0130 | 6.3±1.6 | 0.9680 | 0.9611±0.0255 | 1.5 |
| Random (baseline) | 0.0433±0.0042 | 5.5±1.5 | 0.9767 | 0.9648±0.0375 | 13.0 |
| DE (baseline) | 0.0402±0.0059 | 5.5±0.7 | 0.9800 | 0.9704±0.0289 | 4.6 |
| Mutual info (top-k) | 0.0420 | 5 | 0.9760 | 0.9630 | 0.2 |
| RFE (logistic) | 0.0383 | 6 | 0.9840 | 1.0000 | 0.2 |
| L1 logistic | 0.0383 | 6 | 0.9840 | 1.0000 | 0.4 |

Mann-Whitney U tests on final fitness (Holm-corrected over all pairs):

| A | B | p (raw) | p (Holm) | Result (alpha=0.05) |
|---|---|---|---|---|
| GA | PSO | 6.22e-01 | 1.00e+00 | no difference |
| GA | GWO | 4.01e-01 | 1.00e+00 | no difference |
| GA | WOA | 3.40e-02 | 4.08e-01 | no difference |
| GA | Random | 3.06e-01 | 1.00e+00 | no difference |
| GA | DE | 8.20e-01 | 1.00e+00 | no difference |
| PSO | GWO | 1.26e-01 | 1.00e+00 | no difference |
| PSO | WOA | 2.71e-02 | 3.53e-01 | no difference |
| PSO | Random | 5.43e-01 | 1.00e+00 | no difference |
| PSO | DE | 5.39e-01 | 1.00e+00 | no difference |
| GWO | WOA | 3.92e-03 | 5.88e-02 | no difference |
| GWO | Random | 4.83e-02 | 5.32e-01 | no difference |
| GWO | DE | 2.84e-01 | 1.00e+00 | no difference |
| WOA | Random | 7.50e-02 | 7.50e-01 | no difference |
| WOA | DE | 1.22e-02 | 1.71e-01 | no difference |
| Random | DE | 2.24e-01 | 1.00e+00 | no difference |
