# 37. Forecasting for Business Planning

## Overview
Forecasting extends time series analysis (Topic 29) into the future, giving businesses the quantitative basis for budgeting, staffing, and inventory decisions.

## Common Forecasting Approaches
- **Moving averages**: smooths short-term fluctuations to reveal underlying trend; simple but lags behind sudden changes.
- **Exponential smoothing (e.g., Holt-Winters)**: weights recent observations more heavily than older ones, and can explicitly model trend and seasonality.
- **ARIMA (AutoRegressive Integrated Moving Average)**: models a time series using its own past values (autoregression) and past forecast errors (moving average), after making it stationary (integration/differencing).
- **Regression-based forecasting**: models the target as a function of external predictors (e.g., forecasting sales from ad spend, price, and seasonality dummy variables), useful when external drivers matter more than the series' own history.

## Evaluating Forecast Accuracy
- **MAE (Mean Absolute Error)**: average absolute difference between forecast and actual, in original units.
- **MAPE (Mean Absolute Percentage Error)**: MAE expressed as a percentage — easier to communicate to business stakeholders.
- **RMSE (Root Mean Squared Error)**: penalizes large errors more heavily than MAE — useful when big misses are especially costly.

## Best Practices
- Always validate on a **holdout period** (data not used to fit the model) — never evaluate accuracy only on the training period.
- Provide a **forecast interval**, not just a point forecast — communicates the growing uncertainty of predictions further into the future.
- Re-forecast regularly as new data arrives; don't treat a forecast as a one-time, static artifact.

## Python Example
```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pandas as pd

sales = pd.Series([100,105,98,110,120,115,130,140,135,150],
                   index=pd.date_range("2024-01-01", periods=10, freq="M"))

model = ExponentialSmoothing(sales, trend="add", seasonal=None).fit()
forecast = model.forecast(3)
print(forecast)
```

## Business Application
A finance team uses Holt-Winters exponential smoothing on 3 years of monthly revenue to produce next-quarter forecasts with confidence intervals, directly informing headcount and budget planning rather than relying on a flat "grow 10%" assumption.

## Key Takeaways
- Different forecasting methods suit different data patterns — match the method to whether trend, seasonality, and external drivers matter.
- Always validate forecast accuracy on a holdout period, and report an interval, not just a single number.
- Forecasting is an ongoing process, not a one-time deliverable — models should be refreshed as new data arrives.
