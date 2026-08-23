# 31. Non-Parametric Tests

## Overview
Non-parametric tests make far fewer assumptions about the underlying data distribution than t-tests or ANOVA — essential when data is heavily skewed, ordinal, has small sample sizes, or contains significant outliers.

## When to Go Non-Parametric
- Data is ordinal (rankings, satisfaction scales) rather than truly continuous.
- Sample size is small and normality can't be verified or assumed.
- Data contains significant outliers that would distort a mean-based test.

## Common Non-Parametric Tests and Their Parametric Counterparts
| Non-Parametric Test | Parametric Equivalent | Use Case |
|---|---|---|
| Mann-Whitney U test | Independent two-sample t-test | Compare two independent groups |
| Wilcoxon signed-rank test | Paired t-test | Compare two related/paired samples |
| Kruskal-Wallis test | One-way ANOVA | Compare 3+ independent groups |
| Spearman's rank correlation | Pearson correlation | Monotonic (non-linear) relationships |

## How They Work (Conceptually)
Most non-parametric tests convert raw values to **ranks** first, then compare rank sums/distributions between groups — this is what makes them robust to outliers and non-normal shapes (an extreme outlier is still just "the highest rank," not a distorting raw value).

## Trade-off
Non-parametric tests are more robust but generally have **less statistical power** than their parametric counterparts when the parametric assumptions actually do hold — you're trading some sensitivity for robustness.

## Python Example
```python
from scipy import stats
import numpy as np

group_a = [12, 15, 14, 200, 13]  # contains an outlier
group_b = [20, 22, 19, 25, 21]

u_stat, p_value = stats.mannwhitneyu(group_a, group_b)
print(f"Mann-Whitney U: {u_stat}, p-value: {p_value:.4f}")
```

## Business Application
A UX researcher analyzing Likert-scale survey ratings (ordinal 1-5 data) uses the Mann-Whitney U test instead of a t-test to compare satisfaction between two design variants, correctly respecting that the data is ordinal, not truly continuous.

## Key Takeaways
- Non-parametric tests trade some statistical power for far fewer distributional assumptions.
- Use them for ordinal data, small samples, or data with significant outliers/skew.
- Rank-based methods are naturally robust to extreme values, unlike mean-based parametric tests.
