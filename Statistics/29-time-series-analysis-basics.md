# 29. Time Series Analysis Basics

## Overview
Time series data — observations indexed by time (daily sales, monthly revenue, hourly traffic) — has structure that standard cross-sectional statistical methods ignore: trend, seasonality, and autocorrelation.

## Core Components of a Time Series
- **Trend**: long-term upward or downward movement.
- **Seasonality**: regular, repeating patterns tied to the calendar (weekly, monthly, yearly).
- **Cyclical patterns**: longer-term fluctuations not tied to a fixed calendar period (e.g., economic cycles).
- **Noise/residual**: the unpredictable remainder after removing trend and seasonality.

## Decomposition
Time series decomposition splits a series into these components (additive: y = trend + seasonality + residual, or multiplicative: y = trend × seasonality × residual) — essential for understanding what's actually driving movement in a metric.

## Stationarity
Many time series models require the data to be **stationary** — statistical properties (mean, variance) don't change over time. Non-stationary data is often made stationary via **differencing** (subtracting the previous value). Test with the **Augmented Dickey-Fuller (ADF) test**.

## Autocorrelation
Time series values are often correlated with their own past values (autocorrelation) — a key structural difference from independent cross-sectional data, and the basis for models like ARIMA (Topic 37).

## Python Example
```python
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

dates = pd.date_range("2023-01-01", periods=104, freq="W")
sales = pd.Series(100 + 0.5*range(104) + 15*pd.Series(range(104)).apply(lambda x: (x % 52 < 26)*10),
                   index=dates)

decomposition = seasonal_decompose(sales, model="additive", period=52)
# decomposition.trend, .seasonal, .resid available for plotting/analysis
```

## Business Application
A retailer decomposes two years of weekly sales data to separate a genuine upward growth trend from seasonal holiday spikes — preventing them from mistakenly attributing a temporary seasonal bump to a marketing campaign's lasting impact.

## Key Takeaways
- Time series data has structure (trend, seasonality, autocorrelation) that must be explicitly modeled, not ignored.
- Decomposition separates a metric's movement into interpretable components before drawing business conclusions.
- Stationarity is often a prerequisite for classical time series forecasting models.
