# 06. Mathematical & Statistical Functions

Statistics on arrays is the daily bread of exploratory data analysis (EDA) and feature engineering. Understanding the `axis` parameter deeply is essential.

## Basic Aggregations

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

arr.sum()       # 15
arr.mean()      # 3.0
arr.std()       # 1.414... (population std, ddof=0 by default)
arr.var()       # 2.0
arr.min()       # 1
arr.max()       # 5
arr.argmin()    # 0  -- INDEX of the minimum value
arr.argmax()    # 4  -- INDEX of the maximum value
np.median(arr)  # 3.0
```

**Important:** NumPy's `.std()`/`.var()` default to `ddof=0` (population statistics). Pandas defaults to `ddof=1` (sample statistics). This is a very common source of "why do NumPy and Pandas give different std values on the same data?" confusion.

```python
# To match Pandas' sample standard deviation:
arr.std(ddof=1)
```

## The `axis` Parameter (Critical for 2D+ Data)

This is the #1 concept that trips people up. For a 2D array (rows = samples, columns = features — the standard ML convention):

- `axis=0` → operate **down the columns** (result: one value per column/feature)
- `axis=1` → operate **across the rows** (result: one value per row/sample)

```python
X = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

X.sum(axis=0)    # [12 15 18]  -- sum of each COLUMN
X.sum(axis=1)    # [ 6 15 24]  -- sum of each ROW

X.mean(axis=0)   # mean of each feature (column) -- classic normalization use case
X.mean(axis=1)   # mean of each sample (row)

X.max(axis=0)    # max value per column
X.argmax(axis=1) # index of max value within each row (e.g., predicted class per sample)
```

**Memory trick:** `axis=0` collapses rows (moves *down*), `axis=1` collapses columns (moves *across*). If you're ever unsure, test on a small array and check `.shape` of the result.

### Real-world example: getting predicted class from softmax probabilities

```python
probs = np.array([[0.1, 0.7, 0.2],
                   [0.6, 0.3, 0.1],
                   [0.2, 0.2, 0.6]])

predicted_classes = probs.argmax(axis=1)   # [1 0 2]
```

This exact pattern is used after every softmax-output classifier to convert probabilities into predicted labels.

## Cumulative Functions

```python
arr = np.array([1, 2, 3, 4])
np.cumsum(arr)    # [1 3 6 10]  -- running total
np.cumprod(arr)   # [1 2 6 24]  -- running product
```

**Use case:** cumulative sums are common for computing running totals in time series (e.g., cumulative revenue), or for computing empirical CDFs.

## Percentiles and Quantiles (EDA Staple)

```python
data = np.array([15, 22, 8, 19, 35, 42, 11, 27])

np.percentile(data, 50)     # median (50th percentile)
np.percentile(data, [25, 50, 75])   # quartiles -- classic 5-number summary component
np.quantile(data, 0.9)      # 90th percentile -- common for outlier thresholds

# IQR-based outlier detection (a standard EDA technique)
q1, q3 = np.percentile(data, [25, 75])
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
outliers = data[(data < lower_bound) | (data > upper_bound)]
```

## Correlation and Covariance

```python
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 5])

np.corrcoef(x, y)   # 2x2 correlation matrix; [0,1] and [1,0] give the correlation coefficient
np.cov(x, y)        # 2x2 covariance matrix
```

`np.corrcoef` is a fast way to check linear relationships between features before feeding them into a model — highly correlated features are candidates for removal (multicollinearity).

## Handling NaN Values in Statistics

Real-world data is full of missing values. Standard functions propagate `NaN`; the `nan*` variants ignore them:

```python
data = np.array([1, 2, np.nan, 4, 5])

data.sum()        # nan  <- one NaN poisons the whole result
np.nansum(data)   # 12.0 -- ignores NaN

np.nanmean(data)  # 3.0
np.nanstd(data)
np.nanmax(data)
np.nanmin(data)
np.isnan(data)    # [False False  True False False] -- boolean mask of NaN locations
np.count_nonzero(np.isnan(data))   # count of missing values -- common data quality check
```

**Practical pattern for a quick missing-data audit:**

```python
def missing_report(X):
    n_missing = np.isnan(X).sum(axis=0)
    pct_missing = n_missing / X.shape[0] * 100
    return n_missing, pct_missing
```

## Sorting and Ranking

```python
arr = np.array([3, 1, 4, 1, 5, 9, 2])

np.sort(arr)           # [1 1 2 3 4 5 9] -- returns a new sorted array
arr.sort()              # sorts IN PLACE

idx = np.argsort(arr)   # indices that WOULD sort the array (very useful!)
print(arr[idx])          # applying idx gives sorted order

# Sort a 2D array along a specific axis
X = np.array([[3, 1], [2, 4]])
np.sort(X, axis=0)      # sort within each column
np.sort(X, axis=1)      # sort within each row
```

`np.argsort` is essential for ranking — e.g., finding the top-k most important features by importance score, or the top-k nearest neighbors by distance.

```python
importances = np.array([0.1, 0.5, 0.05, 0.3])
top_2_idx = np.argsort(importances)[::-1][:2]   # indices of top 2 largest values
print(top_2_idx)   # [1 3]
```

**Next:** `07_numpy_reshaping_stacking_splitting.md`
