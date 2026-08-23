# 19. Time Series Analysis

Time series data (sales over time, sensor readings, stock prices, user activity logs) is extremely common in data science, and Pandas has first-class, extensive support for it that goes far beyond what plain NumPy offers.

## Parsing Dates

```python
import pandas as pd

df = pd.DataFrame({'date': ['2024-01-01', '2024-01-02', '2024-01-03'], 'sales': [100, 150, 130]})

df['date'] = pd.to_datetime(df['date'])       # convert string column to datetime64
df.dtypes    # date is now datetime64[ns]

# Parsing with a specific format (faster and safer for non-standard formats)
pd.to_datetime(df['date'], format='%Y-%m-%d')

# Handling parse errors gracefully
pd.to_datetime(['2024-01-01', 'not a date'], errors='coerce')  # invalid becomes NaT
```

`NaT` ("Not a Time") is the datetime equivalent of `NaN` — represents missing/invalid timestamps and is handled by the same `isnull()`/`dropna()`/`fillna()` machinery.

## The DatetimeIndex — Unlocking Time Series Superpowers

```python
df = df.set_index('date')     # promote date column to be the index

df.index                       # DatetimeIndex(['2024-01-01', '2024-01-02', '2024-01-03'], ...)

# Once the index is a DatetimeIndex, powerful slicing becomes available:
df['2024-01']                  # all rows in January 2024
df['2024-01-01':'2024-01-02']  # date range slicing, inclusive
```

## Extracting Date Components

```python
df = df.reset_index()
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['day_of_week'] = df['date'].dt.day_name()    # 'Monday', 'Tuesday', ...
df['is_weekend'] = df['date'].dt.dayofweek >= 5
df['quarter'] = df['date'].dt.quarter
df['week_of_year'] = df['date'].dt.isocalendar().week
```

The `.dt` accessor is the datetime equivalent of the `.str` accessor — the standard, vectorized way to extract date/time features for use in ML models (day-of-week seasonality, month, is_holiday flags, etc.).

## Resampling — Changing the Time Frequency

Resampling aggregates time series data into a different frequency (e.g., daily data into monthly summaries) — conceptually a specialized `groupby` for time.

```python
df = df.set_index('date')

df['sales'].resample('D').sum()      # daily totals (if data has sub-daily granularity)
df['sales'].resample('W').sum()      # weekly totals
df['sales'].resample('ME').sum()     # month-end totals
df['sales'].resample('QE').mean()    # quarterly averages
df['sales'].resample('YE').sum()     # yearly totals

# Multiple aggregations at once
df['sales'].resample('ME').agg(['sum', 'mean', 'std'])
```

**Common frequency codes:** `D` (day), `W` (week), `ME` (month end), `QE` (quarter end), `YE` (year end), `h` (hour), `min` (minute).

**Data science use case:** resampling is the standard first step in almost any time series forecasting or trend-analysis project — e.g., converting raw per-transaction data into daily/weekly aggregated sales before modeling.

## Rolling Windows (Moving Averages)

```python
df['sales_7day_avg'] = df['sales'].rolling(window=7).mean()
df['sales_7day_std'] = df['sales'].rolling(window=7).std()
df['sales_cumulative'] = df['sales'].cumsum()

# Rolling with a minimum period requirement (avoids NaN at the very start)
df['sales'].rolling(window=7, min_periods=1).mean()
```

**Data science use case:** rolling averages are the standard technique for smoothing noisy time series to reveal trends, and are a core feature-engineering technique for time series forecasting models (e.g., "7-day rolling average" as a predictor feature).

## Expanding Windows (Cumulative Statistics)

```python
df['sales'].expanding().mean()    # running average from the start up to each point
df['sales'].expanding().max()     # running maximum seen so far
```

**Use case:** useful for "running total" or "best score so far" type features, and for detecting cumulative drift in monitoring dashboards.

## Shifting and Lagging (Critical for Forecasting Features)

```python
df['sales_prev_day'] = df['sales'].shift(1)         # lag by 1 period -- previous day's value
df['sales_next_day'] = df['sales'].shift(-1)          # lead by 1 period -- next day's value
df['sales_change'] = df['sales'] - df['sales'].shift(1)   # day-over-day change
df['sales_pct_change'] = df['sales'].pct_change()          # percentage change

df['sales_yoy_change'] = df['sales'] - df['sales'].shift(365)  # year-over-year (daily data)
```

**Data science use case:** lag features (`shift()`) are the fundamental building block of time series forecasting models — a model predicting tomorrow's sales typically uses yesterday's sales, last week's sales, etc. as input features. Getting shift direction right (and avoiding "leaking" future information into training data) is critical for valid forecasting models.

## Handling Irregular / Missing Time Steps

```python
full_range = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='D')
df = df.set_index('date').reindex(full_range)
df.index.name = 'date'

# Now missing days show up explicitly as NaN and can be handled deliberately
df['sales'] = df['sales'].fillna(0)      # e.g., no sales recorded = 0 sales
```

Real-world time series frequently have gaps (a sensor was offline, a store was closed). Reindexing against a complete, regular date range makes these gaps explicit rather than silently absent — essential before applying rolling windows or resampling, which assume regular spacing.

## Timezone Handling

```python
df['date'] = df['date'].dt.tz_localize('UTC')            # assign a timezone to naive datetimes
df['date_local'] = df['date'].dt.tz_convert('America/New_York')   # convert to another timezone
```

Timezone bugs are a classic, subtle source of off-by-one-day errors in time series data collected from multiple regions — always explicitly localize/convert timezones rather than assuming naive timestamps are unambiguous.

**Next:** `20_pandas_advanced_performance_real_world_workflows.md`
