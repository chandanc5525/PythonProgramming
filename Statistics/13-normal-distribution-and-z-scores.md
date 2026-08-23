# 13. The Normal Distribution and Z-Scores

## Overview
The normal distribution's predictable, symmetric shape makes it possible to standardize any observation and compare it against a reference — the core idea behind z-scores.

## The Standard Normal Distribution
A normal distribution with mean = 0 and standard deviation = 1. Any normal variable can be converted into this standard form.

## Z-Score Formula
z = (x − μ) / σ

A z-score tells you how many standard deviations a value is from the mean.
- z = 0 → exactly at the mean
- z = +2 → two standard deviations above the mean (unusually high)
- z = −1.5 → 1.5 standard deviations below the mean

## Using Z-Scores
- Compare values from different scales/distributions (e.g., SAT score vs GRE score).
- Identify outliers (commonly |z| > 3 is flagged as unusual).
- Look up exact probabilities using the standard normal table or software.

## Worked Example
A customer spends $180/month; the average customer spends $120 with std dev $30.
z = (180 − 120) / 30 = **2.0** → this customer spends 2 standard deviations above average, placing them roughly in the top 2.3% of spenders.

## Python Example
```python
from scipy.stats import norm

mu, sigma = 120, 30
x = 180
z = (x - mu) / sigma
percentile = norm.cdf(z) * 100
print(f"Z-score: {z}, Percentile: {percentile:.1f}%")
```

## Business Application
A bank flags credit card transactions with a z-score beyond ±3 relative to a customer's typical spending pattern as potentially fraudulent — standardization allows one universal rule to apply across millions of customers with very different spending baselines.

## Key Takeaways
- Z-scores standardize values so they can be compared across different means/scales.
- The standard normal distribution converts any z-score directly into a percentile/probability.
- Z-scores are a simple, powerful tool for outlier detection and anomaly flagging in business systems.
