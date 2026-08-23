# 33. Statistical Power and Sample Size Determination

## Overview
Before running any experiment or study, statistical power analysis answers a critical planning question: "how much data do I need to reliably detect an effect I actually care about?"

## Statistical Power
Power = 1 − β = the probability of correctly rejecting H₀ when H₁ is actually true (i.e., correctly detecting a real effect). Conventionally, 80% power is a common minimum target.

## Four Interconnected Factors
1. **Sample size (n)**: larger samples → higher power.
2. **Effect size**: the magnitude of the true difference/relationship you want to detect — larger effects are easier to detect with less data.
3. **Significance level (α)**: stricter α (e.g., 0.01 vs 0.05) requires more data to maintain the same power.
4. **Power (1 − β)**: the target detection probability, typically set at 0.80 or 0.90.

Any three of these determine the fourth — power analysis is most commonly used to solve for required sample size given a target effect size, α, and power.

## Why This Matters Before, Not After, a Study
- **Underpowered studies** risk missing real effects (Type II error) and wasting the resources spent — a "no significant difference" result from an underpowered test is genuinely uninformative.
- **Overpowered studies** can detect trivially small, practically meaningless effects as "statistically significant," wasting resources on unnecessary precision.

## Python Example
```python
from statsmodels.stats.power import TTestIndPower

analysis = TTestIndPower()
required_n = analysis.solve_power(effect_size=0.3, alpha=0.05, power=0.8, alternative='two-sided')
print(f"Required sample size per group: {required_n:.0f}")
```

## Business Application
Before launching an A/B test, a growth team runs a power analysis using their minimum meaningful lift (e.g., a 2% conversion increase) to determine they need 15,000 users per group — preventing them from running an underpowered test that would fail to detect a real, valuable improvement.

## Key Takeaways
- Power analysis should happen *before* data collection, not after a "non-significant" result to explain it away.
- An underpowered study risks costly false negatives — missing real, valuable effects.
- Effect size (not just p-value) should drive sample size planning, since it reflects what's practically meaningful to the business.
