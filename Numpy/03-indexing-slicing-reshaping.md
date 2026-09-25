# NumPy Lecture Notes — 03: Indexing, Slicing & Reshaping

## 1. Introduction

Efficiently accessing and reorganizing array data is central to NumPy usage. This lesson covers:

- **Indexing**: accessing single elements.
- **Slicing**: accessing sub-ranges (views, not copies).
- **Reshaping**: changing the "shape" of data without changing its content.

Understanding whether an operation returns a **view** (shares memory) or a **copy** (independent memory) is one of the most important — and most commonly misunderstood — concepts in NumPy.

---

## 2. Coding: Indexing & Slicing

### 1D Indexing

```python
import numpy as np

a = np.array([10, 20, 30, 40, 50])

print(a[0])      # 10
print(a[-1])     # 50
print(a[1:4])    # [20 30 40]
print(a[::2])    # [10 30 50]  (step of 2)
print(a[::-1])   # [50 40 30 20 10]  (reversed)
```

### 2D Indexing

```python
b = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

print(b[0, 0])      # 1
print(b[1, :])       # [4 5 6]  -> entire row 1
print(b[:, 1])       # [2 5 8]  -> entire column 1
print(b[0:2, 1:3])   # [[2 3], [5 6]]  -> sub-matrix
```

### Views vs Copies (Critical Concept)

```python
original = np.array([1, 2, 3, 4, 5])
view = original[1:4]      # SLICING returns a VIEW
view[0] = 999
print(original)           # [1 999 3 4 5]  <- original is modified!

copy = original[1:4].copy()   # explicit COPY
copy[0] = -1
print(original)           # unaffected by the copy
```

> **Rule of thumb**: Basic slicing (`a[1:4]`) returns a *view*. Fancy indexing (`a[[1,2,3]]`) and boolean indexing return a *copy*.

### Fancy (Advanced) Indexing

```python
a = np.array([10, 20, 30, 40, 50])
indices = [0, 2, 4]
print(a[indices])          # [10 30 50] -> always a copy

b = np.array([[1, 2], [3, 4], [5, 6]])
print(b[[0, 2]])           # rows 0 and 2 -> [[1 2] [5 6]]
```

### Boolean Masking

```python
a = np.array([10, 15, 20, 25, 30])
mask = a > 18
print(mask)         # [False False  True  True  True]
print(a[mask])       # [20 25 30]

# Combined condition
print(a[(a > 10) & (a < 30)])  # [15 20 25]
```

---

## 3. Coding: Reshaping Arrays

```python
a = np.arange(12)          # [0 1 2 ... 11]
print(a.shape)              # (12,)

b = a.reshape(3, 4)         # reshape into 3 rows, 4 cols
print(b)

c = a.reshape(2, -1)        # -1 lets NumPy auto-calculate that dimension
print(c.shape)              # (2, 6)

# Flatten back to 1D
flat = b.flatten()          # always returns a COPY
raveled = b.ravel()         # returns a VIEW when possible (faster)

# Transpose
d = b.T
print(d.shape)               # (4, 3)

# Adding/removing dimensions
e = np.array([1, 2, 3])
expanded = np.expand_dims(e, axis=0)   # shape (1, 3)
squeezed = np.squeeze(expanded)         # back to shape (3,)
```

### Stacking & Splitting

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(np.vstack([a, b]))     # stack vertically -> shape (2,3)
print(np.hstack([a, b]))     # stack horizontally -> shape (6,)
print(np.column_stack([a, b]))  # stack as columns -> shape (3,2)

c = np.arange(9)
print(np.split(c, 3))        # split into 3 equal parts
```

---

## 4. Use Cases & Scenarios

1. **Image cropping**: Slicing a 2D/3D array to extract a region of interest from an image, e.g., `image[50:150, 100:200]`.
2. **Feature selection in ML**: Boolean masking to filter rows of a dataset matching a condition (e.g., `X[y == 1]` to extract only positive class samples).
3. **Reshaping for neural networks**: Flattening a `(28, 28)` image into a `(784,)` vector before feeding it into a dense neural network layer.
4. **Time series windowing**: Slicing an array to extract a rolling window of the last 30 days for a moving average calculation.
5. **Batch processing**: Reshaping a flat array of collected sensor readings into `(num_batches, batch_size)` for parallel processing.

### Real-World Scenario

> An image classification pipeline loads a batch of grayscale images as a `(1000, 28, 28)` NumPy array. Before feeding it into a neural network requiring flat vectors, the array is reshaped to `(1000, 784)` using `reshape(1000, -1)` — with no data copying, this operation is nearly instantaneous.

```python
images = np.random.rand(1000, 28, 28)   # simulate 1000 grayscale images
flattened = images.reshape(1000, -1)
print(flattened.shape)   # (1000, 784)
```

---

## 5. Practice Problems

1. Given `a = np.arange(20)`, extract every 3rd element starting from index 2.
2. Create a `5x5` matrix using `np.arange(25).reshape(5,5)`. Extract the middle `3x3` sub-matrix using slicing.
3. Demonstrate with code why modifying a slice of an array also modifies the original array. Then show how `.copy()` prevents this.
4. Given `scores = np.array([45, 67, 89, 32, 95, 71])`, use boolean masking to extract all scores greater than or equal to 60 (a "passing" filter).
5. Create a 1D array of 24 elements and reshape it into shapes `(2,3,4)`, `(4,6)`, and `(24,)`. Verify each has the same total number of elements using `.size`.
6. **Scenario**: You have a `(1000, 3)` array representing RGB pixel values for 1000 pixels. Use fancy indexing to select only pixels where the Red channel (`column 0`) value is greater than 200 (bright red pixels).
7. **Conceptual**: Explain the difference between `ravel()` and `flatten()`. In what scenario would using `flatten()` be safer despite being slower?
