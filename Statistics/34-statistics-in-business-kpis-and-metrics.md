# 34. Statistics in Business KPIs and Metrics

## Overview
Key Performance Indicators (KPIs) are statistical summaries by nature — but poorly designed KPIs can mislead just as easily as they inform. Applying statistical rigor to metric design prevents costly misinterpretation.

## Common Statistical Pitfalls in KPI Design
- **Reporting only averages**: hides variance and outliers (Topic 5) — a "$50 average order value" could mean consistent $50 orders or a mix of $10 and $200 orders.
- **Ignoring statistical significance in period-over-period comparisons**: a 3% week-over-week change in a noisy metric may be well within normal random variation, not a real signal.
- **Survivorship bias**: analyzing only customers who remain active ignores the (often more informative) customers who churned.
- **Simpson's Paradox**: a trend that appears in aggregated data can reverse or disappear when data is broken into subgroups — always check whether a KPI trend holds within key segments, not just in aggregate.

## Building Statistically Sound KPIs
- Pair every headline metric with a measure of variability or a confidence interval where feasible.
- Define clear, consistent time windows and cohorts to avoid apples-to-oranges comparisons.
- Distinguish **leading indicators** (predictive, e.g., trial sign-ups) from **lagging indicators** (outcome-confirming, e.g., churn) in a dashboard.
- Use control charts or statistical process control to distinguish genuine shifts from normal noise in a metric over time.

## Python Example
```python
import numpy as np

weekly_conversion = np.array([0.041, 0.039, 0.043, 0.038, 0.052, 0.040])
mean, std = weekly_conversion.mean(), weekly_conversion.std(ddof=1)
upper_control_limit = mean + 3*std
print("Week 5 (0.052) exceeds control limit?", 0.052 > upper_control_limit)
```

## Business Application
A subscription company notices overall retention "improved" this quarter, but a Simpson's Paradox check reveals retention actually declined in every individual customer segment — the aggregate improvement was driven purely by a mix shift toward a naturally higher-retention segment, not real improvement.

## Key Takeaways
- KPIs are statistics, and inherit all the pitfalls (averages hiding variance, misleading aggregation) that raw statistics do.
- Always check whether an aggregate trend holds within key subgroups before trusting it (Simpson's Paradox).
- Statistical process control helps distinguish a genuine metric shift from ordinary random fluctuation.
