# 17. Hypothesis Testing Fundamentals

## Overview
Hypothesis testing is the formal statistical framework for deciding whether observed data provides enough evidence to support a claim about a population, beyond what random chance alone could explain.

## The Framework
1. **Null hypothesis (H₀)**: the default assumption — typically "no effect" or "no difference" (e.g., new website design has no effect on conversion rate).
2. **Alternative hypothesis (H₁ / Hₐ)**: the claim you're testing for (e.g., new design increases conversion rate).
3. **Significance level (α)**: the threshold probability for rejecting H₀ when it's actually true — commonly 0.05.
4. **Test statistic**: a standardized value computed from sample data (z, t, F, χ² depending on the test).
5. **P-value**: the probability of observing data this extreme (or more extreme) *if H₀ were true*.
6. **Decision rule**: if p-value < α, reject H₀ in favor of H₁; otherwise, fail to reject H₀.

## Critical Nuance
"Fail to reject H₀" is **not** the same as "prove H₀ is true." Absence of evidence is not evidence of absence — you simply didn't find enough evidence to overturn the default assumption.

## One-Tailed vs Two-Tailed Tests
- **Two-tailed**: tests for any difference (H₁: μ ≠ μ₀) — used when direction isn't specified in advance.
- **One-tailed**: tests for a difference in a specific direction (H₁: μ > μ₀) — more statistical power if the direction is truly known/expected in advance.

## Python Example
```python
from scipy import stats
import numpy as np

control = np.random.normal(100, 15, 200)
treatment = np.random.normal(104, 15, 200)

t_stat, p_value = stats.ttest_ind(treatment, control)
print(f"t-stat: {t_stat:.3f}, p-value: {p_value:.4f}")
alpha = 0.05
print("Reject H0" if p_value < alpha else "Fail to reject H0")
```

## Business Application
A product team tests H₀: "the new checkout flow has no effect on completion rate" against H₁: "it increases completion rate." A p-value of 0.02 (< 0.05) gives them statistical grounds to roll out the new flow, rather than relying on gut feel.

## Key Takeaways
- Hypothesis testing formalizes decision-making under uncertainty using a null/alternative framework.
- A low p-value is evidence against H₀, not proof of H₁ — statistics never "proves" anything with certainty.
- The significance level α is chosen *before* the test, to control the risk of false positives.
