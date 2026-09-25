# NumPy Lecture Notes — 04: Array Operations & Broadcasting

## 1. Introduction

**Vectorization** is NumPy's core performance principle: apply operations to entire arrays at once instead of looping element-by-element. **Broadcasting** extends this further, allowing operations between arrays of *different shapes* by implicitly expanding the smaller array to match the larger one — without actually copying data in memory.

---

## 2. Coding: Element-wise Operations

```python
import numpy as np

a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

print(a + b)     # [11 22 33 44]
print(a - b)     # [-9 -18 -27 -36]
print(a * b)     # [10 40 90 160]
print(a / b)     # [0.1 0.1 0.1 0.1]
print(a ** 2)    # [1 4 9 16]
print(a % 2)     # [1 0 1 0]

# Scalar operations
print(a + 10)    # [11 12 13 14]
print(a * 2)     # [2 4 6 8]

# Comparison operators (return boolean arrays)
print(a > 2)     # [False False  True  True]
print(a == b/10) # [ True  True  True  True]
```

### Universal Functions (ufuncs)

```python
a = np.array([1, 4, 9, 16])

print(np.sqrt(a))     # [1. 2. 3. 4.]
print(np.exp(a))       # exponential
print(np.log(a))       # natural log
print(np.sin(a))       # trigonometric
print(np.abs(np.array([-1, -2, 3])))  # [1 2 3]
print(np.round(3.14159, 2))            # 3.14
```

---

## 3. Coding: Broadcasting Rules

Broadcasting aligns array shapes from the **trailing (rightmost) dimension** outward. Two dimensions are compatible when:
1. They are equal, OR
2. One of them is `1`.

```python
# Example 1: scalar broadcast to array
a = np.array([[1, 2, 3], [4, 5, 6]])   # shape (2, 3)
result = a + 10                         # scalar broadcast to (2,3)
print(result)

# Example 2: 1D array broadcast across rows of 2D array
row_vector = np.array([10, 20, 30])     # shape (3,)
result2 = a + row_vector                # (2,3) + (3,) -> works
print(result2)
# [[11 22 33]
#  [14 25 36]]

# Example 3: column vector broadcast
col_vector = np.array([[100], [200]])   # shape (2, 1)
result3 = a + col_vector                # (2,3) + (2,1) -> works
print(result3)
# [[101 102 103]
#  [204 205 206]]

# Example 4: incompatible shapes raise an error
try:
    bad = a + np.array([1, 2])          # shape (2,3) + (2,) -> ERROR
except ValueError as e:
    print("Broadcasting Error:", e)
```

### Visualizing Broadcasting

```
Shape (2, 3):        [[1, 2, 3],
                       [4, 5, 6]]

Shape (3,):  [10, 20, 30]  --stretched to--> [[10,20,30],
                                                [10,20,30]]

Result:               [[11,22,33],
                        [14,25,36]]
```

---

## 4. Aggregate & Axis-based Operations

```python
a = np.array([[1, 2, 3], [4, 5, 6]])

print(a.sum())            # 21 (all elements)
print(a.sum(axis=0))      # [5 7 9]  -> sum down each column
print(a.sum(axis=1))      # [6 15]   -> sum across each row

print(a.mean(axis=0))     # column-wise mean
print(a.max(axis=1))      # row-wise max
print(a.min())             # global min
print(a.cumsum(axis=1))   # cumulative sum along rows
```

> **Axis tip**: `axis=0` operates "down the rows" (column-wise result), `axis=1` operates "across the columns" (row-wise result). This trips up beginners — always verify with a small example.

---

## 5. Use Cases & Scenarios

1. **Feature normalization in ML**: Subtracting the mean and dividing by standard deviation across a feature matrix using broadcasting (`(X - mean) / std`), without writing explicit loops.
2. **Image processing**: Adding a brightness offset to every pixel in an image by broadcasting a scalar across a `(H, W, 3)` array.
3. **Financial calculations**: Computing percentage returns for multiple stocks simultaneously by broadcasting a `(1, N)` array of initial prices across a `(T, N)` matrix of daily prices.
4. **Grading systems**: Applying a curve (e.g., `+5` points) to an entire class's exam scores in one operation.
5. **Physics simulations**: Broadcasting gravitational force vectors across a grid of particle positions.

### Real-World Scenario

> A data scientist has a feature matrix `X` of shape `(10000, 5)` representing 10,000 samples with 5 features each. To standardize the data before training a model, they compute the mean and standard deviation per feature (shape `(5,)`) and use broadcasting to normalize all 10,000 rows in a single vectorized line — orders of magnitude faster than looping.

```python
X = np.random.rand(10000, 5) * 100   # simulate raw feature data

mean = X.mean(axis=0)      # shape (5,)
std = X.std(axis=0)        # shape (5,)

X_normalized = (X - mean) / std   # broadcasting in action
print(X_normalized.mean(axis=0).round(2))  # ~[0. 0. 0. 0. 0.]
print(X_normalized.std(axis=0).round(2))   # ~[1. 1. 1. 1. 1.]
```

---

## 6. Practice Problems

1. Create two arrays of shape `(3,)` and add, subtract, multiply, and divide them element-wise. Print each result.
2. Given a `4x4` matrix, add a `1x4` row vector `[1,2,3,4]` to every row using broadcasting.
3. Create a `3x1` column vector and a `1x4` row vector. Add them together and explain the resulting shape.
4. Given a matrix of exam scores `scores = np.array([[70,85,90],[60,75,80],[95,88,92]])`, compute the mean score per student (row-wise) and per exam (column-wise).
5. **Scenario**: You have temperature readings in Celsius as a `(365,)` array for a year. Convert all readings to Fahrenheit using the formula `F = C * 9/5 + 32` in a single vectorized line.
6. **Debugging exercise**: Explain why `np.array([[1,2,3],[4,5,6]]) + np.array([1,2])` raises a `ValueError`. What shape would the second array need to be for broadcasting to succeed?
7. Write a function using broadcasting (no loops) that computes the Euclidean distance between a single point `(x, y)` and an array of `N` other points of shape `(N, 2)`.
