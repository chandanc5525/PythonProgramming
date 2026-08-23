# 22. ANOVA — Analysis of Variance

## Overview
ANOVA extends the t-test to compare means across **three or more** groups simultaneously, without inflating the false-positive rate that would result from running many pairwise t-tests.

## Why Not Just Run Multiple t-Tests?
Running many pairwise t-tests increases the overall chance of a false positive (multiple comparisons problem). ANOVA tests all groups at once with a single test, controlling the overall Type I error rate.

## Hypotheses
- H₀: μ₁ = μ₂ = μ₃ = ... = μₖ (all group means are equal)
- H₁: at least one group mean differs

## The F-Statistic
ANOVA compares **between-group variance** to **within-group variance**:
F = (variance between groups) / (variance within groups)

A large F means group means differ more than would be expected from random within-group noise alone.

## After a Significant ANOVA: Post-Hoc Tests
A significant ANOVA tells you *that* a difference exists somewhere, but not *where*. Post-hoc tests (Tukey's HSD, Bonferroni-corrected pairwise tests) identify which specific group pairs differ.

## Assumptions
- Independence of observations.
- Approximate normality within each group.
- Homogeneity of variance across groups (check with Levene's test).

## Python Example
```python
from scipy import stats
import numpy as np

region_a = np.random.normal(500, 50, 40)
region_b = np.random.normal(520, 50, 40)
region_c = np.random.normal(560, 50, 40)

f_stat, p_value = stats.f_oneway(region_a, region_b, region_c)
print(f"F-stat: {f_stat:.3f}, p-value: {p_value:.4f}")
```

## Business Application
A retail chain compares average daily sales across four store formats (flagship, mall, outlet, online-pickup) using one-way ANOVA to test whether format significantly affects sales, then runs Tukey's HSD to identify exactly which formats differ from each other.

## Key Takeaways
- ANOVA is the right tool for comparing 3+ group means at once, controlling overall error rate.
- A significant F-test must be followed by post-hoc tests to pinpoint which groups actually differ.
- Two-way ANOVA extends this further to test the effect of two categorical factors (and their interaction) simultaneously.
