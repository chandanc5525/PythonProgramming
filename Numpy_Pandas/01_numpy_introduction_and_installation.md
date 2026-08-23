# 01. Introduction to NumPy

## What is NumPy?

NumPy (**Num**erical **Py**thon) is the foundational package for numerical and scientific computing in Python. It provides:

- A powerful **N-dimensional array object** (`ndarray`)
- Fast **vectorized** mathematical operations (no explicit Python loops needed)
- Tools for **linear algebra, random number generation, Fourier transforms**
- The underlying data structure used by **Pandas, Scikit-learn, TensorFlow, PyTorch, SciPy**, and virtually every data science library in Python

As a data scientist, you rarely use NumPy in isolation — but almost everything you do (feature engineering, matrix math for ML models, image processing, statistical computation) sits on top of NumPy arrays. Understanding NumPy deeply makes you faster at debugging Pandas, writing efficient ML preprocessing code, and understanding what libraries are doing under the hood.

## Why not just use Python lists?

Python lists are flexible but slow and memory-heavy for numerical work because:

1. Each element in a list is a full Python object (with type info, reference count, etc.)
2. Lists don't support element-wise math (`[1,2,3] * 2` doesn't do what you'd expect)
3. Iterating in Python is slow compared to compiled C loops

NumPy arrays store data in a single, contiguous block of memory with a **fixed type**, allowing operations to run in optimized, compiled C code — often 10x to 100x faster than pure Python.

```python
import numpy as np
import time

# Pure Python
py_list = list(range(1_000_000))
start = time.time()
py_result = [x * 2 for x in py_list]
print("Python loop:", time.time() - start)

# NumPy vectorized
np_arr = np.arange(1_000_000)
start = time.time()
np_result = np_arr * 2
print("NumPy vectorized:", time.time() - start)
```

NumPy will typically be 10–50x faster on this kind of operation.

## Installation

```bash
pip install numpy

# In a data science environment, typically installed alongside:
pip install numpy pandas matplotlib scikit-learn jupyter
```

Verify installation:

```python
import numpy as np
print(np.__version__)
```

## The Core Object: `ndarray`

Everything in NumPy revolves around the `ndarray` (N-dimensional array):

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
print(type(arr))        # <class 'numpy.ndarray'>
print(arr.dtype)        # int64 (or int32 on Windows)
print(arr.shape)        # (5,)
print(arr.ndim)         # 1 (number of dimensions)
```

Key attributes every data scientist should know cold:

| Attribute | Meaning |
|---|---|
| `.shape` | Tuple describing the size of each dimension |
| `.ndim`  | Number of dimensions (1D, 2D, 3D, ...) |
| `.dtype` | Data type of elements (int64, float32, bool, etc.) |
| `.size`  | Total number of elements |
| `.itemsize` | Bytes per element |
| `.nbytes` | Total bytes consumed by the array |

```python
arr2d = np.array([[1, 2, 3], [4, 5, 6]])
print(arr2d.shape)     # (2, 3) -> 2 rows, 3 columns
print(arr2d.ndim)      # 2
print(arr2d.size)      # 6
print(arr2d.dtype)     # int64
print(arr2d.nbytes)    # 48 (6 elements * 8 bytes)
```

## Data Science Perspective: Why This Matters

- **Feature matrices** in ML (`X`) are almost always 2D NumPy arrays: `(n_samples, n_features)`
- **Images** are 3D arrays: `(height, width, channels)`
- **Batches of images** (deep learning) are 4D arrays: `(batch_size, height, width, channels)`
- **Pandas DataFrames** are built on top of NumPy arrays internally (each column is often a NumPy array)
- Scikit-learn models expect NumPy arrays (or array-like objects) as input via `.fit(X, y)`

Understanding `shape` and `dtype` is the single most common source of bugs in data science pipelines — shape mismatches ("expected 2D array, got 1D array instead") are extremely common when moving between Pandas and Scikit-learn/NumPy.

## What's Next

The following files build up from array creation, through indexing, operations, and into the specific tools (linear algebra, random sampling, broadcasting) that show up daily in real data science workflows.

**Next:** `02_numpy_arrays_basics.md`
