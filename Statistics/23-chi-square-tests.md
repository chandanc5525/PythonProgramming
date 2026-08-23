# 23. Chi-Square Tests

## Overview
Chi-square tests are used for categorical data — testing relationships between categories or whether observed category frequencies match expected ones. Unlike t-tests/ANOVA, they don't require numeric/continuous data.

## Two Main Types
### 1. Chi-Square Goodness-of-Fit Test
Tests whether a single categorical variable's observed distribution matches an expected distribution.
- H₀: the observed frequencies match the expected distribution.
- Example: "Do website visits split evenly (25% each) across four traffic sources, as expected?"

### 2. Chi-Square Test of Independence
Tests whether two categorical variables are associated (dependent) or unrelated (independent).
- H₀: the two variables are independent (no association).
- Example: "Is there a relationship between customer region and preferred payment method?"

## Test Statistic
χ² = Σ [(Observed − Expected)² / Expected], summed across all cells

Larger differences between observed and expected counts produce a larger χ² statistic and a stronger case against H₀.

## Assumptions
- Data are frequency counts, not percentages or continuous measures.
- Observations are independent.
- Expected count in each cell is generally ≥ 5 for the test to be valid.

## Python Example
```python
from scipy.stats import chi2_contingency
import numpy as np

# Rows: region, Columns: payment method (contingency table of counts)
table = np.array([[120, 90, 40],
                   [80, 110, 60],
                   [100, 95, 55]])

chi2, p_value, dof, expected = chi2_contingency(table)
print(f"Chi2: {chi2:.3f}, p-value: {p_value:.4f}, dof: {dof}")
```

## Business Application
A marketing analyst uses a chi-square test of independence to check whether email subject-line style (categorical) is associated with whether a customer opens the email (categorical), guiding subject-line strategy with statistical confidence rather than assumption.

## Key Takeaways
- Chi-square tests are the standard tool for categorical (not numeric) data analysis.
- Goodness-of-fit checks a single variable against an expected distribution; test of independence checks association between two variables.
- Small expected cell counts (< 5) can invalidate the chi-square test — consider Fisher's exact test as an alternative in that case.
