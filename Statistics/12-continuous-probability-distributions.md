# 12. Continuous Probability Distributions (Normal, Uniform, Exponential)

## Overview
Continuous distributions model variables that can take any value within a range — revenue, time, temperature — and are described by a probability density function (PDF) rather than exact-point probabilities.

## Normal (Gaussian) Distribution
- Symmetric, bell-shaped, defined by mean μ and standard deviation σ.
- The most important distribution in statistics due to the Central Limit Theorem (Topic 14).
- Empirical rule: ~68% of data within ±1σ, ~95% within ±2σ, ~99.7% within ±3σ.

## Uniform Distribution
- All values within [a, b] are equally likely.
- Use case: modeling "a customer arrives randomly within a 30-minute window" with no preference for any sub-interval.

## Exponential Distribution
- Models the time between independent events occurring at a constant rate (closely related to Poisson).
- Memoryless property: the probability of waiting additional time doesn't depend on time already waited.
- Use case: time between customer arrivals, time until equipment failure.

## Python Example
```python
import numpy as np
from scipy.stats import norm, expon

# Normal: probability delivery takes longer than 60 min (mean=45, sd=10)
p_late = 1 - norm.cdf(60, loc=45, scale=10)
print("P(delivery > 60 min):", round(p_late, 4))

# Exponential: mean time between website visits = 2 minutes
p_within_1min = expon.cdf(1, scale=2)
print("P(next visit within 1 min):", round(p_within_1min, 4))
```

## Business Application
A logistics company models delivery times as normally distributed to set realistic SLAs (e.g., "95% of deliveries within X minutes"), and models time-between-orders as exponential to plan warehouse staffing for peak arrival rates.

## Key Takeaways
- The normal distribution is the backbone of classical inferential statistics.
- Uniform models "equally likely" continuous outcomes; exponential models waiting times between rare events.
- Knowing the underlying distribution lets you compute exact probabilities for business thresholds and SLAs.
