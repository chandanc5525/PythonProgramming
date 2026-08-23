# 14. Central Limit Theorem

## Overview
The Central Limit Theorem (CLT) is the theoretical backbone that makes most of inferential statistics possible — it explains why the normal distribution shows up everywhere, even when the underlying data isn't normal.

## The Theorem
For a sufficiently large sample size (commonly n ≥ 30), the **sampling distribution of the sample mean** approaches a normal distribution — *regardless of the shape of the original population distribution* — with:
- Mean of sampling distribution = population mean (μ)
- Standard deviation of sampling distribution (standard error) = σ / √n

## Why It's So Important
Even if individual customer purchase amounts are heavily right-skewed, the *average* purchase amount across repeated samples of, say, 50 customers will be approximately normally distributed. This lets us apply normal-distribution-based methods (confidence intervals, t-tests, z-tests) to sample means even when raw data isn't normal.

## Key Implications
- Larger samples → tighter, more normal sampling distribution (standard error shrinks as 1/√n).
- Enables hypothesis testing and confidence intervals on virtually any population, given large enough samples.
- Explains why aggregated business metrics (average order value, average response time) tend to look normal even when individual transactions don't.

## Python Example
```python
import numpy as np

pop = np.random.exponential(scale=50, size=100000)  # skewed population

sample_means = [np.mean(np.random.choice(pop, size=40)) for _ in range(1000)]
print("Population skew (raw data): highly skewed")
print("Sample means std dev (~SE):", np.std(sample_means))
print("Sample means look approximately normal via histogram")
```

## Business Application
Individual customer session durations are right-skewed (most sessions short, a few very long), but a product analytics team can still validly use t-tests to compare *average* session duration between two app versions because the CLT guarantees the sampling distribution of the mean is approximately normal at their sample sizes.

## Key Takeaways
- CLT justifies using normal-based inferential methods even on non-normal raw data, as long as sample size is adequate.
- Standard error decreases with √n — quadrupling sample size only halves the standard error.
- CLT is why "n ≥ 30" is a common rule of thumb in applied statistics.
