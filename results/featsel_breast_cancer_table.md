Budget: 400 fitness evaluations per run, population 16, 10 runs.

| Method | Fitness (mean±std) | Features used | CV acc | Test acc | Time/run (s) |
|---|---|---|---|---|---|
| All features | 0.0810 | 30 | 0.9674 | 0.9474 | - |
| GA | 0.0350±0.0040 | 11.7±2.2 | 0.9837 | 0.9386±0.0060 | 3.9 |
| PSO | 0.0324±0.0036 | 10.3±2.0 | 0.9840 | 0.9415±0.0101 | 8.6 |
| GWO | 0.0253±0.0042 | 7.6±2.0 | 0.9867 | 0.9386±0.0102 | 8.5 |
| WOA | 0.0419±0.0045 | 11.3±2.2 | 0.9757 | 0.9380±0.0120 | 4.0 |
| Random (baseline) | 0.0385±0.0024 | 10.4±2.5 | 0.9777 | 0.9474±0.0094 | 21.3 |
| DE (baseline) | 0.0286±0.0022 | 9.9±1.5 | 0.9872 | 0.9398±0.0094 | 13.9 |
| Mutual info (top-k) | 0.0484 | 19 | 0.9824 | 0.9532 | 0.6 |
| RFE (logistic) | 0.0250 | 5 | 0.9824 | 0.9474 | 0.7 |
| L1 logistic | 0.0282 | 4 | 0.9773 | 0.9474 | 5.3 |

Mann-Whitney U tests on final fitness (Holm-corrected over all pairs):

| A | B | p (raw) | p (Holm) | Result (alpha=0.05) |
|---|---|---|---|---|
| GA | PSO | 1.04e-01 | 2.08e-01 | no difference |
| GA | GWO | 1.31e-03 | 1.31e-02 | GWO better |
| GA | WOA | 7.28e-03 | 4.37e-02 | GA better |
| GA | Random | 6.40e-02 | 1.92e-01 | no difference |
| GA | DE | 2.20e-03 | 1.76e-02 | DE better |
| PSO | GWO | 3.60e-03 | 2.52e-02 | GWO better |
| PSO | WOA | 1.01e-03 | 1.11e-02 | PSO better |
| PSO | Random | 1.71e-03 | 1.54e-02 | PSO better |
| PSO | DE | 1.91e-02 | 9.53e-02 | no difference |
| GWO | WOA | 3.28e-04 | 4.27e-03 | GWO better |
| GWO | Random | 3.28e-04 | 4.27e-03 | GWO better |
| GWO | DE | 2.32e-02 | 9.53e-02 | no difference |
| WOA | Random | 1.04e-01 | 2.08e-01 | no difference |
| WOA | DE | 1.83e-04 | 2.74e-03 | DE better |
| Random | DE | 1.83e-04 | 2.74e-03 | DE better |
