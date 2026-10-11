"""Four nature-inspired optimizers sharing one interface.

Every optimizer MINIMIZES `fitness(x) -> float` over the box [lb, ub]^dim and
returns (best_x, best_f, history) where history[i] is the best fitness found
after iteration i (used for convergence plots).
"""
import numpy as np


class Optimizer:
    name = "base"

    def __init__(self, pop_size=30, iters=100, seed=None):
        self.pop_size = pop_size
        self.iters = iters
        self.rng = np.random.default_rng(seed)

    # -- helpers ---------------------------------------------------------
    def _init_pop(self, dim, lb, ub):
        return self.rng.uniform(lb, ub, size=(self.pop_size, dim))

    @staticmethod
    def _eval(fitness, pop):
        return np.array([fitness(x) for x in pop])

    def optimize(self, fitness, dim, lb, ub):
        raise NotImplementedError


class PSO(Optimizer):
    """Particle Swarm Optimization (inertia-weight variant)."""
    name = "PSO"

    def __init__(self, *a, w_max=0.9, w_min=0.4, c1=1.5, c2=1.5, **kw):
        super().__init__(*a, **kw)
        self.w_max, self.w_min, self.c1, self.c2 = w_max, w_min, c1, c2

    def optimize(self, fitness, dim, lb, ub):
        rng = self.rng
        x = self._init_pop(dim, lb, ub)
        vmax = 0.2 * (ub - lb)
        v = rng.uniform(-vmax, vmax, size=x.shape)
        f = self._eval(fitness, x)
        pbest, pbest_f = x.copy(), f.copy()
        g = np.argmin(f)
        gbest, gbest_f = x[g].copy(), f[g]
        history = []
        for t in range(self.iters):
            w = self.w_max - (self.w_max - self.w_min) * t / max(1, self.iters - 1)
            r1, r2 = rng.random(x.shape), rng.random(x.shape)
            v = w * v + self.c1 * r1 * (pbest - x) + self.c2 * r2 * (gbest - x)
            v = np.clip(v, -vmax, vmax)
            x = np.clip(x + v, lb, ub)
            f = self._eval(fitness, x)
            better = f < pbest_f
            pbest[better], pbest_f[better] = x[better], f[better]
            g = np.argmin(pbest_f)
            if pbest_f[g] < gbest_f:
                gbest, gbest_f = pbest[g].copy(), pbest_f[g]
            history.append(gbest_f)
        return gbest, gbest_f, np.array(history)


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
        rng = self.rng
        mr = self.mr if self.mr is not None else 1.0 / dim
        pop = self._init_pop(dim, lb, ub)
        f = self._eval(fitness, pop)
        best_i = np.argmin(f)
        best, best_f = pop[best_i].copy(), f[best_i]
        history = []
        for _ in range(self.iters):
            order = np.argsort(f)
            new_pop = [pop[i].copy() for i in order[:self.elite]]
            new_f = [f[i] for i in order[:self.elite]]
            children = []
            while len(new_pop) + len(children) < self.pop_size:
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
            if len(children):
                cf = self._eval(fitness, children)
                new_pop.extend(children)
                new_f.extend(cf)
            pop, f = np.array(new_pop), np.array(new_f)
            i = np.argmin(f)
            if f[i] < best_f:
                best, best_f = pop[i].copy(), f[i]
            history.append(best_f)
        return best, best_f, np.array(history)


class GWO(Optimizer):
    """Grey Wolf Optimizer (Mirjalili et al., 2014)."""
    name = "GWO"

    def optimize(self, fitness, dim, lb, ub):
        rng = self.rng
        x = self._init_pop(dim, lb, ub)
        f = self._eval(fitness, x)
        order = np.argsort(f)
        alpha, beta, delta = (x[order[i]].copy() for i in range(3))
        alpha_f = f[order[0]]
        history = []
        for t in range(self.iters):
            a = 2 - 2 * t / self.iters
            new_x = np.zeros_like(x)
            for leader in (alpha, beta, delta):
                r1, r2 = rng.random(x.shape), rng.random(x.shape)
                A, C = 2 * a * r1 - a, 2 * r2
                new_x += leader - A * np.abs(C * leader - x)
            x = np.clip(new_x / 3.0, lb, ub)
            f = self._eval(fitness, x)
            order = np.argsort(f)
            if f[order[0]] < alpha_f:
                alpha_f = f[order[0]]
                alpha = x[order[0]].copy()
            # update beta/delta from current population (alpha kept as best-so-far)
            beta, delta = x[order[1]].copy(), x[order[2]].copy()
            history.append(alpha_f)
        return alpha, alpha_f, np.array(history)


class WOA(Optimizer):
    """Whale Optimization Algorithm (Mirjalili & Lewis, 2016)."""
    name = "WOA"

    def __init__(self, *a, b=1.0, **kw):
        super().__init__(*a, **kw)
        self.b = b

    def optimize(self, fitness, dim, lb, ub):
        rng = self.rng
        x = self._init_pop(dim, lb, ub)
        f = self._eval(fitness, x)
        i = np.argmin(f)
        best, best_f = x[i].copy(), f[i]
        history = []
        for t in range(self.iters):
            a = 2 - 2 * t / self.iters
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
            f = self._eval(fitness, x)
            i = np.argmin(f)
            if f[i] < best_f:
                best, best_f = x[i].copy(), f[i]
            history.append(best_f)
        return best, best_f, np.array(history)


ALGORITHMS = {"GA": GA, "PSO": PSO, "GWO": GWO, "WOA": WOA}
