# 10. Advanced NumPy: Performance & Deep Internals

This is the "depth" file for NumPy — the concepts that separate someone who *uses* NumPy from someone who *understands* it well enough to write genuinely fast, production-grade data science code.

## Vectorization: Replacing Loops

The single biggest performance lesson in NumPy: **avoid Python-level loops over array elements.**

```python
import numpy as np
import time

n = 1_000_000
a = np.random.default_rng(0).random(n)
b = np.random.default_rng(1).random(n)

# SLOW: Python loop
start = time.time()
result = np.empty(n)
for i in range(n):
    result[i] = a[i] * b[i] + 1
print("Loop:", time.time() - start)

# FAST: vectorized
start = time.time()
result_vec = a * b + 1
print("Vectorized:", time.time() - start)
```

The vectorized version is typically 50-100x faster because it runs in compiled C code with no per-element Python interpreter overhead.

## `np.vectorize` — Convenience, Not Speed

```python
def my_func(x):
    return x ** 2 if x > 0 else 0

vec_func = np.vectorize(my_func)
vec_func(np.array([-2, -1, 0, 1, 2]))   # [0 0 0 1 4]
```

**Important misconception:** `np.vectorize` is a convenience wrapper (it's really just a hidden Python loop) — it does **not** give you C-level speed. For real performance, replace conditional logic with `np.where` or boolean masking instead:

```python
# True vectorized version -- much faster
arr = np.array([-2, -1, 0, 1, 2])
result = np.where(arr > 0, arr ** 2, 0)
```

## Memory Layout: C-order vs Fortran-order

```python
a = np.array([[1, 2, 3], [4, 5, 6]], order='C')   # row-major (default) -- rows stored contiguously
b = np.array([[1, 2, 3], [4, 5, 6]], order='F')   # column-major -- columns stored contiguously

print(a.flags['C_CONTIGUOUS'])   # True
print(b.flags['F_CONTIGUOUS'])   # True
```

**Why this matters:** operations that iterate along the contiguous axis are faster because of CPU cache locality. Summing along axis=1 (rows) on a C-order array is faster than summing along axis=0, and vice versa for F-order. This matters for very large arrays (millions+ elements) in performance-critical pipelines.

## Strides: How NumPy Actually Stores Data

```python
a = np.array([[1, 2, 3], [4, 5, 6]])
print(a.strides)   # (24, 8) -- bytes to step to move to next row / next column
```

Strides explain why reshaping and transposing are (usually) nearly free — `.T` doesn't copy data, it just changes the strides metadata to reinterpret the same memory block. This is also why some operations trigger unexpected copies: an operation that can't be expressed via strides alone (e.g., certain reshapes on non-contiguous arrays) forces a full copy.

```python
a = np.arange(6).reshape(2, 3)
b = a.T                   # view -- no copy, just different strides
print(np.shares_memory(a, b))   # True

c = a.T.reshape(6)        # this FORCES a copy because the transposed view isn't C-contiguous
print(np.shares_memory(a, c))   # False
```

## Avoiding Unnecessary Copies

```python
# BAD: repeated concatenation in a loop -- O(n^2) due to repeated full copies
result = np.array([])
for i in range(1000):
    result = np.concatenate([result, np.array([i])])   # very slow

# GOOD: preallocate, or collect in a list and convert once
result = np.empty(1000)
for i in range(1000):
    result[i] = i

# BEST (when possible): fully vectorized, no loop at all
result = np.arange(1000)
```

**General rule:** preallocate arrays with `np.empty`/`np.zeros` when the final size is known, rather than growing arrays incrementally — growing requires repeated full reallocation and copying.

## Structured Arrays (Mixed dtypes, Lightweight Alternative to DataFrames)

```python
dtype = [('name', 'U10'), ('age', 'i4'), ('score', 'f8')]
data = np.array([('Alice', 25, 88.5), ('Bob', 30, 92.1)], dtype=dtype)

print(data['name'])     # ['Alice' 'Bob']
print(data['age'].mean())   # 27.5
```

Structured arrays are a lightweight, memory-efficient alternative to Pandas for simple tabular data when you don't need the full DataFrame API — useful in performance-critical code or when interfacing with C libraries.

## `np.einsum` — Expressive, Fast Tensor Operations

Einstein summation notation lets you express many linear algebra and tensor operations concisely and often faster than chained NumPy calls (avoids creating intermediate arrays):

```python
A = np.random.default_rng(0).random((3, 4))
B = np.random.default_rng(1).random((4, 5))

# Standard matrix multiply
C1 = A @ B

# Same operation via einsum
C2 = np.einsum('ij,jk->ik', A, B)
print(np.allclose(C1, C2))   # True

# Other common patterns:
np.einsum('ii->i', np.eye(3))     # extract diagonal
np.einsum('ij->ji', A)             # transpose
np.einsum('ij,ij->', A, A)         # sum of element-wise squares (Frobenius norm squared)
```

`einsum` is heavily used in deep learning code (e.g., attention mechanisms in transformers) for expressing complex tensor contractions clearly and efficiently.

## Numerical Stability Considerations

```python
# Naive softmax can overflow with large values
def naive_softmax(x):
    exp_x = np.exp(x)
    return exp_x / exp_x.sum()

# Numerically stable version -- subtract the max before exponentiating
def stable_softmax(x):
    exp_x = np.exp(x - np.max(x))
    return exp_x / exp_x.sum()

x = np.array([1000, 1001, 1002])
# naive_softmax(x)  -> produces NaN due to overflow!
print(stable_softmax(x))   # correct, stable result
```

This "subtract the max" trick is a textbook numerical-stability pattern used inside virtually every ML framework's softmax implementation — understanding it helps you debug NaN losses during model training.

## Performance Checklist for Data Scientists

1. **Vectorize** — replace explicit loops with array operations wherever possible.
2. **Preallocate** arrays instead of growing them incrementally.
3. **Use appropriate dtypes** — `float32` instead of `float64` can halve memory for large datasets/deep learning.
4. **Watch for accidental copies** — use `np.shares_memory()` to check, and slice/view instead of copying when mutation isn't needed.
5. **Use `axis` correctly** in aggregations instead of looping over rows/columns manually.
6. **Profile before optimizing** — use `%timeit` in Jupyter or Python's `timeit` module to confirm where time is actually spent.

```python
# In Jupyter/IPython
%timeit arr.sum()
%timeit np.sum(arr)
```

---

This concludes the NumPy series. **NumPy files 01–10** built the foundation for everything that follows: Pandas (files 11–20) is built directly on top of these array concepts, and every DataFrame operation ultimately compiles down to NumPy operations under the hood.

**Next:** `11_pandas_introduction_and_data_structures.md`
