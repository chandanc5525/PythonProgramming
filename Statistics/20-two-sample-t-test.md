# 20. Two-Sample t-Test

## Overview
The two-sample (independent samples) t-test compares the means of two separate, unrelated groups to determine whether they differ significantly — the statistical backbone of A/B testing.

## When to Use
- Comparing outcomes between two independent groups (control vs treatment, Group A vs Group B) that were **not** paired/matched.
- Example: average revenue per user for customers who saw Version A vs Version B of a landing page.

## Hypotheses
- H₀: μ₁ = μ₂ (no difference between group means)
- H₁: μ₁ ≠ μ₂ (two-tailed) or a directional alternative

## Two Variants
- **Equal variances assumed (Student's t-test)**: use when both groups have similar variance (check with Levene's test).
- **Unequal variances (Welch's t-test)**: safer default in practice; doesn't assume equal variance between groups.

## Assumptions
- Independence of observations, both within and between groups.
- Approximate normality of each group (or large enough n per CLT).
- Random assignment to groups (critical for causal interpretation in A/B tests).

## Python Example
```python
from scipy import stats
import numpy as np

group_a = np.random.normal(45, 8, 150)   # current design
group_b = np.random.normal(48, 8, 150)   # new design

t_stat, p_value = stats.ttest_ind(group_a, group_b, equal_var=False)  # Welch's t-test
print(f"t-stat: {t_stat:.3f}, p-value: {p_value:.4f}")
```

## Business Application
An e-commerce team runs a two-sample t-test comparing average order value between users who saw a new recommendation algorithm (treatment) and users who saw the old one (control), providing the statistical basis for a rollout decision.

## Key Takeaways
- Two-sample t-tests compare two independent group means — the statistical engine behind most classic A/B tests.
- Welch's t-test (unequal variances) is generally the safer default choice over Student's t-test.
- Random assignment to groups is what allows a significant result to be interpreted causally, not just as correlation.
