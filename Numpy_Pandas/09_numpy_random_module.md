# 09. The Random Module

Random sampling is everywhere in data science: train/test splitting, bootstrapping, Monte Carlo simulation, initializing model weights, generating synthetic data for testing, and stochastic algorithms like SGD.

## The Modern API: `Generator` (Preferred over legacy `np.random.seed`)

```python
import numpy as np

rng = np.random.default_rng(seed=42)   # create a reproducible random Generator
```

**Why use `default_rng` instead of `np.random.seed()`?** The old global-state API (`np.random.seed(42)` followed by `np.random.rand()`) is considered legacy. It mutates global state, which causes hard-to-debug issues in larger codebases (e.g., one function accidentally consuming randomness meant for another). The `Generator` API (`default_rng`) is self-contained, faster, and is the officially recommended approach since NumPy 1.17+.

```python
# Legacy (still common in older code/tutorials, still works, but avoid in new code)
np.random.seed(42)
np.random.rand(3)

# Modern (preferred)
rng = np.random.default_rng(42)
rng.random(3)
```

## Generating Random Numbers

```python
rng = np.random.default_rng(42)

rng.random(5)                  # 5 floats uniformly in [0, 1)
rng.random((3, 3))             # 3x3 matrix of uniform floats

rng.integers(0, 10, size=5)    # 5 random ints in [0, 10) -- note: exclusive upper bound
rng.integers(0, 10, size=5, endpoint=True)  # inclusive of 10

rng.normal(loc=0, scale=1, size=5)      # standard normal (Gaussian) samples
rng.normal(loc=100, scale=15, size=1000)  # e.g., simulate IQ scores: mean=100, std=15

rng.uniform(low=0, high=100, size=5)    # uniform floats in a custom range
rng.binomial(n=10, p=0.5, size=5)       # binomial distribution samples
rng.poisson(lam=3, size=5)              # Poisson distribution samples
rng.exponential(scale=1.0, size=5)      # exponential distribution samples
```

## Sampling From Existing Data

```python
arr = np.array([10, 20, 30, 40, 50])

rng.choice(arr, size=3)                  # random sample WITH replacement
rng.choice(arr, size=3, replace=False)   # random sample WITHOUT replacement (like a subset)
rng.choice(arr, size=5, p=[0.5, 0.1, 0.1, 0.1, 0.2])  # weighted sampling by probability
```

**Data science use case: bootstrapping** — repeatedly resampling a dataset with replacement to estimate confidence intervals or the variance of a statistic, without assuming a distribution:

```python
data = np.array([23, 45, 12, 67, 34, 89, 21, 56])

def bootstrap_mean_ci(data, n_bootstrap=10000, ci=95):
    rng = np.random.default_rng(0)
    means = np.array([
        rng.choice(data, size=len(data), replace=True).mean()
        for _ in range(n_bootstrap)
    ])
    lower = np.percentile(means, (100 - ci) / 2)
    upper = np.percentile(means, 100 - (100 - ci) / 2)
    return means.mean(), (lower, upper)

estimated_mean, confidence_interval = bootstrap_mean_ci(data)
print(estimated_mean, confidence_interval)
```

## Shuffling

```python
arr = np.arange(10)
rng.shuffle(arr)          # shuffles IN PLACE
print(arr)

permuted = rng.permutation(10)   # returns a NEW shuffled array/permutation, original untouched
```

**Data science use case: manual train/test split**

```python
def train_test_split_manual(X, y, test_size=0.2, seed=42):
    rng = np.random.default_rng(seed)
    n = X.shape[0]
    indices = rng.permutation(n)
    test_count = int(n * test_size)

    test_idx, train_idx = indices[:test_count], indices[test_count:]
    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]
```

This is conceptually identical to what `sklearn.model_selection.train_test_split` does internally.

## Monte Carlo Simulation Example

A classic use case: estimating probabilities or expected values through repeated random simulation.

```python
# Estimate the probability of getting at least one 6 in 4 rolls of a fair die
rng = np.random.default_rng(1)

n_trials = 100_000
rolls = rng.integers(1, 7, size=(n_trials, 4))   # simulate 4 rolls, n_trials times
at_least_one_six = (rolls == 6).any(axis=1)
probability = at_least_one_six.mean()
print(f"Estimated probability: {probability:.4f}")   # ~0.5177, matches theoretical 1-(5/6)^4
```

## Reproducibility Best Practices

1. **Always set a seed** when publishing results, writing tests, or debugging — otherwise results change on every run and can't be verified.
2. **Pass the same `rng` object** through your pipeline (or derive child generators with `rng.spawn()`) rather than reseeding repeatedly, to avoid accidentally correlated "random" sequences.
3. **Document the seed** used in experiments — this is considered a core reproducibility practice in data science research and production ML.

```python
# Spawning independent child generators (good for parallel processes)
rng = np.random.default_rng(42)
child_rngs = rng.spawn(3)   # 3 independent, reproducible generators
```

**Next:** `10_numpy_advanced_performance_optimization.md`
