# NumPy Lecture Notes — 05: Mathematical & Statistical Functions

## 1. Introduction

NumPy provides an extensive library of mathematical, statistical, and trigonometric functions optimized for array-wide computation. This lesson covers descriptive statistics, mathematical transforms, sorting, and set operations — the toolbox used constantly in data analysis and scientific computing.

---

## 2. Coding: Descriptive Statistics

```python
import numpy as np

data = np.array([23, 45, 12, 67, 34, 89, 21, 56])

print("Mean:", np.mean(data))
print("Median:", np.median(data))
print("Std Dev:", np.std(data))
print("Variance:", np.var(data))
print("Min/Max:", np.min(data), np.max(data))
print("Range:", np.ptp(data))          # max - min
print("Percentile (25th):", np.percentile(data, 25))
print("Percentile (75th):", np.percentile(data, 75))

# Index of min/max
print("Argmax:", np.argmax(data))       # index of largest value
print("Argmin:", np.argmin(data))       # index of smallest value
```

### 2D Statistics with Axis Control

```python
matrix = np.array([[10, 20, 30],
                    [40, 50, 60],
                    [70, 80, 90]])

print(np.mean(matrix, axis=0))   # column-wise mean
print(np.mean(matrix, axis=1))   # row-wise mean
print(np.std(matrix))             # overall std dev
```

---

## 3. Coding: Mathematical Functions

```python
a = np.array([1, 2, 3, 4, 5])

# Trigonometric
print(np.sin(a))
print(np.cos(a))
print(np.tan(a))

# Exponential and logarithmic
print(np.exp(a))       # e^x
print(np.log(a))       # natural log
print(np.log2(a))      # base-2 log
print(np.log10(a))     # base-10 log

# Rounding
b = np.array([1.234, 5.678, 9.999])
print(np.round(b, 1))    # [1.2 5.7 10. ]
print(np.floor(b))        # [1. 5. 9.]
print(np.ceil(b))         # [2. 6. 10.]
print(np.trunc(b))        # [1. 5. 9.]

# Sums and products
print(np.sum(a))
print(np.prod(a))
print(np.cumsum(a))    # cumulative sum: [1 3 6 10 15]
print(np.cumprod(a))   # cumulative product: [1 2 6 24 120]
```

---

## 4. Coding: Sorting & Searching

```python
a = np.array([34, 12, 78, 3, 90, 21])

print(np.sort(a))               # [ 3 12 21 34 78 90]
print(np.argsort(a))            # indices that would sort the array

# Sorting 2D arrays
matrix = np.array([[3, 1], [2, 4], [0, 5]])
print(np.sort(matrix, axis=0))  # sort each column
print(np.sort(matrix, axis=1))  # sort each row

# Searching
print(np.where(a > 30))          # indices where condition is True
print(np.where(a > 30, 1, 0))    # replace: 1 if >30 else 0

# Unique values & set operations
b = np.array([1, 2, 2, 3, 3, 3, 4])
print(np.unique(b))               # [1 2 3 4]
print(np.unique(b, return_counts=True))  # values + counts

set1 = np.array([1, 2, 3, 4])
set2 = np.array([3, 4, 5, 6])
print(np.intersect1d(set1, set2))   # [3 4]
print(np.union1d(set1, set2))       # [1 2 3 4 5 6]
print(np.setdiff1d(set1, set2))     # [1 2]
```

---

## 5. Use Cases & Scenarios

1. **A/B testing analysis**: Computing means and standard deviations of conversion rates for two test groups to determine statistical significance.
2. **Anomaly detection**: Using percentiles (e.g., values beyond the 99th percentile) to flag outliers in sensor or transaction data.
3. **Signal processing**: Applying `np.sin`/`np.cos` to generate or analyze waveforms in audio or radio signal applications.
4. **Leaderboard/ranking systems**: Using `np.argsort` to rank players by score while retaining original index references.
5. **Deduplication**: Using `np.unique` to identify distinct customer IDs from a large transaction log.

### Real-World Scenario

> A quality-control engineer at a manufacturing plant records daily defect counts per production line. Using NumPy, they compute the mean and standard deviation of defects, then use `np.where` to flag any day where defects exceeded "mean + 2*std" as a statistical anomaly requiring investigation.

```python
defects = np.array([12, 15, 11, 14, 45, 13, 16, 12, 50, 14])

mean = np.mean(defects)
std = np.std(defects)
threshold = mean + 2 * std

anomaly_flags = np.where(defects > threshold, "ANOMALY", "normal")
print("Threshold:", threshold)
print(anomaly_flags)
```

---

## 6. Practice Problems

1. Given `data = np.array([4, 8, 15, 16, 23, 42])`, compute mean, median, variance, and standard deviation.
2. Create a `5x5` matrix of random integers (1–100) and find the row-wise and column-wise maximum values.
3. Use `np.argsort` to sort a list of student names by their corresponding scores array, without directly sorting the names array. (Hint: use the sorted indices to index into the names array.)
4. Given two arrays of customer IDs from two different marketing campaigns, find: (a) customers who received both campaigns, (b) customers unique to campaign A.
5. **Scenario**: You have a year of daily website traffic data (365 values). Use `np.percentile` to determine the traffic value at the 90th percentile — representing your "high-traffic day" threshold.
6. Round the array `np.array([2.567, 8.123, 4.999, 1.001])` to 0, 1, and 2 decimal places. Compare with `floor` and `ceil`.
7. **Challenge**: Write code that computes the Z-score (`(x - mean) / std`) for every element in a dataset, then use boolean masking to extract all values with a Z-score greater than 2 (common outlier detection technique).
