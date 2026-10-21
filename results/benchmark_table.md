## Mean final fitness (lower is better)

| Function | GA | PSO | GWO | WOA | Random | DE |
|---|---|---|---|---|---|---|
| Sphere | 5.9e+00 | 7.9e+00 | 1.9e-10 | **4.6e-31** | 4.5e+04 | 5.3e+01 |
| Rastrigin | 2.3e+01 | 6.2e+01 | 3.5e+01 | **1.1e-14** | 3.6e+02 | 2.1e+02 |
| Ackley | 1.3e+00 | 2.9e+00 | 3.9e-06 | **1.0e-14** | 2.0e+01 | 3.8e+00 |
| Griewank | 1.1e+00 | 9.8e-01 | **1.7e-02** | 4.5e-02 | 4.0e+02 | 1.5e+00 |
| Rosenbrock | 3.0e+02 | 4.9e+02 | 2.8e+01 | **2.5e+01** | 1.1e+08 | 2.0e+04 |
| Schwefel | 2.7e+03 | 5.0e+03 | 6.5e+03 | **1.4e+02** | 8.6e+03 | 7.3e+03 |
| Schwefel (sign-flipped) | **2.9e+03** | 5.1e+03 | 7.0e+03 | 8.2e+03 | 8.7e+03 | 7.3e+03 |
| Shifted Sphere | **9.7e+00** | 1.7e+01 | 2.1e+03 | 3.5e+04 | 5.7e+04 | 2.2e+02 |
| Shifted Rastrigin | **4.5e+01** | 9.5e+01 | 1.0e+02 | 3.1e+02 | 3.9e+02 | 2.1e+02 |
| Shifted Ackley | **1.6e+00** | 2.9e+00 | 9.2e+00 | 1.9e+01 | 2.0e+01 | 3.7e+00 |
| Shifted Griewank | 1.1e+00 | **9.9e-01** | 1.6e+01 | 3.2e+02 | 5.2e+02 | 2.2e+00 |

## Mean rank across functions

| Algorithm | Mean rank, all functions | Optimum at centre (4) | Optimum off-centre (7) |
|---|---|---|---|
| GA | 2.09 | 3.00 | 1.57 |
| PSO | 2.82 | 3.75 | 2.29 |
| GWO | 2.91 | 2.00 | 3.43 |
| WOA | 2.91 | 1.25 | 3.86 |
| DE | 4.27 | 5.00 | 3.86 |
| Random | 6.00 | 6.00 | 6.00 |

Friedman test over all 11 functions: p = 7.75e-06 (1 = best rank).

## Full results

Budget: 6000 fitness evaluations per run, dim=30, population 30, 20 runs.

