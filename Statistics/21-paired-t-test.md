# 21. Paired t-Test

## Overview
The paired t-test compares two related measurements taken from the **same** subjects or matched pairs — such as before/after or two treatments on the same unit — accounting for the natural correlation between paired observations.

## When to Use
- Before-and-after studies (customer satisfaction before vs after a service change, for the same customers).
- Matched-pairs designs (same store's sales in two different promotional periods).
- **Not** appropriate for two independent, unrelated groups — use the two-sample t-test for that (Topic 20).

## Why Pairing Matters
Pairing removes between-subject variability from the comparison, focusing purely on the *within-subject* change — this typically gives more statistical power than treating the two sets as independent groups.

## Hypotheses
- H₀: μ_d = 0 (mean of the differences is zero — no real change)
- H₁: μ_d ≠ 0

## Test Statistic
Compute the difference d = x_after − x_before for each pair, then run a one-sample t-test on those differences against 0:
t = d̄ / (s_d / √n)

## Python Example
```python
from scipy import stats
import numpy as np

before = np.array([72, 68, 75, 80, 65, 70, 78, 74])
after  = np.array([75, 70, 78, 82, 68, 74, 80, 77])

t_stat, p_value = stats.ttest_rel(after, before)
print(f"t-stat: {t_stat:.3f}, p-value: {p_value:.4f}")
```

## Business Application
An HR team measures employee engagement scores for the same 200 employees before and after a new benefits program, using a paired t-test to isolate the true within-employee change — a far more precise design than comparing two different employee samples.

## Key Takeaways
- Use paired t-tests when the same subjects are measured twice (or matched deliberately) — it's statistically more powerful than an unpaired test in these cases.
- The test effectively reduces to a one-sample t-test on the differences between pairs.
- Mistaking a paired design for an independent one wastes statistical power and can obscure real effects.
