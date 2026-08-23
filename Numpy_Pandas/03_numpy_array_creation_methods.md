# 03. Array Creation Methods (In Depth)

Data scientists need to generate arrays constantly — for placeholders, synthetic test data, initializing model weights, or building grids for evaluation. This file covers every practical creation method.

## Sequence Generators

```python
import numpy as np

np.arange(10)              # [0 1 2 3 4 5 6 7 8 9]
np.arange(2, 10, 2)        # [2 4 6 8]  -- start, stop (exclusive), step
np.arange(0, 1, 0.1)       # floats -- BEWARE floating point rounding issues

np.linspace(0, 10, 5)      # [0., 2.5, 5., 7.5, 10.] -- 5 points including both ends
np.linspace(0, 10, 5, endpoint=False)  # excludes the endpoint

np.logspace(0, 3, 4)       # [1, 10, 100, 1000] -- log-scale spacing, base 10 by default
```

**Data science use case:** `np.linspace` is the standard way to build a range of hyperparameter values (e.g., learning rates) or an x-axis for plotting a fitted curve. `np.logspace` is preferred when hyperparameters span orders of magnitude (e.g., regularization strength `alpha` from 0.0001 to 1000).

## Placeholder Arrays

```python
np.zeros(5)                 # [0. 0. 0. 0. 0.]
np.zeros((3, 3))            # 3x3 zero matrix
np.ones((2, 3))
np.full((2, 3), fill_value=-1)

# "Like" variants: match shape/dtype of an existing array
existing = np.array([[1, 2], [3, 4]])
np.zeros_like(existing)     # zeros with same shape/dtype as `existing`
np.ones_like(existing)
np.full_like(existing, 9)
```

`_like` functions are extremely useful when writing generic preprocessing functions that need a same-shaped output array without hardcoding dimensions.

## Identity and Diagonal Matrices

```python
np.eye(4)                   # 4x4 identity matrix (used in linear algebra, regularization)
np.identity(3)              # same as eye() for square matrices

np.diag([1, 2, 3])          # 3x3 matrix with [1,2,3] on the diagonal, 0 elsewhere
np.diag(np.array([[1,2],[3,4]]))  # extracts diagonal: [1, 4]
```

## Random Array Generation (Preview)

Covered in depth in file 09, but the essentials:

```python
rng = np.random.default_rng(seed=42)   # modern, recommended API

rng.random((2, 3))          # uniform floats in [0, 1)
rng.integers(0, 10, size=5) # random ints in [0, 10)
rng.normal(loc=0, scale=1, size=(3, 3))  # standard normal distribution
```

**Always set a seed** (`seed=42` or similar) when generating random data for reproducible experiments — critical for debugging ML pipelines and sharing reproducible results with teammates.

## Building Arrays from Existing Data

```python
# From a Python range
np.array(range(10))

# From a list of tuples
np.array([(1, 2), (3, 4)])

# From nested lists (must have consistent shape!)
np.array([[1, 2, 3], [4, 5]])  # This raises issues -- creates a ragged/object array with a warning

# From a Pandas Series/DataFrame
import pandas as pd
s = pd.Series([1, 2, 3])
np.array(s)          # or s.to_numpy() -- the preferred, explicit method
```

**Best practice:** when converting from Pandas to NumPy, prefer `.to_numpy()` or `.values` over `np.array(df)` for clarity and to avoid unnecessary copies when possible.

## Meshgrids (For Evaluating Functions Over a Grid)

```python
x = np.linspace(-5, 5, 5)
y = np.linspace(-5, 5, 5)
X, Y = np.meshgrid(x, y)

Z = X**2 + Y**2   # evaluate a function over the entire 2D grid at once
```

**Data science use case:** meshgrids are the standard tool for visualizing decision boundaries of classifiers (plotting `predict()` over a grid of points) and for contour/surface plots in EDA and model diagnostics.

## Building from Files (Preview)

```python
# Simple text/CSV loading (Pandas is usually preferred, but NumPy works for pure numeric data)
data = np.loadtxt('data.csv', delimiter=',', skiprows=1)

# Faster and more robust for structured numeric data
data = np.genfromtxt('data.csv', delimiter=',', skip_header=1, filling_values=np.nan)

# Saving arrays in NumPy's native binary format (fast, preserves dtype/shape exactly)
np.save('array.npy', data)
loaded = np.load('array.npy')

# Multiple arrays in one compressed file
np.savez('arrays.npz', X=X_train, y=y_train)
loaded = np.load('arrays.npz')
X_train = loaded['X']
```

`.npy`/`.npz` are the standard formats for caching preprocessed feature arrays between pipeline runs — much faster to load than re-parsing CSVs every time.

**Next:** `04_numpy_indexing_slicing.md`
