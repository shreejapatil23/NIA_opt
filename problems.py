"""Problems the optimizers are tested on: benchmark functions and
feature selection."""
import numpy as np
from sklearn.datasets import load_breast_cancer, load_wine
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


# name -> (function, lower bound, upper bound)
BENCHMARKS = {
    "Sphere": (sphere, -100.0, 100.0),
    "Rastrigin": (rastrigin, -5.12, 5.12),
    "Ackley": (ackley, -32.0, 32.0),
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

    def fitness(self, x):
        mask = self.decode(x)
        err = 1.0 - self.accuracy(mask)
        return self.alpha * err + (1 - self.alpha) * mask.sum() / self.n_features

    def baseline(self):
        """Accuracy using ALL features, for comparison."""
        return self.accuracy(np.ones(self.n_features, dtype=bool))
