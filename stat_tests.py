"""Statistical tests shared by both experiments.

- Pairwise: Mann-Whitney U (= Wilcoxon rank-sum) for independent runs. Unlike
  scipy's `ranksums`, `mannwhitneyu` corrects for ties, which are common here
  (feature-selection fitness only takes a few distinct values).
- Multiple comparisons: Holm-Bonferroni correction across all pairs, so the
  chance of ANY false "significant" result stays below 5%.
- Across problems: Friedman test on per-problem ranks (Demsar, 2006).
"""
import itertools

import numpy as np
from scipy.stats import friedmanchisquare, mannwhitneyu, rankdata


def mann_whitney(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if np.unique(np.concatenate([a, b])).size == 1:   # all identical: no difference
        return 1.0
    p = mannwhitneyu(a, b, alternative="two-sided").pvalue
    return 1.0 if np.isnan(p) else float(p)


def holm(pvalues):
    """Holm-Bonferroni adjusted p-values (same order as the input)."""
    p = np.asarray(pvalues, float)
    m = len(p)
    order = np.argsort(p)
    adj = np.empty(m)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, (m - rank) * p[i])
        adj[i] = min(1.0, running)
    return adj


def pairwise(samples, alpha=0.05):
    """samples: {name: values (lower is better)}.
    Returns rows (a, b, p_raw, p_holm, verdict) for every pair."""
    names = list(samples)
    pairs = list(itertools.combinations(names, 2))
    raw = [mann_whitney(samples[a], samples[b]) for a, b in pairs]
    adj = holm(raw)
    rows = []
    for (a, b), p, q in zip(pairs, raw, adj):
        if q >= alpha:
            verdict = "no difference"
        else:
            winner = a if np.median(samples[a]) < np.median(samples[b]) else b
            verdict = f"{winner} better"
        rows.append((a, b, p, q, verdict))
    return rows


def pairwise_table(samples, alpha=0.05):
    lines = ["| A | B | p (raw) | p (Holm) | Result (alpha=0.05) |",
             "|---|---|---|---|---|"]
    for a, b, p, q, v in pairwise(samples, alpha):
        lines.append(f"| {a} | {b} | {p:.2e} | {q:.2e} | {v} |")
    return "\n".join(lines)


def friedman(scores):
    """scores: {algorithm: [score on problem 1, problem 2, ...]} (lower is better).
    Returns (mean rank per algorithm, Friedman p-value)."""
    names = list(scores)
    m = np.array([scores[n] for n in names], float).T      # problems x algorithms
    # round so values equal to machine precision count as ties
    ranks = np.array([rankdata(np.round(row, 12)) for row in m])
    mean_rank = dict(zip(names, ranks.mean(axis=0)))
    p = friedmanchisquare(*m.T).pvalue
    return mean_rank, float(p)
