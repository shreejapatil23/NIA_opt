"""Nature-inspired optimizers (plus two reference baselines) sharing one interface.

Every optimizer MINIMIZES `fitness(x) -> float` over the box [lb, ub]^dim.

Budget. All algorithms get the same number of fitness evaluations
(`max_evals`), not the same number of iterations, because algorithms spend a
different number of evaluations per iteration (e.g. GA re-uses its elites).
Schedules that normally depend on the iteration counter (GWO/WOA `a`, PSO
inertia) use the fraction of the budget spent instead.

`optimize()` returns (best_x, best_f, history) where history[i] is the best
fitness found after i+1 evaluations, so len(history) == max_evals and curves
from different algorithms line up exactly.
"""
import numpy as np


class Optimizer:
    name = "base"

    def __init__(self, pop_size=30, max_evals=None, iters=None, seed=None):
        """Give either `max_evals`, or `iters` (then max_evals = pop_size * (iters + 1),
        i.e. the initial population plus `iters` full generations)."""
        if max_evals is None:
            if iters is None:
                raise ValueError("give max_evals or iters")
            max_evals = pop_size * (iters + 1)
        self.pop_size = pop_size
        self.max_evals = int(max_evals)
        self.rng = np.random.default_rng(seed)

    # -- budget bookkeeping ------------------------------------------------
    def _start(self, fitness):
        self._fitness = fitness
        self._evals = 0
        self._best_x, self._best_f = None, np.inf
        self._trace = []

    def _done(self):
        return self._evals >= self.max_evals

    def _progress(self):
        """Fraction of the evaluation budget used so far, in [0, 1]."""
        return self._evals / self.max_evals

    def _eval(self, pop):
        """Evaluate a population. Individuals beyond the remaining budget are
        not evaluated and get +inf (this only happens in the last generation)."""
        f = np.full(len(pop), np.inf)
        for i, x in enumerate(pop):
            if self._done():
                break
            f[i] = self._fitness(x)
            self._evals += 1
            if f[i] < self._best_f:
                self._best_f, self._best_x = f[i], np.array(x, copy=True)
            self._trace.append(self._best_f)
        return f

    def _result(self):
        return self._best_x, self._best_f, np.array(self._trace)

    def _init_pop(self, dim, lb, ub):
        return self.rng.uniform(lb, ub, size=(self.pop_size, dim))

    def optimize(self, fitness, dim, lb, ub):
        raise NotImplementedError


class RandomSearch(Optimizer):
    """Baseline: sample uniformly at random. Anything worth using must beat this."""
    name = "Random"

    def optimize(self, fitness, dim, lb, ub):
        self._start(fitness)
        while not self._done():
            self._eval(self._init_pop(dim, lb, ub))
        return self._result()


class DE(Optimizer):
    """Reference baseline: Differential Evolution, DE/rand/1/bin
    (Storn & Price, 1997)."""
    name = "DE"

    def __init__(self, *a, F=0.5, CR=0.9, **kw):
        super().__init__(*a, **kw)
        self.F, self.CR = F, CR

    def optimize(self, fitness, dim, lb, ub):
        self._start(fitness)
        rng, n = self.rng, self.pop_size
        x = self._init_pop(dim, lb, ub)
        f = self._eval(x)
        while not self._done():
            trial = np.empty_like(x)
            for i in range(n):
                r1, r2, r3 = rng.choice([j for j in range(n) if j != i], 3, replace=False)
                mutant = x[r1] + self.F * (x[r2] - x[r3])
                cross = rng.random(dim) < self.CR
                cross[rng.integers(dim)] = True          # at least one gene from mutant
                trial[i] = np.clip(np.where(cross, mutant, x[i]), lb, ub)
            tf = self._eval(trial)
            better = tf <= f
            x[better], f[better] = trial[better], tf[better]
        return self._result()


class PSO(Optimizer):
    """Particle Swarm Optimization (inertia-weight variant)."""
    name = "PSO"

    def __init__(self, *a, w_max=0.9, w_min=0.4, c1=1.5, c2=1.5, **kw):
        super().__init__(*a, **kw)
        self.w_max, self.w_min, self.c1, self.c2 = w_max, w_min, c1, c2

    def optimize(self, fitness, dim, lb, ub):
        self._start(fitness)
        rng = self.rng
        x = self._init_pop(dim, lb, ub)
        vmax = 0.2 * (ub - lb)
        v = rng.uniform(-vmax, vmax, size=x.shape)
        f = self._eval(x)
        pbest, pbest_f = x.copy(), f.copy()
        g = np.argmin(f)
        gbest = x[g].copy()
        while not self._done():
            w = self.w_max - (self.w_max - self.w_min) * self._progress()
            r1, r2 = rng.random(x.shape), rng.random(x.shape)
            v = w * v + self.c1 * r1 * (pbest - x) + self.c2 * r2 * (gbest - x)
            v = np.clip(v, -vmax, vmax)
            x = np.clip(x + v, lb, ub)
            f = self._eval(x)
            better = f < pbest_f
            pbest[better], pbest_f[better] = x[better], f[better]
            gbest = pbest[np.argmin(pbest_f)].copy()
        return self._result()


