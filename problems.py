"""Problems the optimizers are tested on: benchmark functions and
feature selection (plus classical feature-selection baselines)."""
import numpy as np
from sklearn.datasets import load_breast_cancer, load_wine
from sklearn.feature_selection import RFE, mutual_info_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler


# ---------------------------------------------------------------- benchmarks
def sphere(x):
    return float(np.sum(x ** 2))


def rastrigin(x):
    return float(10 * len(x) + np.sum(x ** 2 - 10 * np.cos(2 * np.pi * x)))


def ackley(x):
    d = len(x)
    return float(-20 * np.exp(-0.2 * np.sqrt(np.sum(x ** 2) / d))
                 - np.exp(np.sum(np.cos(2 * np.pi * x)) / d) + 20 + np.e)


def griewank(x):
    i = np.arange(1, len(x) + 1)
    return float(np.sum(x ** 2) / 4000 - np.prod(np.cos(x / np.sqrt(i))) + 1)


def rosenbrock(x):
    """Optimum at (1, ..., 1): a narrow curved valley, not at the centre."""
    return float(np.sum(100 * (x[1:] - x[:-1] ** 2) ** 2 + (x[:-1] - 1) ** 2))


def schwefel(x):
    """Schwefel 2.26. Optimum at x_i = 420.9687, near the EDGE of [-500, 500],
    with the second-best region far away: a direct test of centre bias."""
    return float(418.9828872724338 * len(x) - np.sum(x * np.sin(np.sqrt(np.abs(x)))))


class Shifted:
    """f(x - o): moves the optimum from the origin to a random point o.

    Centre-biased algorithms (GWO, WOA) get no free help from an optimum that
    sits in the middle of the box. The shift is drawn once per (function,
    dimension) from a fixed seed, within 80% of the bounds, so every algorithm
    and every run sees the same problem. A plain class (not a closure) so it can
    be sent to worker processes."""

    def __init__(self, func, lb, ub, seed=0):
        self.func, self.lb, self.ub, self.seed = func, lb, ub, seed
        self._o = {}

    def shift(self, dim):
        if dim not in self._o:
            rng = np.random.default_rng(self.seed)
            self._o[dim] = rng.uniform(0.8 * self.lb, 0.8 * self.ub, dim)
        return self._o[dim]

    def __call__(self, x):
        return self.func(x - self.shift(len(x)))


# name -> (function, lower bound, upper bound). All optima have value 0.
BENCHMARKS = {
    # classic: optimum at the centre of the box
    "Sphere": (sphere, -100.0, 100.0),
    "Rastrigin": (rastrigin, -5.12, 5.12),
    "Ackley": (ackley, -32.0, 32.0),
    "Griewank": (griewank, -600.0, 600.0),
    # optimum away from the centre
    "Rosenbrock": (rosenbrock, -30.0, 30.0),
    "Schwefel": (schwefel, -500.0, 500.0),
    "Shifted Sphere": (Shifted(sphere, -100.0, 100.0, seed=1), -100.0, 100.0),
    "Shifted Rastrigin": (Shifted(rastrigin, -5.12, 5.12, seed=2), -5.12, 5.12),
    "Shifted Ackley": (Shifted(ackley, -32.0, 32.0, seed=3), -32.0, 32.0),
    "Shifted Griewank": (Shifted(griewank, -600.0, 600.0, seed=4), -600.0, 600.0),
}


# --------------------------------------------------------- feature selection
class FeatureSelection:
    """Each solution is a real vector in [0,1]^n_features; features with
    value > 0.5 are selected. Fitness (to MINIMIZE) is

        alpha * (1 - CV accuracy) + (1 - alpha) * (n_selected / n_features)

    so the optimizer trades classification error against subset size."""

    def __init__(self, dataset="breast_cancer", alpha=0.95, k=5, cv=5):
        loader = {"breast_cancer": load_breast_cancer, "wine": load_wine}[dataset]
        data = loader()
        # Hold out 30% of the data. The optimizer only ever sees the training
        # part (via cross-validation); the test part gives an honest final score.
        X_tr, X_te, y_tr, y_te = train_test_split(
            data.data, data.target, test_size=0.3, stratify=data.target,
            random_state=0)
        scaler = StandardScaler().fit(X_tr)
        self.X, self.y = scaler.transform(X_tr), y_tr
        self.X_test, self.y_test = scaler.transform(X_te), y_te
        self.n_features = self.X.shape[1]
        self.feature_names = list(data.feature_names)
        self.alpha, self.k, self.cv = alpha, k, cv
        self._cache = {}

    def accuracy(self, mask):
        """Cross-validated accuracy on the training split (used as fitness)."""
        key = mask.tobytes()
        if key not in self._cache:
            clf = KNeighborsClassifier(n_neighbors=self.k)
            self._cache[key] = cross_val_score(
                clf, self.X[:, mask], self.y, cv=self.cv).mean()
        return self._cache[key]

    def test_accuracy(self, mask):
        """Accuracy on the held-out split (never seen by the optimizer)."""
        clf = KNeighborsClassifier(n_neighbors=self.k)
        clf.fit(self.X[:, mask], self.y)
        return clf.score(self.X_test[:, mask], self.y_test)

    def decode(self, x):
        mask = np.asarray(x) > 0.5
        if not mask.any():                 # never allow an empty subset
            mask[np.argmax(x)] = True
        return mask

    def mask_fitness(self, mask):
        err = 1.0 - self.accuracy(mask)
        return self.alpha * err + (1 - self.alpha) * mask.sum() / self.n_features

    def fitness(self, x):
        return self.mask_fitness(self.decode(x))

    def baseline(self):
        """Accuracy using ALL features, for comparison."""
        return self.accuracy(np.ones(self.n_features, dtype=bool))

    # ------------------------------------------- classical selection methods
    # Each method produces a family of candidate subsets from the training
    # split only; we keep the one with the best value of the SAME fitness the
    # optimizers minimize, so the comparison is like for like.
    def _best_of(self, masks):
        masks = [m for m in masks if m.any()]
        return min(masks, key=self.mask_fitness)

    def _top_k_masks(self, ranking):
        """ranking: feature indices, best first -> masks of the top-k, k = 1..n."""
        masks = []
        for k in range(1, self.n_features + 1):
            m = np.zeros(self.n_features, dtype=bool)
            m[ranking[:k]] = True
            masks.append(m)
        return masks

    def select_mutual_info(self):
        """Filter method: rank features by mutual information with the label."""
        mi = mutual_info_classif(self.X, self.y, random_state=0)
        return self._best_of(self._top_k_masks(np.argsort(mi)[::-1]))

    def select_rfe(self):
        """Wrapper method: recursive feature elimination with logistic regression."""
        rfe = RFE(LogisticRegression(max_iter=5000), n_features_to_select=1).fit(self.X, self.y)
        return self._best_of(self._top_k_masks(np.argsort(rfe.ranking_)))

    def select_l1(self):
        """Embedded method: L1-regularised logistic regression; sweep the
        regularisation strength and keep features with non-zero weight."""
        masks = []
        for C in np.logspace(-3, 1, 25):
            lr = LogisticRegression(l1_ratio=1.0, C=C, solver="saga",
                                    max_iter=20000).fit(self.X, self.y)
            masks.append(np.any(lr.coef_ != 0, axis=0))
        return self._best_of(masks)

    def classical_methods(self):
        return {"Mutual info (top-k)": self.select_mutual_info,
                "RFE (logistic)": self.select_rfe,
                "L1 logistic": self.select_l1}
