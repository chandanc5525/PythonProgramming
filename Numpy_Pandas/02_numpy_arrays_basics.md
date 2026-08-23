# 02. NumPy Arrays: The Basics

## Creating Arrays from Python Structures

```python
import numpy as np

# 1D array from a list
a = np.array([1, 2, 3])

# 2D array from a list of lists (matrix)
b = np.array([[1, 2, 3], [4, 5, 6]])

# 3D array (e.g., a stack of matrices, or a color image)
c = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])

print(a.shape)  # (3,)
print(b.shape)  # (2, 3)
print(c.shape)  # (2, 2, 2)
```

## Understanding Data Types (`dtype`)

Every NumPy array has a single, uniform data type. This is unlike Python lists, which can hold mixed types.

```python
int_arr = np.array([1, 2, 3])
print(int_arr.dtype)          # int64

float_arr = np.array([1.0, 2.0, 3.0])
print(float_arr.dtype)        # float64

# Mixed input gets upcast to the most general type
mixed = np.array([1, 2.5, 3])
print(mixed.dtype)            # float64 -- all elements become floats

bool_arr = np.array([True, False, True])
print(bool_arr.dtype)         # bool

# Explicit dtype control
explicit = np.array([1, 2, 3], dtype=np.float32)
print(explicit.dtype)         # float32
```

### Common dtypes in data science work

| dtype | Use case |
|---|---|
| `int64` / `int32` | Counts, IDs, categorical codes |
| `float64` | Default for most numerical computation |
| `float32` | Deep learning (saves memory, GPUs prefer it) |
| `bool` | Masks, filters, flags |
| `object` | Mixed types / strings (avoid when possible — kills performance) |
| `datetime64` | Timestamps (heavily used in Pandas) |

**Why dtype matters in practice:** loading a dataset with the wrong dtype (e.g., numeric columns read as `object`) silently breaks downstream math operations and blows up memory usage. Always check `.dtype` after loading data.

## Type Conversion

```python
arr = np.array([1.7, 2.3, 3.9])
int_version = arr.astype(np.int32)     # [1, 2, 3] -- truncates, doesn't round!
print(int_version)

# Common gotcha: astype(int) truncates towards zero, it does NOT round
print(np.array([1.9, -1.9]).astype(int))  # [1, -1]

# To round first, then convert:
print(np.round([1.9, -1.9]).astype(int))  # [2, -2]
```

## Array Creation Shortcuts

```python
np.zeros((3, 4))        # 3x4 array of zeros (common weight initialization / placeholders)
np.ones((2, 2))         # 2x2 array of ones
np.full((2, 2), 7)      # 2x2 array filled with 7
np.eye(3)               # 3x3 identity matrix
np.empty((2, 2))        # uninitialized memory (fast, but contains garbage values)

np.arange(0, 10, 2)     # [0, 2, 4, 6, 8] -- like Python's range()
np.linspace(0, 1, 5)    # [0., 0.25, 0.5, 0.75, 1.] -- 5 evenly spaced points
```

`np.linspace` is especially useful for generating evenly spaced values for plotting functions, simulations, or grid search ranges.

## Copies vs. Views (Critical Concept)

This is one of the most common sources of subtle bugs for data scientists.

```python
a = np.array([1, 2, 3, 4, 5])

# Slicing creates a VIEW, not a copy -- modifying it modifies the original!
b = a[1:3]
b[0] = 999
print(a)   # [1, 999, 3, 4, 5]  <- 'a' changed too!

# To avoid this, explicitly copy:
c = a[1:3].copy()
c[0] = -1
print(a)   # unaffected
```

**Rule of thumb:** Basic slicing (`arr[1:3]`) returns a *view*. Fancy indexing (`arr[[1,2]]`) and boolean masking return a *copy*. When in doubt, use `.copy()` if you plan to mutate a subset without affecting the source array — this is a very common bug when preprocessing data pipelines that share arrays across steps.

## Checking Memory Layout

```python
a = np.array([[1, 2, 3], [4, 5, 6]])
print(a.flags['C_CONTIGUOUS'])   # True -- row-major (default, C-style)
print(a.flags['OWNDATA'])        # True if this array owns its data (not a view)
```

Knowing whether an array is a view matters when you pass arrays into functions that mutate in-place (common in preprocessing pipelines) — an unexpected view can silently corrupt your original dataset.

**Next:** `03_numpy_array_creation_methods.md`
