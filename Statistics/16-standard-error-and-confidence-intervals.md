# 16. Standard Error and Confidence Intervals

## Overview
A single sample statistic (like a sample mean) is just a point estimate — it doesn't communicate how much uncertainty surrounds it. Confidence intervals fix this by providing a range of plausible values for the population parameter.

## Standard Error (SE)
SE = σ / √n (population std dev known) or s / √n (using sample std dev as estimate)

The standard error measures how much sample means would vary from sample to sample — it shrinks as sample size grows.

## Confidence Interval Formula
CI = point estimate ± (critical value × standard error)

For a 95% CI on a mean (large sample): x̄ ± 1.96 × (s/√n)

## Interpreting a Confidence Interval — Correctly
"We are 95% confident the true population mean lies between $118 and $132" means: **if we repeated this sampling process many times, 95% of the resulting intervals would contain the true population parameter.** It does *not* mean there's a 95% probability the true mean is in this specific interval (a common misinterpretation).

## Factors Affecting Interval Width
- Larger sample size → narrower interval (more precision).
- Higher confidence level (99% vs 90%) → wider interval (more certainty requires more range).
- Greater data variability (larger s) → wider interval.

## Python Example
```python
import numpy as np
from scipy import stats

sample = np.random.normal(loc=125, scale=20, size=100)
mean = np.mean(sample)
se = stats.sem(sample)
ci = stats.t.interval(0.95, df=len(sample)-1, loc=mean, scale=se)
print(f"Sample mean: {mean:.2f}, 95% CI: ({ci[0]:.2f}, {ci[1]:.2f})")
```

## Business Application
Instead of reporting "average customer satisfaction is 7.8," an analytics team reports "average satisfaction is 7.8, 95% CI [7.5, 8.1]" — giving leadership a defensible sense of precision and preventing overreaction to small period-to-period fluctuations that fall within the margin of error.

## Key Takeaways
- Confidence intervals communicate the precision of an estimate, not just its point value.
- Wider intervals reflect more uncertainty — from smaller samples, higher variability, or higher confidence levels.
- Always report a range, not just a point estimate, when precision matters to the decision.
