# NumPy Lecture Notes — 08: Advanced Indexing, Masking & Structured Arrays

## 1. Introduction

This lesson goes beyond basic slicing into powerful, advanced techniques: multi-dimensional fancy indexing, complex boolean logic, `np.where`/`np.select` for conditional transformations, and structured/record arrays for handling heterogeneous, labeled data.

---

## 2. Coding: Multi-Dimensional Fancy Indexing

```python
import numpy as np

matrix = np.array([[10, 20, 30],
                    [40, 50, 60],
                    [70, 80, 90]])

# Select specific (row, col) pairs
rows = np.array([0, 1, 2])
cols = np.array([2, 0, 1])
print(matrix[rows, cols])     # [30 40 80] -> (0,2), (1,0), (2,1)

# Select entire rows using an index array
print(matrix[[0, 2]])          # rows 0 and 2

# Combine fancy indexing with slicing
print(matrix[[0, 2], 1:3])     # rows 0,2, columns 1:3
```

### `np.ix_` for Cross-Product Indexing

```python
matrix = np.arange(1, 26).reshape(5, 5)

rows = [0, 2, 4]
cols = [1, 3]

# Naive fancy indexing does NOT give a sub-grid -- np.ix_ does
sub_grid = matrix[np.ix_(rows, cols)]
print(sub_grid)
# Selects the cross-product: rows {0,2,4} x cols {1,3}
```

---

## 3. Coding: Advanced Boolean Masking

```python
data = np.array([12, -5, 34, -1, 0, 45, -20, 8])

# Multiple conditions
mask = (data > 0) & (data < 40)
print(data[mask])              # [12 34  8]

# OR conditions
mask2 = (data < -10) | (data > 40)
print(data[mask2])             # [45 -20]

# NOT condition
print(data[~(data > 0)])       # [-5 -1  0 -20]

# Conditional replacement
cleaned = np.where(data < 0, 0, data)   # replace negatives with 0
print(cleaned)

# Multi-branch conditional with np.select
conditions = [data < 0, data == 0, data > 0]
choices = ["negative", "zero", "positive"]
labels = np.select(conditions, choices)
print(labels)
```

### `np.clip` — Bounding Values

```python
a = np.array([-10, 5, 50, 150, 200])
clipped = np.clip(a, 0, 100)     # clamp values to range [0, 100]
print(clipped)   # [  0   5  50 100 100]
```

### Setting Values via Masks

```python
grades = np.array([55, 82, 45, 91, 67, 38])
grades[grades < 50] = 0   # fail grades reset to 0
print(grades)              # [ 0 82  0 91 67  0]
```

---

## 4. Coding: Structured (Record) Arrays

```python
# Define a structured dtype -- like a lightweight table
dt = np.dtype([('name', 'U10'), ('age', 'i4'), ('salary', 'f8')])

employees = np.array([
    ('Alice', 29, 75000.0),
    ('Bob', 35, 82000.0),
    ('Carol', 41, 91000.0)
], dtype=dt)

print(employees['name'])          # ['Alice' 'Bob' 'Carol']
print(employees['salary'].mean()) # average salary
print(employees[employees['age'] > 30])   # filter rows like a mini-database
```

---

## 5. Use Cases & Scenarios

1. **Data cleaning**: Using boolean masks to detect and replace missing/invalid sensor readings (e.g., replacing all `-999` error codes with `NaN`).
2. **Image segmentation**: Masking pixels of an image matching a specific color/intensity range for object detection.
3. **Grading/scoring pipelines**: Using `np.select` to assign letter grades (A/B/C/D/F) based on numeric score ranges in one vectorized operation.
4. **Outlier capping**: Using `np.clip` to bound extreme financial or sensor values (winsorization) before statistical analysis.
5. **Lightweight tabular data**: Using structured arrays for fast, typed record storage when a full Pandas DataFrame is unnecessary overhead.

### Real-World Scenario

> An environmental monitoring system collects temperature readings, but faulty sensors occasionally report `-999` as an error code. A data engineer uses boolean masking to identify and replace all error codes with `np.nan`, then uses `np.nanmean` to compute statistics while safely ignoring the missing values.

```python
readings = np.array([22.5, 23.1, -999, 21.8, -999, 24.0, 22.9])

# Replace sentinel error values with NaN
cleaned = np.where(readings == -999, np.nan, readings)
print(cleaned)

# Compute statistics ignoring NaNs
print("Mean (ignoring errors):", np.nanmean(cleaned))
print("Valid readings count:", np.sum(~np.isnan(cleaned)))
```

---

## 6. Practice Problems

1. Given a `5x5` matrix of numbers `1-25`, use `np.ix_` to extract the sub-grid formed by rows `[1,3]` and columns `[0,2,4]`.
2. Given `data = np.array([5, -3, 12, -8, 0, 19, -1])`, use boolean masking to set all negative values to `-1` and all positive values to `1` (keep zero as `0`). Hint: use `np.select` or nested `np.where`.
3. Use `np.clip` to bound an array of temperature readings between `-10` and `40` degrees.
4. **Scenario**: You have exam scores `[45, 88, 72, 91, 33, 67, 58, 95]`. Use `np.select` to assign letter grades: `>=90: 'A'`, `>=75: 'B'`, `>=60: 'C'`, `else: 'F'`.
5. Create a structured array representing 4 products with fields `name` (string), `price` (float), and `quantity` (int). Compute the total inventory value (`sum(price * quantity)`).
6. Given a dataset with sentinel error values of `-1`, replace them with `np.nan` and compute the mean, ignoring NaNs, using `np.nanmean`.
7. **Challenge**: Given a `(100, 100)` grayscale image array with pixel values 0-255, create a binary mask marking all "bright" pixels (value > 200) as `True`. Count how many bright pixels exist using `np.sum()` on the mask.
