# NumPy Lecture Notes — 01: Introduction & Array Basics

## 1. Introduction

**NumPy** (Numerical Python) is the foundational library for numerical and scientific computing in Python. It provides:

- The **`ndarray`** — a fast, memory-efficient, multi-dimensional array object.
- **Vectorized operations** — mathematical operations applied to whole arrays without explicit Python loops.
- The computational core for higher-level libraries: **Pandas, SciPy, scikit-learn, TensorFlow, PyTorch, Matplotlib**.

### Why NumPy over native Python lists?

| Feature | Python List | NumPy Array |
|---|---|---|
| Storage | Heterogeneous, pointer-based | Homogeneous, contiguous memory |
| Speed | Slow (interpreted loops) | Fast (C-optimized, vectorized) |
| Memory | High overhead per element | Compact, fixed-size elements |
| Math operations | Manual looping required | Built-in element-wise ops |
| Broadcasting | Not supported | Supported |

NumPy arrays are stored as contiguous blocks of memory of a single data type, which allows CPU-level optimizations (SIMD instructions) and avoids Python's per-object overhead.

### Installation

```bash
pip install numpy
```

### Importing

```python
import numpy as np
print(np.__version__)
```

---

## 2. Coding: Creating Your First Arrays

```python
import numpy as np

# 1D array (vector)
a = np.array([1, 2, 3, 4, 5])
print(a)                # [1 2 3 4 5]
print(type(a))           # <class 'numpy.ndarray'>

# 2D array (matrix)
b = np.array([[1, 2, 3], [4, 5, 6]])
print(b)
# [[1 2 3]
#  [4 5 6]]

# 3D array (tensor)
c = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
print(c.shape)           # (2, 2, 2)
```

### Key Array Attributes

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

print(arr.ndim)      # 2  -> number of dimensions
print(arr.shape)     # (2, 3) -> rows, columns
print(arr.size)      # 6  -> total number of elements
print(arr.dtype)     # int64 -> data type of elements
print(arr.itemsize)  # 8  -> bytes per element
print(arr.nbytes)    # 48 -> total bytes consumed
```

### Comparing List vs Array Performance

```python
import time

size = 1_000_000
py_list = list(range(size))
np_array = np.arange(size)

start = time.time()
py_result = [x * 2 for x in py_list]
print("List time:", time.time() - start)

start = time.time()
np_result = np_array * 2
print("NumPy time:", time.time() - start)
```

NumPy is typically **10x to 100x faster** for large-scale numeric operations because it avoids Python-level loop overhead and uses compiled C code internally.

---

## 3. Use Cases & Scenarios

1. **Scientific computing**: Representing physical quantities (temperature grids, sensor readings) as arrays for fast numerical simulation.
2. **Data preprocessing pipelines**: Before data reaches Pandas or scikit-learn, raw numeric data is often manipulated as NumPy arrays.
3. **Image processing**: An image is just a 3D NumPy array `(height, width, channels)` — libraries like OpenCV and PIL interoperate directly with NumPy.
4. **Financial modeling**: Representing time series of prices/returns as arrays to compute rolling statistics efficiently.
5. **Machine learning**: Feature matrices (`X`) and label vectors (`y`) are almost always NumPy arrays or array-backed structures under the hood.

### Real-World Scenario

> A retail analytics team receives millions of daily transaction amounts as a raw list. Instead of looping in Python to compute total revenue, average basket size, and outlier detection, they convert to a NumPy array once and apply vectorized operations — cutting processing time from minutes to seconds.

```python
transactions = np.array([250, 89, 430, 12, 999, 45, 670])

total_revenue = transactions.sum()
average_basket = transactions.mean()
high_value = transactions[transactions > 400]

print("Total:", total_revenue)
print("Average:", average_basket)
print("High-value transactions:", high_value)
```

---

## 4. Practice Problems

1. Create a 1D NumPy array of integers from 10 to 20 and print its `dtype`, `shape`, and `size`.
2. Create a 2D array of shape `(3, 4)` filled with your choice of numbers. Print its `ndim` and `nbytes`.
3. Given `arr = np.array([1, 2, 3])`, what is the effect of `arr.dtype` if you create it as `np.array([1, 2, 3], dtype=float)`? Verify with code.
4. Write a small benchmark (like the one above) comparing summing a list of 2,000,000 numbers using a Python `for` loop vs. `np.sum()`. Report the time difference.
5. **Scenario**: You are given daily step counts for a month as a Python list. Convert it to a NumPy array and compute: total steps, best day, and how many days exceeded 10,000 steps.
6. **Conceptual**: Explain in your own words why NumPy arrays must be homogeneous (single data type) while Python lists can be heterogeneous. What performance benefit does this design choice provide?