class GA(Optimizer):
    """Real-coded Genetic Algorithm: tournament selection, arithmetic
    crossover, Gaussian mutation, elitism."""
    name = "GA"

    def __init__(self, *a, crossover_rate=0.9, mutation_rate=None,
                 mutation_sigma=0.1, elite=2, tournament=3, **kw):
        super().__init__(*a, **kw)
        self.cr, self.mr = crossover_rate, mutation_rate
        self.sigma, self.elite, self.k = mutation_sigma, elite, tournament

    def _select(self, pop, f):
        idx = self.rng.integers(0, len(pop), size=self.k)
        return pop[idx[np.argmin(f[idx])]]

    def optimize(self, fitness, dim, lb, ub):
        self._start(fitness)
        rng = self.rng
        mr = self.mr if self.mr is not None else 1.0 / dim
        pop = self._init_pop(dim, lb, ub)
        f = self._eval(pop)
        while not self._done():
            order = np.argsort(f)
            elite_pop, elite_f = pop[order[:self.elite]], f[order[:self.elite]]
            children = []
            for _ in range(self.pop_size - self.elite):
                p1, p2 = self._select(pop, f), self._select(pop, f)
                if rng.random() < self.cr:
                    a = rng.random(dim)
                    c = a * p1 + (1 - a) * p2
                else:
                    c = p1.copy()
                mask = rng.random(dim) < mr
                c = c + mask * rng.normal(0, self.sigma * (ub - lb), dim)
                children.append(np.clip(c, lb, ub))
            children = np.array(children)
            cf = self._eval(children)
            pop = np.vstack([elite_pop, children])
            f = np.concatenate([elite_f, cf])
        return self._result()


class GWO(Optimizer):
    """Grey Wolf Optimizer (Mirjalili et al., 2014)."""
    name = "GWO"

    def optimize(self, fitness, dim, lb, ub):
        self._start(fitness)
        rng = self.rng
        x = self._init_pop(dim, lb, ub)
        f = self._eval(x)
        order = np.argsort(f)
        alpha, beta, delta = (x[order[i]].copy() for i in range(3))
        alpha_f = f[order[0]]
        while not self._done():
            a = 2 - 2 * self._progress()
            new_x = np.zeros_like(x)
            for leader in (alpha, beta, delta):
                r1, r2 = rng.random(x.shape), rng.random(x.shape)
                A, C = 2 * a * r1 - a, 2 * r2
                new_x += leader - A * np.abs(C * leader - x)
            x = np.clip(new_x / 3.0, lb, ub)
            f = self._eval(x)
            order = np.argsort(f)
            if f[order[0]] < alpha_f:
                alpha_f = f[order[0]]
                alpha = x[order[0]].copy()
            # update beta/delta from current population (alpha kept as best-so-far)
            beta, delta = x[order[1]].copy(), x[order[2]].copy()
        return self._result()


class WOA(Optimizer):
    """Whale Optimization Algorithm (Mirjalili & Lewis, 2016)."""
    name = "WOA"

    def __init__(self, *a, b=1.0, **kw):
        super().__init__(*a, **kw)
        self.b = b

    def optimize(self, fitness, dim, lb, ub):
        self._start(fitness)
        rng = self.rng
        x = self._init_pop(dim, lb, ub)
        f = self._eval(x)
        i = np.argmin(f)
        best = x[i].copy()
        best_f = f[i]
        while not self._done():
            a = 2 - 2 * self._progress()
            for k in range(self.pop_size):
                A = 2 * a * rng.random() - a           # scalar per whale (as in the paper)
                C = 2 * rng.random()
                if rng.random() < 0.5:
                    if abs(A) < 1:                     # exploit: encircle prey
                        x[k] = best - A * np.abs(C * best - x[k])
                    else:                              # explore: random whale
                        rand = x[rng.integers(0, self.pop_size)]
                        x[k] = rand - A * np.abs(C * rand - x[k])
                else:                                  # spiral bubble-net
                    l = rng.uniform(-1, 1)
                    d = np.abs(best - x[k])
                    x[k] = d * np.exp(self.b * l) * np.cos(2 * np.pi * l) + best
            x = np.clip(x, lb, ub)
            f = self._eval(x)
            i = np.argmin(f)
            if f[i] < best_f:
                best, best_f = x[i].copy(), f[i]
        return self._result()


# The four nature-inspired algorithms being compared ...
ALGORITHMS = {"GA": GA, "PSO": PSO, "GWO": GWO, "WOA": WOA}
# ... and reference baselines run alongside them.
BASELINES = {"Random": RandomSearch, "DE": DE}
ALL = {**ALGORITHMS, **BASELINES}
