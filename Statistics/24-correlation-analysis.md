# 24. Correlation Analysis

## Overview
Correlation measures the strength and direction of the linear relationship between two continuous variables — a foundational step before building any regression model.

## Pearson Correlation Coefficient (r)
r ranges from −1 to +1:
- r = +1: perfect positive linear relationship
- r = −1: perfect negative linear relationship
- r = 0: no linear relationship
- |r| ≥ 0.7: strong; 0.3–0.7: moderate; < 0.3: weak (rules of thumb, context-dependent)

Formula: r = Σ[(xᵢ−x̄)(yᵢ−ȳ)] / √[Σ(xᵢ−x̄)² Σ(yᵢ−ȳ)²]

## Spearman's Rank Correlation
A non-parametric alternative that measures monotonic (not necessarily linear) relationships, using ranked data — more robust to outliers and non-linear-but-monotonic patterns.

## The Golden Rule: Correlation ≠ Causation
Two variables can be strongly correlated due to:
- A genuine causal relationship
- Reverse causation (Y causes X, not the other way around)
- A confounding third variable driving both
- Pure coincidence (especially in large datasets — "spurious correlation")

## Python Example
```python
import numpy as np
from scipy.stats import pearsonr, spearmanr

ad_spend = np.array([10,15,20,25,30,35,40])
sales = np.array([102,115,130,133,150,158,170])

r, p = pearsonr(ad_spend, sales)
print(f"Pearson r: {r:.3f}, p-value: {p:.4f}")
```

## Business Application
A marketing analyst finds a strong positive correlation (r = 0.85) between social media engagement and sales, but resists the temptation to claim engagement *causes* sales — both could be driven by a confounder like overall brand momentum or seasonality, warranting a controlled experiment before reallocating budget.

## Key Takeaways
- Correlation quantifies linear association strength/direction; it does not establish causation.
- Pearson's r assumes roughly linear relationships and is sensitive to outliers; Spearman's is more robust for monotonic, non-linear patterns.
- Always visualize with a scatter plot alongside the correlation coefficient — the same r can arise from very different underlying patterns (Anscombe's quartet).
