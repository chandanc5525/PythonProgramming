# 07. Reshaping, Stacking, and Splitting Arrays

Data rarely arrives in the shape your model or algorithm needs. Reshaping is a daily operation — especially when moving between tabular data, images, and model inputs.

## Reshaping

```python
import numpy as np

arr = np.arange(12)          # shape (12,)
print(arr.reshape(3, 4))     # reshape to 3 rows, 4 columns
print(arr.reshape(4, 3))     # reshape to 4 rows, 3 columns
print(arr.reshape(2, 2, 3))  # reshape to 3D: (2, 2, 3)
```

**The `-1` trick** — let NumPy infer one dimension automatically:

```python
arr.reshape(3, -1)    # NumPy computes: 12 / 3 = 4 columns -> shape (3, 4)
arr.reshape(-1, 1)    # turn a 1D array into a column vector, shape (12, 1)
arr.reshape(-1)       # flatten back to 1D
```

### Why `reshape(-1, 1)` shows up constantly

Scikit-learn requires 2D input for features (`X`) even when you have a single feature. This is one of the most common real-world errors:

```python
# ValueError: Expected 2D array, got 1D array instead
single_feature = np.array([1, 2, 3, 4, 5])
# model.fit(single_feature, y)   # FAILS

# Fix:
single_feature_2d = single_feature.reshape(-1, 1)   # shape (5, 1)
# model.fit(single_feature_2d, y)   # works
```

## Flattening

```python
X = np.array([[1, 2], [3, 4]])

X.flatten()    # [1 2 3 4] -- ALWAYS returns a copy
X.ravel()      # [1 2 3 4] -- returns a VIEW when possible (faster, but can mutate original)
```

**Use case:** flattening a 2D image (`height x width`) into a 1D feature vector for classical ML models that expect flat feature vectors (as opposed to CNNs which keep spatial structure).

## Transposing

```python
X = np.array([[1, 2, 3], [4, 5, 6]])   # shape (2, 3)
X.T                                      # shape (3, 2) -- swaps rows and columns
np.transpose(X)                          # same as .T

# For higher dimensions, specify axis order explicitly
X3 = np.ones((2, 3, 4))
X3.transpose(1, 0, 2).shape   # (3, 2, 4) -- swaps axes 0 and 1
```

**Use case:** transposing is essential in linear algebra for ML (e.g., computing `X.T @ X` for normal equations in linear regression) and for converting between "channels-first" and "channels-last" image formats in deep learning.

## Adding/Removing Dimensions

```python
a = np.array([1, 2, 3])        # shape (3,)

a[np.newaxis, :]                # shape (1, 3) -- row vector
a[:, np.newaxis]                # shape (3, 1) -- column vector
np.expand_dims(a, axis=0)       # same as a[np.newaxis, :]

b = np.array([[[1, 2, 3]]])     # shape (1, 1, 3)
np.squeeze(b)                    # removes all size-1 dimensions -> shape (3,)
np.squeeze(b, axis=0)            # removes only axis 0 -> shape (1, 3)
```

**Use case:** `expand_dims` is used constantly to add a "batch dimension" before feeding a single sample into a model that expects a batch (e.g., `model.predict(image[np.newaxis, ...])`).

## Stacking Arrays Together

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

np.vstack([a, b])       # stack vertically (row-wise) -> shape (2, 3)
np.hstack([a, b])       # stack horizontally -> shape (6,)
np.column_stack([a, b]) # stack as columns -> shape (3, 2)
np.stack([a, b], axis=0)  # general-purpose stacking, creates a NEW axis -> shape (2, 3)
np.concatenate([a, b])    # joins along an EXISTING axis -> shape (6,)
```

**Difference between `stack` and `concatenate`:** `stack` always creates a new dimension; `concatenate` joins along an existing one. This distinction matters when assembling batches of samples or combining feature arrays from different sources.

### Common real-world pattern: combining features from different sources

```python
numerical_features = np.array([[1.0, 2.0], [3.0, 4.0]])     # shape (2, 2)
encoded_categorical = np.array([[0, 1, 0], [1, 0, 0]])       # shape (2, 3)

X_combined = np.hstack([numerical_features, encoded_categorical])  # shape (2, 5)
```

This is exactly what happens (conceptually) when combining scaled numeric columns with one-hot encoded categorical columns before model training.

## Splitting Arrays

```python
arr = np.arange(9)

np.split(arr, 3)               # split into 3 EQUAL parts: [array([0,1,2]), array([3,4,5]), array([6,7,8])]
np.split(arr, [3, 6])          # split at specific indices -> 3 parts of sizes 3,3,3

X = np.arange(12).reshape(4, 3)
np.vsplit(X, 2)                # split into 2 groups of rows
np.hsplit(X, 3)                # split into 3 groups of columns
```

**Use case:** manually implementing k-fold cross-validation splits, or dividing a feature matrix into numeric/categorical column groups for separate preprocessing.

## Repeating and Tiling

```python
a = np.array([1, 2, 3])

np.repeat(a, 2)          # [1 1 2 2 3 3] -- repeats each element
np.tile(a, 2)             # [1 2 3 1 2 3] -- repeats the whole array

np.tile(a, (2, 1))        # tile into a 2D array: [[1,2,3],[1,2,3]]
```

**Use case:** `np.repeat` is handy for expanding aggregated group statistics back to the original row-level shape (a manual version of Pandas' `groupby().transform()`).

**Next:** `08_numpy_linear_algebra.md`
