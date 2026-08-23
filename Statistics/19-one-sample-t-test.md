# 19. One-Sample t-Test

## Overview
The one-sample t-test determines whether a sample mean is significantly different from a known or hypothesized population value — useful when you want to check a single group against a fixed benchmark.

## When to Use
- Comparing a sample mean to a target/benchmark (e.g., "is average call handling time different from the target of 6 minutes?").
- Population standard deviation is unknown (very common in practice) — the t-distribution accounts for this extra uncertainty, especially with smaller samples.

## Hypotheses
- H₀: μ = μ₀ (sample mean equals the hypothesized value)
- H₁: μ ≠ μ₀ (two-tailed) or μ > μ₀ / μ < μ₀ (one-tailed)

## Test Statistic
t = (x̄ − μ₀) / (s / √n), with degrees of freedom = n − 1

## Assumptions
- Data is continuous and approximately normally distributed (or n is large enough for CLT to apply).
- Observations are independent.
- Random sampling from the population of interest.

## Python Example
```python
from scipy import stats
import numpy as np

handling_times = np.array([5.8, 6.4, 6.1, 7.0, 6.5, 5.9, 6.8, 7.2, 6.3, 6.6])
target = 6.0

t_stat, p_value = stats.ttest_1samp(handling_times, popmean=target)
print(f"t-stat: {t_stat:.3f}, p-value: {p_value:.4f}")
# If p < 0.05, handling times differ significantly from the 6-minute target
```

## Business Application
A call center manager tests whether average handling time across a sample of calls differs significantly from the company's 6-minute SLA target, providing statistical (not just anecdotal) grounds to decide whether additional agent training is warranted.

## Key Takeaways
- Use a one-sample t-test to compare a single sample mean against a known benchmark, not against another sample.
- The t-distribution (wider tails than normal) accounts for extra uncertainty from estimating the standard deviation.
- With larger sample sizes, the t-distribution converges to the normal distribution.
