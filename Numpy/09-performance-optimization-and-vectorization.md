# NumPy Lecture Notes — 09: Performance Optimization & Vectorization

## 1. Introduction

Writing *correct* NumPy code is only half the job — writing *fast* NumPy code requires understanding memory layout, avoiding unnecessary copies, and replacing Python loops with vectorized operations. This lesson covers profiling, vectorization patterns, memory strides, and when to reach for tools like `numba` or `Cython` when NumPy alone isn't enough.

---

## 2. Coding: Vectorization vs Loops

```python
import numpy as np
import time

n = 5_000_000
a = np.random.rand(n)
b = np.random.rand(n)

# SLOW: Python loop
def loop_add(a, b):
    result = np.empty(len(a))
    for i in range(len(a)):
        result[i] = a[i] + b[i]
    return result

start = time.time()
loop_result = loop_add(a, b)
print("Loop time:", time.time() - start)

# FAST: Vectorized
start = time.time()
vec_result = a + b
print("Vectorized time:", time.time() - start)
```

Vectorized operations are typically **50-200x faster** because they execute in compiled C code and avoid the overhead of Python's interpreter loop (bytecode dispatch, type-checking per element).

### Replacing Common Loop Patterns

```python
# BAD: appending in a loop
result = []
for x in range(1000):
    result.append(x ** 2)
result = np.array(result)

# GOOD: vectorized
result = np.arange(1000) ** 2

# BAD: conditional loop
data = np.random.randn(100000)
positive_count = 0
for x in data:
    if x > 0:
        positive_count += 1

# GOOD: vectorized boolean sum
positive_count = np.sum(data > 0)
```

---

## 3. Coding: Memory Layout & Strides

```python
a = np.arange(12).reshape(3, 4)
print(a.strides)     # (32, 8) -> bytes to step for each dimension
print(a.flags['C_CONTIGUOUS'])   # True -> row-major (C order)

b = a.T
print(b.flags['C_CONTIGUOUS'])   # False -> transposing breaks contiguity

# Forcing contiguous memory (important before some C-extension calls)
c = np.ascontiguousarray(b)
print(c.flags['C_CONTIGUOUS'])   # True
```

> **Why this matters**: Operations on contiguous memory are cache-friendlier and faster. Transposing or fancy-slicing can create non-contiguous views that slow down subsequent operations — `np.ascontiguousarray()` fixes this when needed.

### In-Place Operations (Avoiding Extra Memory Allocation)

```python
a = np.random.rand(1_000_000)

# Creates a new array (extra memory allocation)
b = a * 2

# In-place -- reuses existing memory, faster for large arrays
a *= 2

# Using `out` parameter to avoid allocating temporary arrays
result = np.empty_like(a)
np.multiply(a, 2, out=result)
```

---

## 4. Coding: Profiling & Benchmarking

```python
import numpy as np
import timeit

a = np.random.rand(1_000_000)

# Using timeit for reliable benchmarking
time_taken = timeit.timeit(lambda: np.sum(a), number=100)
print(f"Average time per call: {time_taken / 100:.6f} sec")

# Comparing sum() built-in vs np.sum()
py_list = a.tolist()
py_time = timeit.timeit(lambda: sum(py_list), number=100)
np_time = timeit.timeit(lambda: np.sum(a), number=100)
print(f"Python sum: {py_time:.4f}s | NumPy sum: {np_time:.4f}s")
```

### When NumPy Vectorization Isn't Enough

For extremely performance-critical code with complex per-element logic that can't be vectorized, consider:

```python
# numba: JIT-compiles Python functions to machine code
from numba import njit

@njit
def fast_custom_loop(arr):
    total = 0.0
    for i in range(len(arr)):
        total += arr[i] ** 2 if arr[i] > 0 else 0
    return total

# This runs at near-C speed despite looking like a plain Python loop
```

---

## 5. Use Cases & Scenarios

1. **Large-scale data pipelines**: Processing millions of rows of sensor or transaction data where loop-based code would take hours instead of seconds.
2. **Real-time systems**: Trading algorithms or robotics control loops where microsecond-level performance directly impacts outcomes.
3. **Deep learning preprocessing**: Vectorized image augmentation (normalization, resizing math) applied across large training batches.
4. **Scientific computing**: Simulating physical systems (fluid dynamics, particle physics) where vectorized array math replaces nested loops over grid cells.
5. **Backend APIs**: Optimizing numeric computation endpoints (e.g., recommendation scoring) to reduce server response latency and cost.

### Real-World Scenario

> A logistics company processes GPS coordinates for 50,000 delivery trucks every minute to compute distances traveled. Their original implementation used nested Python loops and took 45 seconds per batch — too slow for real-time dashboards. By rewriting the distance calculation using vectorized NumPy operations (the Haversine formula applied across the full array at once), processing time dropped to under 0.3 seconds.

```python
def haversine_vectorized(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

lat1 = np.random.uniform(-90, 90, 50000)
lon1 = np.random.uniform(-180, 180, 50000)
lat2 = np.random.uniform(-90, 90, 50000)
lon2 = np.random.uniform(-180, 180, 50000)

distances = haversine_vectorized(lat1, lon1, lat2, lon2)
print("Average distance:", distances.mean(), "km")
```

---

## 6. Practice Problems

1. Write both a loop-based and a vectorized version of a function that squares every element of a 2,000,000-element array. Benchmark both using `timeit` and report the speedup factor.
2. Given `a = np.arange(1000000)`, compare the performance of `sum(a)` (Python built-in) vs `np.sum(a)` vs `a.sum()`. Which is fastest and why?
3. Create a `1000x1000` matrix, transpose it, and check `flags['C_CONTIGUOUS']` before and after. Use `np.ascontiguousarray()` to fix it and verify.
4. Rewrite this loop using vectorization: 
   ```python
   result = []
   for x in data:
       result.append(x**2 if x > 0 else -x)
   ```
5. **Scenario**: You're processing a `(1,000,000, 3)` array of RGB pixel values and need to convert each pixel to grayscale using `gray = 0.299*R + 0.114*B + 0.587*G`. Write a fully vectorized solution (no loops) and explain why it scales better than a per-pixel loop.
6. **Conceptual**: Explain the difference between `a = a + 1` and `a += 1` in terms of memory allocation. When would the in-place version be preferable in a performance-critical application?
7. **Challenge**: Profile and optimize this function using vectorization: computing the pairwise Euclidean distance between every pair of points in a `(5000, 2)` array of 2D coordinates (avoid nested Python loops — hint: use broadcasting with `[:, np.newaxis, :]`).
