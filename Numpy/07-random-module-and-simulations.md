# NumPy Lecture Notes — 07: Random Module & Simulations

## 1. Introduction

NumPy's `numpy.random` module provides tools for generating random numbers, sampling from statistical distributions, and running stochastic simulations. Since NumPy 1.17, the **Generator API** (`np.random.default_rng()`) is the recommended modern interface, offering better statistical properties and reproducibility over the legacy `np.random.seed()`-based functions.

---

## 2. Coding: Random Number Generation

### Legacy API (still widely seen in existing code)

```python
import numpy as np

np.random.seed(42)   # for reproducibility

print(np.random.rand(3))          # 3 uniform random floats [0,1)
print(np.random.randn(3))          # 3 samples from standard normal distribution
print(np.random.randint(1, 100, 5))  # 5 random ints between 1-99
print(np.random.choice([10, 20, 30, 40], size=3))  # random sampling
print(np.random.choice([10, 20, 30, 40], size=3, replace=False))  # no repeats
```

### Modern Generator API (recommended)

```python
rng = np.random.default_rng(seed=42)   # create a reproducible generator

print(rng.random(3))              # uniform floats [0,1)
print(rng.integers(1, 100, 5))     # random integers
print(rng.normal(loc=0, scale=1, size=5))     # normal distribution
print(rng.uniform(low=10, high=20, size=5))    # uniform distribution
print(rng.choice([1, 2, 3, 4, 5], size=3, replace=False))
```

### Shuffling and Permutations

```python
a = np.array([1, 2, 3, 4, 5])

rng = np.random.default_rng(1)
rng.shuffle(a)              # shuffles in-place
print(a)

permuted = rng.permutation([1, 2, 3, 4, 5])   # returns a new shuffled array
print(permuted)
```

### Sampling From Distributions

```python
rng = np.random.default_rng(7)

normal_samples = rng.normal(loc=100, scale=15, size=1000)   # e.g., IQ scores
binomial_samples = rng.binomial(n=10, p=0.5, size=1000)      # coin flips
poisson_samples = rng.poisson(lam=3, size=1000)               # arrival events
exponential_samples = rng.exponential(scale=1.0, size=1000)   # wait times

print("Normal mean:", normal_samples.mean())
print("Binomial mean:", binomial_samples.mean())
```

---

## 3. Coding: Monte Carlo Simulation Example

```python
# Estimating Pi using Monte Carlo simulation
rng = np.random.default_rng(0)
n_points = 1_000_000

x = rng.uniform(-1, 1, n_points)
y = rng.uniform(-1, 1, n_points)

inside_circle = (x**2 + y**2) <= 1
pi_estimate = 4 * np.sum(inside_circle) / n_points

print(f"Estimated Pi: {pi_estimate}")   # ~3.14159
```

---

## 4. Use Cases & Scenarios

1. **Train/test splitting**: Randomly shuffling and splitting a dataset into training and testing subsets for machine learning.
2. **Monte Carlo simulations**: Modeling uncertainty in financial forecasting, risk analysis, or physical systems using repeated random sampling.
3. **Data augmentation**: Randomly rotating, flipping, or adding noise to training images to improve model generalization.
4. **A/B testing simulation**: Simulating thousands of hypothetical trials to build confidence intervals before running a real experiment.
5. **Game development**: Generating random events, loot drops, or procedural terrain.
6. **Bootstrapping**: Resampling a dataset with replacement to estimate the variability of a statistic.

### Real-World Scenario

> A finance team wants to estimate the probability that a stock portfolio will lose more than 10% of its value in a year. Using historical mean returns and volatility, they run a Monte Carlo simulation — generating 100,000 random yearly return scenarios drawn from a normal distribution — and calculate the percentage of simulations resulting in a loss greater than 10%.

```python
rng = np.random.default_rng(42)

mean_return = 0.08     # 8% average annual return
volatility = 0.15      # 15% standard deviation
n_simulations = 100_000

simulated_returns = rng.normal(mean_return, volatility, n_simulations)
prob_large_loss = np.mean(simulated_returns < -0.10)

print(f"Probability of losing more than 10%: {prob_large_loss:.2%}")
```

---

## 5. Practice Problems

1. Use `np.random.default_rng` with a fixed seed to generate 10 random integers between 1 and 50. Verify that using the same seed produces the same results every time.
2. Simulate rolling a six-sided die 10,000 times using `rng.integers(1, 7, 10000)`. Compute the frequency of each outcome and compare to the theoretical probability (1/6).
3. Write a train/test split function from scratch: given a dataset of 1000 samples, randomly shuffle indices and split into 80% training and 20% testing sets (no `sklearn` allowed).
4. Simulate flipping a fair coin 1000 times using `rng.binomial(1, 0.5, 1000)`. What proportion of heads did you get? How does it change as you increase to 100,000 flips?
5. **Scenario (Monte Carlo)**: A dice game pays $10 if you roll a sum of 7 or 11 with two dice, otherwise you lose $2. Simulate 100,000 rounds and estimate the expected profit/loss per game.
6. **Scenario (Bootstrapping)**: Given a small sample `data = np.array([23, 45, 12, 67, 34])`, use `rng.choice` with `replace=True` to generate 1000 bootstrap resamples and estimate the standard error of the mean.
7. **Conceptual**: Explain why `np.random.seed()` (legacy, global state) is discouraged in modern code compared to creating a local `Generator` object via `np.random.default_rng()`.
