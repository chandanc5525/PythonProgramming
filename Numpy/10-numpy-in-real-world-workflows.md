# NumPy Lecture Notes — 10: NumPy in Real-World Data Science & ML Workflows

## 1. Introduction

This capstone lesson ties everything together, showing how NumPy underpins the entire modern data/ML stack — as the shared array format between Pandas, Matplotlib, scikit-learn, and deep learning frameworks. It also covers essential production-readiness topics: handling missing data, file I/O, and integration patterns.

---

## 2. Coding: NumPy + Pandas Interoperability

```python
import numpy as np
import pandas as pd

# Pandas DataFrames are built on top of NumPy arrays
df = pd.DataFrame({
    'age': [25, 32, 47, 51],
    'salary': [50000, 64000, 82000, 91000]
})

# Extract underlying NumPy array
arr = df.values          # or df.to_numpy()
print(type(arr))          # <class 'numpy.ndarray'>

# NumPy functions work directly on DataFrame columns (they're array-backed)
print(np.mean(df['salary']))
print(np.corrcoef(df['age'], df['salary']))   # correlation matrix
```

---

## 3. Coding: Handling Missing Data (`NaN`)

```python
data = np.array([1.0, 2.0, np.nan, 4.0, np.nan, 6.0])

print(np.isnan(data))                # boolean mask of missing values
print(np.sum(np.isnan(data)))         # count missing values

# Safe statistics that ignore NaN
print(np.nanmean(data))
print(np.nansum(data))
print(np.nanstd(data))

# Impute missing values with the mean
mean_val = np.nanmean(data)
imputed = np.where(np.isnan(data), mean_val, data)
print(imputed)
```

---

## 4. Coding: File I/O with NumPy

```python
a = np.array([[1, 2, 3], [4, 5, 6]])

# Native binary format (fast, preserves dtype/shape exactly)
np.save('array.npy', a)
loaded = np.load('array.npy')

# Multiple arrays in one compressed file
np.savez('arrays.npz', first=a, second=a * 2)
data = np.load('arrays.npz')
print(data['first'], data['second'])

# Plain text / CSV (human-readable, slower, loses exact dtype info)
np.savetxt('array.csv', a, delimiter=',')
loaded_csv = np.loadtxt('array.csv', delimiter=',')
```

---

## 5. Coding: NumPy as the ML Foundation

```python
# A minimal "from scratch" gradient descent for linear regression
# demonstrates how ML libraries use NumPy under the hood

rng = np.random.default_rng(42)
X = rng.uniform(0, 10, 100)
true_slope, true_intercept = 3.5, 2.0
y = true_slope * X + true_intercept + rng.normal(0, 1, 100)  # add noise

# Initialize parameters
m, b = 0.0, 0.0
learning_rate = 0.01
epochs = 500
n = len(X)

for epoch in range(epochs):
    y_pred = m * X + b
    error = y_pred - y

    grad_m = (2/n) * np.dot(error, X)
    grad_b = (2/n) * np.sum(error)

    m -= learning_rate * grad_m
    b -= learning_rate * grad_b

print(f"Learned slope: {m:.2f} (true: {true_slope})")
print(f"Learned intercept: {b:.2f} (true: {true_intercept})")
```

This example shows precisely why frameworks like scikit-learn, TensorFlow, and PyTorch are built atop (or inspired by) NumPy's array semantics — vectorized gradient computation is the computational core of virtually all ML training loops.

---

## 6. Use Cases & Scenarios

1. **End-to-end ML pipeline**: Raw CSV → Pandas cleaning → `.to_numpy()` → NumPy preprocessing (normalization, splitting) → scikit-learn model training.
2. **Scientific research data archiving**: Saving experiment results as `.npy`/`.npz` files for fast, exact reloading (preserving dtype and shape, unlike CSV).
3. **Computer vision pipelines**: Images loaded via OpenCV/PIL become NumPy arrays; all preprocessing (resizing math, normalization, augmentation) happens through NumPy before reaching a neural network.
4. **A/B test and survey analysis**: Combining `np.nanmean` and masking to handle incomplete survey responses without discarding entire records.
5. **Reproducible research**: Using `.npz` archives to package model weights, hyperparameters, and evaluation arrays together for reproducibility.

### Real-World Scenario

> A healthcare analytics team receives patient vital-sign data with occasional missing readings due to sensor dropout. They load the data into Pandas, convert relevant columns to NumPy arrays, use `np.isnan()` to identify gaps, and apply `np.nanmean()`-based imputation before feeding the cleaned array into a risk-prediction model. The processed arrays are then saved as `.npz` archives for the model training team, ensuring exact numerical reproducibility across environments.

```python
patient_data = pd.DataFrame({
    'heart_rate': [72, 75, np.nan, 80, 68, np.nan, 74],
    'blood_pressure': [120, 122, 118, np.nan, 121, 119, 123]
})

arr = patient_data.to_numpy()
missing_mask = np.isnan(arr)

# Column-wise mean imputation
col_means = np.nanmean(arr, axis=0)
inds = np.where(missing_mask)
arr[inds] = np.take(col_means, inds[1])

print(arr)
np.savez('cleaned_patient_data.npz', data=arr, columns=patient_data.columns.to_numpy())
```

---

## 7. Practice Problems

1. Create a Pandas DataFrame with 3 numeric columns, convert it to a NumPy array with `.to_numpy()`, and compute the correlation matrix using `np.corrcoef` (note: `corrcoef` expects variables as rows, so you may need `.T`).
2. Given an array with missing values `np.array([10, np.nan, 30, np.nan, 50])`, count how many values are missing and compute the mean using both `np.mean` (observe the `NaN` result) and `np.nanmean` (observe the correct result).
3. Save a `5x5` random array to a `.npy` file, then load it back and verify with `np.array_equal()` that the loaded array matches the original exactly.
4. Implement mean-imputation from scratch: given a dataset with missing values in multiple columns, replace each missing value with that column's mean (no loops over individual missing values — use `np.where` and `np.isnan`).
5. **Scenario**: You are given 200 noisy `(x, y)` data points believed to follow a linear relationship. Implement gradient descent from scratch (as shown above) to estimate the slope and intercept, and compare your result to `np.polyfit(x, y, 1)`.
6. Save two related arrays (`features` and `labels`) together into a single compressed `.npz` file, then reload both and verify their shapes match the originals.
7. **Capstone Challenge**: Build a small end-to-end pipeline — generate synthetic data with `np.random`, introduce artificial missing values, clean it with `np.isnan`/`np.nanmean`, normalize it with broadcasting, and finally implement a simple NumPy-only k-nearest-neighbors classifier using vectorized distance calculations (no `sklearn`).

---

## Series Summary

| # | Topic | Core Skills |
|---|---|---|
| 01 | Introduction & Array Basics | ndarray fundamentals, attributes |
| 02 | Array Creation & Dtypes | Creation functions, memory-efficient typing |
| 03 | Indexing, Slicing, Reshaping | Views vs copies, fancy indexing |
| 04 | Operations & Broadcasting | Vectorization, shape compatibility rules |
| 05 | Math & Statistical Functions | Descriptive stats, sorting, set ops |
| 06 | Linear Algebra | Matrix ops, decompositions, solving systems |
| 07 | Random Module & Simulations | Distributions, Monte Carlo methods |
| 08 | Advanced Indexing & Masking | Boolean logic, structured arrays |
| 09 | Performance Optimization | Vectorization patterns, memory layout |
| 10 | Real-World Workflows | Pandas/ML integration, missing data, I/O |

This completes a full basic-to-advanced NumPy curriculum suitable for interview preparation, coursework, or professional reference.
