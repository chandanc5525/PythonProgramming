# 6. Data Distribution Shape: Skewness and Kurtosis

## Overview
Beyond center and spread, the *shape* of a distribution affects which statistical methods are valid and how data should be interpreted.

## Skewness (asymmetry)
- **Symmetric** (skew ≈ 0): mean ≈ median ≈ mode.
- **Right-skewed / positive skew**: long tail to the right; mean > median (e.g., income, house prices).
- **Left-skewed / negative skew**: long tail to the left; mean < median (e.g., age at retirement).

## Kurtosis (tailedness)
- **Mesokurtic** (kurtosis ≈ 3, or excess ≈ 0): normal-like tails.
- **Leptokurtic** (excess > 0): heavy tails, more extreme outliers (e.g., stock returns).
- **Platykurtic** (excess < 0): light tails, fewer extreme values.

## Why It Matters
- Many classical statistical tests (t-tests, ANOVA, linear regression) assume approximately normal (symmetric, mesokurtic) data.
- High skew or kurtosis signals you may need transformations (log, Box-Cox) or non-parametric methods instead.

## Python Example
```python
import numpy as np
from scipy.stats import skew, kurtosis

revenue = np.random.exponential(scale=1000, size=1000)  # right-skewed by nature

print("Skewness:", skew(revenue))       # positive, confirms right skew
print("Excess kurtosis:", kurtosis(revenue))
```

## Business Application
A finance team analyzing daily stock returns notices high kurtosis (fat tails) — meaning extreme gains/losses are more likely than a normal distribution would suggest, prompting them to use risk models that account for tail risk rather than assuming normality.

## Key Takeaways
- Skewness measures asymmetry; kurtosis measures the likelihood of extreme values.
- Checking shape before modeling prevents invalid application of normal-distribution-based methods.
- Log transformations often reduce right skew, making data closer to normal for modeling.
