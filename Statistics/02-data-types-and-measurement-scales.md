# 2. Data Types and Measurement Scales

## Overview
Before applying any statistical technique, you must know what *kind* of data you have. The measurement scale determines which summary statistics, charts, and tests are valid.

## Categories of Data
- **Qualitative (Categorical)**
  - *Nominal*: unordered categories (gender, product category, region).
  - *Ordinal*: ordered categories with unequal/unknown spacing (customer satisfaction: low/medium/high).
- **Quantitative (Numerical)**
  - *Discrete*: countable values (number of orders, defects).
  - *Continuous*: measurable values on a continuum (revenue, weight, time).

## Measurement Scales
| Scale | Order | Equal Intervals | True Zero | Example |
|---|---|---|---|---|
| Nominal | No | No | No | Product category |
| Ordinal | Yes | No | No | Star rating |
| Interval | Yes | Yes | No | Temperature (°C) |
| Ratio | Yes | Yes | Yes | Revenue, age |

## Why This Matters
- You can compute a mean on ratio/interval data, but **not** meaningfully on nominal data.
- Ordinal data is often summarized with median/mode, not mean.
- Choosing the wrong chart (e.g., a line chart for nominal categories) misleads readers.

## Python Example
```python
import pandas as pd

df = pd.DataFrame({
    "region": pd.Categorical(["North", "South", "East"]),          # nominal
    "satisfaction": pd.Categorical(["Low", "High", "Medium"],
                                     categories=["Low", "Medium", "High"],
                                     ordered=True),                  # ordinal
    "revenue": [1200.5, 980.0, 1450.75]                              # ratio
})
print(df.dtypes)
```

## Business Application
A survey team correctly treats "satisfaction rating" as ordinal (using median and mode, not mean) while treating "monthly spend" as ratio data (mean, standard deviation valid) — avoiding a common analytics mistake that skews reported insights.

## Key Takeaways
- Data type dictates which statistics and visualizations are valid.
- Nominal < Ordinal < Interval < Ratio, in terms of how much mathematical operations they support.
- Misclassifying data type is one of the most common — and avoidable — analytics errors.
