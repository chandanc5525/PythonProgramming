# 30. A/B Testing for Business Decisions

## Overview
A/B testing (a controlled, randomized experiment) is the gold standard for establishing *causal* impact of a business change — turning "we think this works" into "we know this works, and by how much."

## Anatomy of an A/B Test
1. **Define the hypothesis and metric**: e.g., "the new button color increases click-through rate."
2. **Randomly assign users** to control (A) and treatment (B) groups — randomization is what allows causal claims.
3. **Determine required sample size in advance** using power analysis (Topic 33) — avoid "peeking" and stopping early, which inflates false-positive risk.
4. **Run the test for a pre-specified duration**, covering full business cycles (e.g., a full week to capture weekday/weekend effects).
5. **Analyze with the appropriate test**: two-sample t-test (continuous metrics like revenue) or chi-square/z-test for proportions (binary metrics like conversion).
6. **Check for practical, not just statistical, significance** — a "significant" 0.01% lift may not be worth the engineering cost to implement.

## Common Pitfalls
- **Peeking problem**: repeatedly checking results and stopping as soon as p < 0.05 dramatically inflates the true false-positive rate.
- **Novelty effect**: users may react differently simply because something is *new*, not because it's genuinely better long-term.
- **Sample ratio mismatch**: if the actual split between groups deviates from the intended split (e.g., 48/52 instead of 50/50), it signals a bug in randomization that invalidates results.
- **Multiple testing**: testing many metrics simultaneously without correction inflates the chance of a false "win."

## Python Example
```python
from scipy.stats import proportions_ztest

conversions = [180, 220]   # [control conversions, treatment conversions]
visitors = [2000, 2000]

z_stat, p_value = proportions_ztest(conversions, visitors)
print(f"z-stat: {z_stat:.3f}, p-value: {p_value:.4f}")
```

## Business Application
A product team pre-registers sample size and test duration before launching an A/B test on a new onboarding flow, avoiding the temptation to stop early on a promising-looking result — protecting the company from rolling out a change based on a false positive.

## Key Takeaways
- Randomization is what allows an A/B test to claim causation, not just correlation.
- Pre-committing to sample size and test duration prevents the "peeking problem" from inflating false positives.
- Statistical significance and business/practical significance are different questions — always evaluate both.
