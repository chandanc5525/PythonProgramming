# 18. Type I and Type II Errors

## Overview
Every hypothesis test involves a risk of being wrong. Understanding the two types of errors — and their tradeoff — is essential to setting statistical tests up appropriately for the business stakes involved.

## The Two Errors
| | H₀ is actually True | H₀ is actually False |
|---|---|---|
| **Reject H₀** | Type I Error (False Positive) — probability = α | Correct decision (True Positive) |
| **Fail to reject H₀** | Correct decision (True Negative) | Type II Error (False Negative) — probability = β |

- **Type I Error (α)**: concluding there's an effect when there isn't one (a false alarm).
- **Type II Error (β)**: failing to detect an effect that actually exists (a missed opportunity).
- **Statistical Power (1 − β)**: the probability of correctly detecting a real effect — see Topic 33.

## The Tradeoff
Lowering α (being more conservative about false positives) increases β (more likely to miss real effects), all else equal. The right balance depends on the relative *cost* of each error type to the business.

## Choosing Based on Business Cost
- **Medical screening test**: Type II error (missing a real disease) is often far costlier than Type I — bias toward lower β (higher sensitivity), even at the cost of more false positives.
- **Spam filter**: Type I error (blocking a legitimate email) may be costlier than Type II (letting some spam through) — bias toward lower α.

## Python Example
```python
# Simulating Type I error rate: how often we reject a TRUE null hypothesis
import numpy as np
from scipy import stats

false_positives = 0
trials = 1000
for _ in range(trials):
    sample_a = np.random.normal(100, 15, 50)
    sample_b = np.random.normal(100, 15, 50)  # SAME mean -> H0 is true
    _, p = stats.ttest_ind(sample_a, sample_b)
    if p < 0.05:
        false_positives += 1

print("Empirical Type I error rate:", false_positives/trials)  # should be ~0.05
```

## Business Application
A fraud detection team deliberately sets a lower significance threshold (accepting a higher false-positive rate) because the cost of missing actual fraud (Type II error) is far greater than the cost of extra manual review of flagged-but-legitimate transactions (Type I error).

## Key Takeaways
- Type I error = false positive; Type II error = false negative — you can't minimize both simultaneously without more data.
- The acceptable balance between α and β should be driven by the relative business cost of each error, not a default 0.05.
- Increasing sample size is the main lever that reduces both errors simultaneously.
