# 16. Data Cleaning & Handling Missing Data

Real-world datasets are messy. This is arguably where data scientists spend the largest share of their actual time — surveys consistently suggest 60-80% of a data science project is data cleaning and preparation.

## Detecting Missing Data

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'a': [1, 2, np.nan, 4],
    'b': [np.nan, 2, 3, 4],
    'c': ['x', 'y', 'z', None]
})

df.isnull()               # boolean DataFrame, True where missing
df.isnull().sum()          # count of missing values PER COLUMN -- essential first check
df.isnull().sum() / len(df) * 100   # percentage missing per column
df.isnull().any()          # which columns have ANY missing values
df.isnull().values.any()   # is there ANY missing value anywhere in the whole DataFrame?

# Visualize missingness quickly
df.isnull().sum().sort_values(ascending=False)
```

**Standard first step on any new dataset:**

```python
def missing_summary(df):
    total = df.isnull().sum()
    pct = (total / len(df) * 100).round(2)
    return pd.DataFrame({'missing_count': total, 'missing_pct': pct}).sort_values('missing_count', ascending=False)

print(missing_summary(df))
```

## Dropping Missing Data

```python
df.dropna()                        # drop ANY row containing at least one NaN
df.dropna(axis=1)                  # drop any COLUMN containing at least one NaN
df.dropna(subset=['a'])            # drop rows where SPECIFICALLY column 'a' is NaN
df.dropna(thresh=2)                 # keep rows with at least 2 non-null values
df.dropna(how='all')                # drop rows only if ALL values are NaN
```

**Caution:** `dropna()` with defaults can silently discard a large fraction of your dataset if missingness is spread across many columns. Always check `df.isnull().sum()` and the resulting row count before and after dropping.

## Filling Missing Data (Imputation)

```python
df.fillna(0)                                  # fill all NaN with a constant
df['a'].fillna(df['a'].mean())                 # fill with column mean -- common for numeric features
df['a'].fillna(df['a'].median())               # median -- more robust to outliers than mean
df['c'].fillna(df['c'].mode()[0])               # fill categorical with the most frequent value

df.fillna(method='ffill')                       # forward-fill: propagate last valid value forward
df.fillna(method='bfill')                       # backward-fill: propagate next valid value backward

# Different fill value per column
df.fillna({'a': 0, 'b': df['b'].mean()})

# Interpolation (great for time series / naturally ordered numeric gaps)
df['a'].interpolate(method='linear')
```

**Choosing an imputation strategy (data science judgment call):**
- **Mean**: simple, works well for roughly normal, low-outlier numeric data
- **Median**: more robust when the column has outliers/skew
- **Mode**: standard for categorical columns
- **Forward/backward fill**: appropriate for ordered/time series data where "last known value" is a reasonable assumption
- **Model-based imputation** (e.g., `sklearn.impute.KNNImputer` or `IterativeImputer`): more sophisticated, used when missingness is substantial and simple imputation would distort relationships

Always ask: **is this data "missing at random," or is missingness itself informative** (e.g., a survey skip pattern)? In the latter case, consider adding a binary "was_missing" indicator column before imputing.

```python
df['a_was_missing'] = df['a'].isnull().astype(int)
df['a'] = df['a'].fillna(df['a'].median())
```

## Replacing Values

```python
df.replace(-999, np.nan)                 # replace a sentinel "missing" code with proper NaN
df.replace({'a': {1: 100, 2: 200}})       # column-specific value mapping
df['c'].replace({'x': 'X', 'y': 'Y'})     # replace specific categorical labels
```

## Removing Duplicates

```python
df.duplicated()                     # boolean mask -- True for duplicate rows (after the first occurrence)
df.duplicated().sum()                # count of duplicate rows
df.drop_duplicates()                  # remove exact duplicate rows
df.drop_duplicates(subset=['a'])      # remove duplicates based on specific column(s) only
df.drop_duplicates(keep='last')        # keep the LAST occurrence instead of the first
```

## Fixing Data Types

```python
df['a'] = df['a'].astype(float)
df['id'] = df['id'].astype(str)                  # IDs should usually be strings, not numeric
df['date'] = pd.to_datetime(df['date'])           # parse strings into proper datetime objects
df['price'] = pd.to_numeric(df['price'], errors='coerce')   # invalid values become NaN instead of crashing
```

`errors='coerce'` is extremely useful for cleaning: it converts anything that can't be parsed into `NaN` rather than raising an exception, letting you handle bad values through the normal missing-data workflow.

## String Cleaning (`.str` accessor)

```python
df['name'] = df['name'].str.strip()               # remove leading/trailing whitespace
df['name'] = df['name'].str.lower()                # normalize case
df['name'] = df['name'].str.replace('_', ' ')       # replace characters
df['name'] = df['name'].str.title()                 # "john smith" -> "John Smith"

# Extract structured info with regex
df['area_code'] = df['phone'].str.extract(r'\((\d{3})\)')
df['has_digit'] = df['name'].str.contains(r'\d', regex=True)
```

Inconsistent capitalization, stray whitespace, and inconsistent categorical labels (`"USA"` vs `"U.S.A."` vs `"United States"`) are among the most common real-world data quality issues — `.str` cleaning should be a standard part of your EDA checklist for any text/categorical column.

## Outlier Detection (Common Cleaning Step)

```python
# Z-score method
from scipy import stats
z_scores = np.abs(stats.zscore(df['a'].dropna()))
outliers = df['a'][z_scores > 3]

# IQR method (more robust, doesn't assume normality)
Q1, Q3 = df['a'].quantile([0.25, 0.75])
IQR = Q3 - Q1
lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
outliers = df[(df['a'] < lower) | (df['a'] > upper)]

# Capping/winsorizing instead of dropping
df['a'] = df['a'].clip(lower=lower, upper=upper)
```

**Next:** `17_pandas_groupby_aggregation.md`