| Function | Algorithm | Mean | Std | Best | Time/run (s) |
|---|---|---|---|---|---|
| Sphere | GA | 5.925e+00 | 2.157e+00 | 2.116e+00 | 0.49 |
| Sphere | PSO | 7.875e+00 | 7.803e+00 | 3.951e-01 | 0.08 |
| Sphere | GWO | 1.893e-10 | 1.572e-10 | 8.583e-12 | 0.10 |
| Sphere | WOA | 4.641e-31 | 1.274e-30 | 1.530e-37 | 0.16 |
| Sphere | Random | 4.485e+04 | 3.284e+03 | 3.768e+04 | 0.05 |
| Sphere | DE | 5.327e+01 | 3.612e+01 | 9.757e+00 | 0.46 |
| Rastrigin | GA | 2.282e+01 | 5.396e+00 | 1.570e+01 | 0.54 |
| Rastrigin | PSO | 6.203e+01 | 2.069e+01 | 2.718e+01 | 0.14 |
| Rastrigin | GWO | 3.500e+01 | 2.327e+01 | 1.657e+01 | 0.14 |
| Rastrigin | WOA | 1.137e-14 | 2.898e-14 | 0.000e+00 | 0.22 |
| Rastrigin | Random | 3.552e+02 | 1.588e+01 | 3.094e+02 | 0.10 |
| Rastrigin | DE | 2.126e+02 | 1.674e+01 | 1.818e+02 | 0.52 |
| Ackley | GA | 1.264e+00 | 4.384e-01 | 6.617e-01 | 0.58 |
| Ackley | PSO | 2.939e+00 | 8.826e-01 | 1.730e+00 | 0.16 |
| Ackley | GWO | 3.923e-06 | 2.089e-06 | 1.266e-06 | 0.19 |
| Ackley | WOA | 1.021e-14 | 6.141e-15 | 3.997e-15 | 0.29 |
| Ackley | Random | 1.997e+01 | 2.096e-01 | 1.956e+01 | 0.16 |
| Ackley | DE | 3.755e+00 | 1.347e+00 | 1.604e+00 | 0.64 |
| Griewank | GA | 1.051e+00 | 2.377e-02 | 9.879e-01 | 0.64 |
| Griewank | PSO | 9.820e-01 | 1.912e-01 | 3.275e-01 | 0.19 |
| Griewank | GWO | 1.712e-02 | 1.475e-02 | 1.086e-10 | 0.20 |
| Griewank | WOA | 4.477e-02 | 1.951e-01 | 0.000e+00 | 0.27 |
| Griewank | Random | 4.047e+02 | 2.956e+01 | 3.401e+02 | 0.15 |
| Griewank | DE | 1.479e+00 | 3.251e-01 | 1.088e+00 | 0.65 |
| Rosenbrock | GA | 2.997e+02 | 1.004e+02 | 1.585e+02 | 0.61 |
| Rosenbrock | PSO | 4.870e+02 | 4.203e+02 | 1.552e+02 | 0.19 |
| Rosenbrock | GWO | 2.766e+01 | 7.308e-01 | 2.690e+01 | 0.20 |
| Rosenbrock | WOA | 2.459e+01 | 9.038e+00 | 4.336e-02 | 0.27 |
| Rosenbrock | Random | 1.144e+08 | 1.848e+07 | 7.559e+07 | 0.13 |
| Rosenbrock | DE | 1.985e+04 | 2.764e+04 | 1.260e+03 | 0.54 |
| Schwefel | GA | 2.721e+03 | 3.844e+02 | 2.167e+03 | 0.58 |
| Schwefel | PSO | 4.950e+03 | 7.440e+02 | 3.301e+03 | 0.10 |
| Schwefel | GWO | 6.546e+03 | 1.299e+03 | 4.909e+03 | 0.12 |
| Schwefel | WOA | 1.358e+02 | 2.240e+02 | 9.425e-08 | 0.19 |
| Schwefel | Random | 8.638e+03 | 4.141e+02 | 7.703e+03 | 0.08 |
| Schwefel | DE | 7.279e+03 | 8.005e+02 | 5.350e+03 | 0.48 |
| Schwefel (sign-flipped) | GA | 2.929e+03 | 4.391e+02 | 2.073e+03 | 0.53 |
| Schwefel (sign-flipped) | PSO | 5.143e+03 | 6.908e+02 | 3.708e+03 | 0.11 |
| Schwefel (sign-flipped) | GWO | 6.974e+03 | 1.065e+03 | 5.797e+03 | 0.13 |
| Schwefel (sign-flipped) | WOA | 8.157e+03 | 8.265e+02 | 6.112e+03 | 0.20 |
| Schwefel (sign-flipped) | Random | 8.684e+03 | 2.920e+02 | 8.049e+03 | 0.09 |
| Schwefel (sign-flipped) | DE | 7.305e+03 | 8.783e+02 | 5.118e+03 | 0.50 |
| Shifted Sphere | GA | 9.732e+00 | 4.475e+00 | 2.448e+00 | 0.50 |
| Shifted Sphere | PSO | 1.712e+01 | 1.537e+01 | 8.042e-01 | 0.09 |
| Shifted Sphere | GWO | 2.109e+03 | 2.179e+03 | 1.023e+02 | 0.11 |
| Shifted Sphere | WOA | 3.498e+04 | 1.017e+04 | 5.678e+02 | 0.19 |
| Shifted Sphere | Random | 5.741e+04 | 1.317e+04 | 3.862e+03 | 0.07 |
| Shifted Sphere | DE | 2.186e+02 | 3.055e+02 | 2.183e+01 | 0.47 |
| Shifted Rastrigin | GA | 4.451e+01 | 1.098e+01 | 2.758e+01 | 0.54 |
| Shifted Rastrigin | PSO | 9.479e+01 | 2.252e+01 | 4.863e+01 | 0.15 |
| Shifted Rastrigin | GWO | 1.037e+02 | 3.910e+01 | 6.619e+01 | 0.16 |
| Shifted Rastrigin | WOA | 3.136e+02 | 4.106e+01 | 1.597e+02 | 0.23 |
| Shifted Rastrigin | Random | 3.949e+02 | 2.394e+01 | 3.319e+02 | 0.12 |
| Shifted Rastrigin | DE | 2.113e+02 | 1.665e+01 | 1.745e+02 | 0.53 |
| Shifted Ackley | GA | 1.619e+00 | 3.637e-01 | 8.775e-01 | 0.60 |
| Shifted Ackley | PSO | 2.906e+00 | 7.264e-01 | 1.799e+00 | 0.17 |
| Shifted Ackley | GWO | 9.167e+00 | 2.913e+00 | 2.512e+00 | 0.23 |
| Shifted Ackley | WOA | 1.887e+01 | 3.515e+00 | 3.613e+00 | 0.30 |
| Shifted Ackley | Random | 1.998e+01 | 1.890e+00 | 1.177e+01 | 0.15 |
| Shifted Ackley | DE | 3.680e+00 | 7.374e-01 | 2.269e+00 | 0.54 |
| Shifted Griewank | GA | 1.089e+00 | 4.774e-02 | 1.032e+00 | 0.60 |
| Shifted Griewank | PSO | 9.871e-01 | 1.560e-01 | 4.894e-01 | 0.18 |
| Shifted Griewank | GWO | 1.593e+01 | 1.943e+01 | 1.295e+00 | 0.19 |
| Shifted Griewank | WOA | 3.153e+02 | 9.312e+01 | 2.171e+00 | 0.26 |
| Shifted Griewank | Random | 5.184e+02 | 1.191e+02 | 3.979e+01 | 0.15 |
| Shifted Griewank | DE | 2.241e+00 | 1.820e+00 | 1.090e+00 | 0.42 |
