## Mean final fitness (lower is better)

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

## Mean rank across functions

| Algorithm | Mean rank, all functions | Optimum at centre (4) | Optimum off-centre (6) |
|---|---|---|---|
| GA | 2.10 | 3.00 | 1.50 |
| GWO | 2.60 | 1.75 | 3.17 |
| WOA | 2.70 | 1.25 | 3.67 |
| PSO | 3.60 | 4.00 | 3.33 |
| DE | 4.00 | 5.00 | 3.33 |
| Random | 6.00 | 6.00 | 6.00 |

Friedman test over all 10 functions: p = 3.12e-05 (1 = best rank).

## Full results

Budget: 6000 fitness evaluations per run, dim=30, population 30, 20 runs.

| Function | Algorithm | Mean | Std | Best | Time/run (s) |
|---|---|---|---|---|---|
| Sphere | GA | 5.925e+00 | 2.157e+00 | 2.116e+00 | 1.07 |
| Sphere | PSO | 1.866e+01 | 3.526e+01 | 1.584e-01 | 0.15 |
| Sphere | GWO | 4.124e-10 | 5.014e-10 | 2.109e-11 | 0.18 |
| Sphere | WOA | 4.641e-31 | 1.274e-30 | 1.530e-37 | 0.31 |
| Sphere | Random | 4.485e+04 | 3.284e+03 | 3.768e+04 | 0.11 |
| Sphere | DE | 5.327e+01 | 3.612e+01 | 9.757e+00 | 1.13 |
| Rastrigin | GA | 2.282e+01 | 5.396e+00 | 1.570e+01 | 1.73 |
| Rastrigin | PSO | 7.979e+01 | 2.715e+01 | 3.831e+01 | 0.52 |
| Rastrigin | GWO | 9.365e+00 | 3.898e+00 | 3.675e+00 | 0.55 |
| Rastrigin | WOA | 1.137e-14 | 2.898e-14 | 0.000e+00 | 0.90 |
| Rastrigin | Random | 3.552e+02 | 1.588e+01 | 3.094e+02 | 0.42 |
| Rastrigin | DE | 2.126e+02 | 1.674e+01 | 1.818e+02 | 2.16 |
| Ackley | GA | 1.264e+00 | 4.384e-01 | 6.617e-01 | 2.22 |
| Ackley | PSO | 2.730e+00 | 8.392e-01 | 1.187e+00 | 0.54 |
| Ackley | GWO | 4.414e-06 | 2.111e-06 | 1.276e-06 | 0.69 |
| Ackley | WOA | 1.021e-14 | 6.141e-15 | 3.997e-15 | 0.79 |
| Ackley | Random | 1.997e+01 | 2.096e-01 | 1.956e+01 | 0.44 |
| Ackley | DE | 3.755e+00 | 1.347e+00 | 1.604e+00 | 1.85 |
| Griewank | GA | 1.051e+00 | 2.377e-02 | 9.879e-01 | 2.04 |
| Griewank | PSO | 1.079e+00 | 3.770e-01 | 5.923e-01 | 0.51 |
| Griewank | GWO | 9.739e-03 | 1.111e-02 | 6.945e-11 | 0.56 |
| Griewank | WOA | 4.477e-02 | 1.951e-01 | 0.000e+00 | 0.84 |
| Griewank | Random | 4.047e+02 | 2.956e+01 | 3.401e+02 | 0.43 |
| Griewank | DE | 1.479e+00 | 3.251e-01 | 1.088e+00 | 0.77 |
| Rosenbrock | GA | 2.997e+02 | 1.004e+02 | 1.585e+02 | 0.61 |
| Rosenbrock | PSO | 9.494e+03 | 2.690e+04 | 1.673e+02 | 0.12 |
| Rosenbrock | GWO | 2.765e+01 | 6.440e-01 | 2.626e+01 | 0.14 |
| Rosenbrock | WOA | 2.459e+01 | 9.038e+00 | 4.336e-02 | 0.19 |
| Rosenbrock | Random | 1.144e+08 | 1.848e+07 | 7.559e+07 | 0.11 |
| Rosenbrock | DE | 1.985e+04 | 2.764e+04 | 1.260e+03 | 0.43 |
| Schwefel | GA | 2.721e+03 | 3.844e+02 | 2.167e+03 | 0.46 |
| Schwefel | PSO | 4.940e+03 | 7.210e+02 | 3.813e+03 | 0.08 |
| Schwefel | GWO | 6.824e+03 | 6.375e+02 | 5.289e+03 | 0.10 |
| Schwefel | WOA | 1.358e+02 | 2.240e+02 | 9.425e-08 | 0.15 |
| Schwefel | Random | 8.638e+03 | 4.141e+02 | 7.703e+03 | 0.06 |
| Schwefel | DE | 7.279e+03 | 8.005e+02 | 5.350e+03 | 0.41 |
| Shifted Sphere | GA | 9.732e+00 | 4.475e+00 | 2.448e+00 | 0.45 |
| Shifted Sphere | PSO | 2.714e+03 | 2.263e+03 | 7.346e+00 | 0.07 |
| Shifted Sphere | GWO | 1.621e+03 | 1.434e+03 | 1.179e+02 | 0.09 |
| Shifted Sphere | WOA | 3.498e+04 | 1.017e+04 | 5.678e+02 | 0.16 |
| Shifted Sphere | Random | 5.741e+04 | 1.317e+04 | 3.862e+03 | 0.05 |
| Shifted Sphere | DE | 2.186e+02 | 3.055e+02 | 2.183e+01 | 0.44 |
| Shifted Rastrigin | GA | 4.451e+01 | 1.098e+01 | 2.758e+01 | 0.49 |
| Shifted Rastrigin | PSO | 9.943e+01 | 2.633e+01 | 5.664e+01 | 0.12 |
| Shifted Rastrigin | GWO | 1.170e+02 | 2.100e+01 | 8.247e+01 | 0.13 |
| Shifted Rastrigin | WOA | 3.136e+02 | 4.106e+01 | 1.597e+02 | 0.19 |
| Shifted Rastrigin | Random | 3.949e+02 | 2.394e+01 | 3.319e+02 | 0.11 |
| Shifted Rastrigin | DE | 2.113e+02 | 1.665e+01 | 1.745e+02 | 0.45 |
| Shifted Ackley | GA | 1.619e+00 | 3.637e-01 | 8.775e-01 | 0.51 |
| Shifted Ackley | PSO | 8.029e+00 | 2.386e+00 | 3.316e+00 | 0.14 |
| Shifted Ackley | GWO | 9.457e+00 | 1.959e+00 | 3.630e+00 | 0.16 |
| Shifted Ackley | WOA | 1.887e+01 | 3.515e+00 | 3.613e+00 | 0.22 |
| Shifted Ackley | Random | 1.998e+01 | 1.890e+00 | 1.177e+01 | 0.13 |
| Shifted Ackley | DE | 3.680e+00 | 7.374e-01 | 2.269e+00 | 0.47 |
| Shifted Griewank | GA | 1.089e+00 | 4.774e-02 | 1.032e+00 | 0.51 |
| Shifted Griewank | PSO | 2.598e+01 | 2.307e+01 | 3.129e-01 | 0.15 |
| Shifted Griewank | GWO | 1.625e+01 | 1.432e+01 | 2.517e+00 | 0.16 |
| Shifted Griewank | WOA | 3.153e+02 | 9.312e+01 | 2.171e+00 | 0.23 |
| Shifted Griewank | Random | 5.184e+02 | 1.191e+02 | 3.979e+01 | 0.13 |
| Shifted Griewank | DE | 2.241e+00 | 1.820e+00 | 1.090e+00 | 0.42 |
