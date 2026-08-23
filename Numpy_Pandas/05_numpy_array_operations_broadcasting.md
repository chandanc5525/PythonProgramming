# 05. Array Operations & Broadcasting

## Element-wise Arithmetic (Vectorization)

NumPy operations apply element-wise by default — no loops required. This is the core of why NumPy is fast, and the core mental model you need for writing efficient data science code.

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([10, 20, 30])

a + b     # [11 22 33]
a - b     # [-9 -18 -27]
a * b     # [10 40 90]   -- element-wise, NOT matrix multiplication
a / b     # [0.1 0.1 0.1]
a ** 2    # [1 4 9]
a % 2     # [1 0 1]
```

**Important:** `*` between two arrays is **element-wise multiplication**, not matrix multiplication. For matrix multiplication, use `@` or `np.matmul` / `np.dot` (covered in file 08).

## Scalar Broadcasting (Simplest Case)

```python
a = np.array([1, 2, 3])
a * 2        # [2 4 6]  -- scalar is "broadcast" across every element
a + 100      # [101 102 103]
```

## Broadcasting Rules (The Core Concept)

Broadcasting lets NumPy perform operations on arrays of *different but compatible* shapes without explicitly copying data. This is one of the most powerful — and most confusing for beginners — concepts in NumPy.

**The rule:** compare shapes element-wise starting from the *trailing* (rightmost) dimension. Two dimensions are compatible if:
1. They are equal, OR
2. One of them is 1

```python
# Example: (3, 4) array + (4,) array
matrix = np.ones((3, 4))       # shape (3, 4)
row = np.array([1, 2, 3, 4])   # shape (4,)

result = matrix + row
print(result.shape)   # (3, 4) -- row is broadcast across all 3 rows
```

Visualizing what happens:
```
matrix:      shape (3, 4)
row:         shape (   4)  -> treated as (1, 4), then repeated to (3, 4)
```

### Column-wise broadcasting

```python
matrix = np.ones((3, 4))
col = np.array([[1], [2], [3]])   # shape (3, 1)

result = matrix + col
print(result.shape)   # (3, 4) -- col is broadcast across all 4 columns
```

### When broadcasting fails

```python
a = np.ones((3, 4))
b = np.ones((3,))       # shape (3,) doesn't align with trailing dim 4

# a + b  --> ValueError: operands could not be broadcast together with shapes (3,4) (3,)

# Fix: reshape b to (3, 1) so it broadcasts along columns
b_fixed = b.reshape(3, 1)
a + b_fixed   # works, shape (3, 4)
```

## Practical Data Science Applications of Broadcasting

### 1. Feature normalization (standardization) — extremely common

```python
X = np.array([[1, 200],
              [2, 300],
              [3, 400]], dtype=float)

mean = X.mean(axis=0)     # shape (2,) -- mean of each column (feature)
std = X.std(axis=0)       # shape (2,)

X_normalized = (X - mean) / std   # broadcasting: (3,2) - (2,) -> (3,2)
print(X_normalized)
```

This is literally what `StandardScaler` does under the hood in scikit-learn — understanding broadcasting means you can implement or debug custom normalization logic without a library.

### 2. Min-max scaling

```python
X_min = X.min(axis=0)
X_max = X.max(axis=0)
X_scaled = (X - X_min) / (X_max - X_min)   # scales each feature to [0, 1]
```

### 3. Computing pairwise distances (used in KNN, clustering)

```python
points = np.array([[0, 0], [3, 4], [6, 8]])   # shape (3, 2)

# Broadcasting trick: (3,1,2) - (1,3,2) -> (3,3,2) pairwise differences
diffs = points[:, np.newaxis, :] - points[np.newaxis, :, :]
distances = np.sqrt((diffs ** 2).sum(axis=2))
print(distances)
# [[0.  5. 10.]
#  [5.  0.  5.]
#  [10. 5.  0.]]
```

This vectorized pairwise-distance pattern avoids nested Python loops and is the backbone of efficient KNN/clustering implementations.

## Universal Functions (ufuncs)

NumPy provides optimized, vectorized math functions ("ufuncs") that operate element-wise:

```python
arr = np.array([1, 4, 9, 16])

np.sqrt(arr)      # [1. 2. 3. 4.]
np.exp(arr)       # e^x for each element
np.log(arr)       # natural log
np.log1p(arr)     # log(1+x) -- numerically stable for small x, common in feature engineering
np.abs([-1, -2])  # [1 2]
np.sign([-5, 0, 5])   # [-1 0 1]

np.sin(arr); np.cos(arr); np.tan(arr)   # trig functions
np.round(3.456, 2)   # 3.46
np.clip(arr, 2, 10)  # clip values to range [2, 10]
```

## Comparison Operators Return Boolean Arrays

```python
a = np.array([1, 2, 3])
b = np.array([3, 2, 1])

a == b     # [False  True False]
a > b      # [False False  True]
np.array_equal(a, b)   # False -- checks if ENTIRE arrays are equal
```

## In-place Operations (Memory Efficiency)

```python
a = np.array([1.0, 2.0, 3.0])
a += 1        # modifies 'a' in place, no new array allocated
a *= 2        # in-place multiply

# Useful when working with large arrays where allocating new memory is expensive
```

**Caution:** in-place operations on integer arrays with float operands can raise casting errors or silently truncate — be explicit about dtype when doing in-place math.

**Next:** `06_numpy_mathematical_statistical_functions.md`
