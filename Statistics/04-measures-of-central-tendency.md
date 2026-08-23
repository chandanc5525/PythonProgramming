# 4. Descriptive Statistics: Measures of Central Tendency

## Overview
Measures of central tendency summarize a dataset with a single representative value — answering "what's typical?"

## The Three Core Measures
- **Mean (average)**: sum of values divided by count. Sensitive to outliers.
- **Median**: the middle value when data is sorted. Robust to outliers.
- **Mode**: the most frequently occurring value. Only measure usable for nominal data.

## Formulas
- Mean: x̄ = (Σxᵢ) / n
- Median: middle value (or average of two middle values if n is even)
- Mode: value(s) with highest frequency

## Choosing the Right Measure
| Situation | Best Measure |
|---|---|
| Symmetric distribution, no outliers | Mean |
| Skewed distribution or outliers present | Median |
| Categorical data | Mode |
| Income, home prices (typically right-skewed) | Median |

## Python Example
```python
import numpy as np
from scipy import stats

data = [42000, 45000, 47000, 48000, 250000]  # one high outlier (executive salary)

print("Mean:", np.mean(data))     # heavily pulled up by outlier
print("Median:", np.median(data)) # robust, more representative
print("Mode:", stats.mode(data, keepdims=True).mode)
```

## Business Application
When reporting "typical" employee salary to the board, an HR analyst reports the **median**, not the mean, because a handful of executive salaries would inflate the mean and misrepresent typical compensation — a classic case of choosing the statistic that tells the truth.

## Key Takeaways
- Mean is best for symmetric data; median is best when outliers or skew are present.
- Reporting the wrong central tendency measure is a common source of misleading business dashboards.
- Always look at the shape of the distribution before picking a summary statistic.
