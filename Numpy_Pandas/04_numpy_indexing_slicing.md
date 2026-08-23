# 04. Indexing and Slicing

Indexing is how you *select* subsets of data — arguably the skill you'll use most often as a data scientist, whether slicing feature matrices, selecting train/test splits, or filtering outliers.

## Basic Indexing (1D)

```python
import numpy as np

a = np.array([10, 20, 30, 40, 50])

a[0]        # 10
a[-1]       # 50 (last element)
a[1:3]      # [20, 30]  (stop is exclusive)
a[:3]       # [10, 20, 30]
a[::2]      # [10, 30, 50]  (every 2nd element)
a[::-1]     # [50, 40, 30, 20, 10]  (reversed)
```

## 2D Indexing (Rows and Columns)

```python
b = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

b[0]          # first row: [1, 2, 3]
b[0, 0]       # single element: 1  (preferred over b[0][0] -- faster, one lookup)
b[:, 0]       # first column: [1, 4, 7]
b[1:, :2]     # rows 1+, first 2 columns: [[4, 5], [7, 8]]
b[-1, -1]     # bottom-right element: 9
```

**Practical tip:** `b[0, 0]` and `b[0][0]` give the same result, but `b[0, 0]` is faster and more idiomatic — it does a single indexing operation instead of creating an intermediate array with `b[0]` first.

## Boolean (Mask) Indexing

The single most-used indexing technique in real data science work — this is how you **filter data based on a condition**.

```python
arr = np.array([1, -2, 3, -4, 5, -6])

mask = arr > 0
print(mask)          # [ True False  True False  True False]
print(arr[mask])     # [1 3 5]

# Inline (most common pattern)
print(arr[arr > 0])  # [1 3 5]

# Combining conditions -- use & | ~ (NOT `and`/`or`/`not`), and always use parentheses
print(arr[(arr > -5) & (arr < 5)])   # [1 -2 3 -4]
print(arr[(arr < 0) | (arr > 4)])    # [-2 -4 5 -6]
print(arr[~(arr > 0)])               # [-2 -4 -6]  -- negation
```

**Common real-world use:** removing outliers, filtering rows matching a business rule, or selecting a subset of samples matching a class label:

```python
scores = np.array([55, 90, 42, 88, 71, 33])
labels = np.array(['fail', 'pass', 'fail', 'pass', 'pass', 'fail'])

passing_scores = scores[scores >= 60]
print(passing_scores)   # [90 88 71]

# Using labels to select
print(scores[labels == 'pass'])   # [90 88 71]
```

### Modifying values via boolean mask (very common in cleaning)

```python
data = np.array([1, -999, 3, -999, 5])
data[data == -999] = np.nan   # replace sentinel "missing" values with NaN
```

## Fancy Indexing (Index Arrays)

Select multiple, arbitrary, non-contiguous indices at once:

```python
arr = np.array([10, 20, 30, 40, 50])
idx = [0, 2, 4]
print(arr[idx])        # [10 30 50]

# 2D fancy indexing
b = np.array([[1,2,3],[4,5,6],[7,8,9]])
print(b[[0, 2]])        # rows 0 and 2: [[1,2,3],[7,8,9]]
print(b[[0, 1], [1, 2]]) # element-wise pairs: b[0,1] and b[1,2] -> [2, 6]
```

**Data science use case:** fancy indexing with a list of indices is exactly how you implement train/test splits manually, or select a specific subset of samples (e.g., misclassified examples) by their row indices.

```python
# Shuffling and splitting a dataset manually
n = 100
indices = np.arange(n)
np.random.default_rng(0).shuffle(indices)

train_idx, test_idx = indices[:80], indices[80:]
X_train, X_test = X[train_idx], X[test_idx]
```

## `np.where` — Conditional Selection and Value Replacement

```python
arr = np.array([1, -2, 3, -4, 5])

# Get indices where condition is True
idx = np.where(arr < 0)
print(idx)              # (array([1, 3]),)

# Ternary-style replacement: where(condition, if_true, if_false)
result = np.where(arr < 0, 0, arr)
print(result)           # [1 0 3 0 5] -- clip negative values to 0

# Common ML preprocessing pattern: binarize based on a threshold
predictions = np.array([0.2, 0.8, 0.4, 0.9])
labels = np.where(predictions > 0.5, 1, 0)
print(labels)           # [0 1 0 1]
```

## `np.select` — Multiple Conditions

```python
arr = np.array([5, 15, 25, 35])
conditions = [arr < 10, arr < 20, arr < 30]
choices = ['low', 'medium', 'high']
result = np.select(conditions, choices, default='very high')
print(result)   # ['low' 'medium' 'high' 'very high']
```

Useful for bucketing/binning continuous variables into categorical labels (feature engineering).

## Setting Values with Slices

```python
a = np.arange(10)
a[2:5] = 0             # broadcast a single value across a slice
print(a)                # [0 1 0 0 0 5 6 7 8 9]

a[2:5] = [100, 200, 300]   # assign matching-length array
print(a)                    # [0 1 100 200 300 5 6 7 8 9]
```

**Next:** `05_numpy_array_operations_broadcasting.md`
