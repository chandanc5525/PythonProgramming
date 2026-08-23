# 5. Descriptive Statistics: Measures of Dispersion

## Overview
Central tendency alone can hide important differences. Two datasets can have the same mean but wildly different spread. Measures of dispersion quantify how spread out the data is.

## Key Measures
- **Range**: max − min. Simple but sensitive to outliers.
- **Variance (σ² / s²)**: average squared deviation from the mean.
- **Standard deviation (σ / s)**: square root of variance; same units as the data.
- **Interquartile Range (IQR)**: Q3 − Q1, the spread of the middle 50% of data. Robust to outliers.
- **Coefficient of Variation (CV)**: (std dev / mean) × 100 — compares variability across datasets with different units/scales.

## Formulas
- Sample variance: s² = Σ(xᵢ − x̄)² / (n − 1)
- Sample standard deviation: s = √s²
- IQR = Q3 − Q1

## Why n − 1?
Dividing by (n − 1) instead of n (Bessel's correction) corrects the bias that arises from estimating variance using the sample mean instead of the true population mean, giving an unbiased estimator of population variance.

## Python Example
```python
import numpy as np

store_a = [95, 100, 105, 98, 102]   # low variability
store_b = [50, 150, 90, 110, 100]   # high variability, same mean

print("Store A std dev:", np.std(store_a, ddof=1))
print("Store B std dev:", np.std(store_b, ddof=1))
# Both have mean ~100, but very different consistency
```

## Business Application
Two delivery services have the same average delivery time (45 minutes), but one has a standard deviation of 5 minutes and the other 25 minutes. The first is far more reliable — dispersion, not just the average, drives customer trust and operational planning.

## Key Takeaways
- Always report spread alongside central tendency — the mean alone can be misleading.
- Standard deviation is in the same units as the original data, making it interpretable.
- Consistency (low variance) is often as valuable to a business as a good average.
