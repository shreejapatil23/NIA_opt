Budget: 400 fitness evaluations per run, population 16, 10 runs.

| Method | Fitness (mean±std) | Features used | CV acc | Test acc | Time/run (s) |
|---|---|---|---|---|---|
| All features | 0.0810 | 30 | 0.9674 | 0.9474 | - |
| GA | 0.0350±0.0040 | 11.7±2.2 | 0.9837 | 0.9386±0.0060 | 3.8 |
| PSO | 0.0343±0.0062 | 12.3±2.3 | 0.9855 | 0.9444±0.0075 | 9.0 |
| GWO | 0.0249±0.0027 | 7.5±2.2 | 0.9870 | 0.9386±0.0102 | 7.7 |
| WOA | 0.0419±0.0045 | 11.3±2.2 | 0.9757 | 0.9380±0.0120 | 3.7 |
| Random (baseline) | 0.0385±0.0024 | 10.4±2.5 | 0.9777 | 0.9474±0.0094 | 21.2 |
| DE (baseline) | 0.0286±0.0022 | 9.9±1.5 | 0.9872 | 0.9398±0.0094 | 14.4 |
| Mutual info (top-k) | 0.0484 | 19 | 0.9824 | 0.9532 | 0.6 |
| RFE (logistic) | 0.0250 | 5 | 0.9824 | 0.9474 | 0.6 |
| L1 logistic | 0.0282 | 4 | 0.9773 | 0.9474 | 5.4 |

Mann-Whitney U tests on final fitness (Holm-corrected over all pairs):

| A | B | p (raw) | p (Holm) | Result (alpha=0.05) |
|---|---|---|---|---|
| GA | PSO | 1.00e+00 | 1.00e+00 | no difference |
| GA | GWO | 7.69e-04 | 8.45e-03 | GWO better |
| GA | WOA | 7.28e-03 | 5.83e-02 | no difference |
| GA | Random | 6.40e-02 | 2.56e-01 | no difference |
| GA | DE | 2.20e-03 | 2.20e-02 | DE better |
| PSO | GWO | 5.78e-03 | 5.20e-02 | no difference |
| PSO | WOA | 1.40e-02 | 8.39e-02 | no difference |
| PSO | Random | 1.62e-01 | 3.24e-01 | no difference |
| PSO | DE | 2.11e-02 | 1.05e-01 | no difference |
| GWO | WOA | 1.83e-04 | 2.74e-03 | GWO better |
| GWO | Random | 1.83e-04 | 2.74e-03 | GWO better |
| GWO | DE | 1.01e-02 | 7.10e-02 | no difference |
| WOA | Random | 1.04e-01 | 3.12e-01 | no difference |
| WOA | DE | 1.83e-04 | 2.74e-03 | DE better |
| Random | DE | 1.83e-04 | 2.74e-03 | DE better |
