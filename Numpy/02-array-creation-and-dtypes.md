# NumPy Lecture Notes — 02: Array Creation & Data Types

## 1. Introduction

Beyond `np.array()`, NumPy provides many specialized functions to create arrays efficiently — without manually typing out every value. Understanding **data types (`dtype`)** is equally important, since it directly controls memory usage, precision, and computational behavior.

---

## 2. Coding: Array Creation Functions

```python
import numpy as np

# Arrays of zeros / ones
zeros = np.zeros((2, 3))          # 2x3 array of 0.0
ones = np.ones((3, 3))            # 3x3 array of 1.0
full = np.full((2, 2), 7)         # 2x2 array filled with 7

# Identity / eye matrix
identity = np.eye(4)              # 4x4 identity matrix

# Ranges
arange_arr = np.arange(0, 10, 2)  # [0 2 4 6 8]
linspace_arr = np.linspace(0, 1, 5)  # 5 evenly spaced points between 0 and 1

# Uninitialized memory (fast but garbage values)
empty_arr = np.empty((2, 2))

# Random arrays
rand_uniform = np.random.rand(2, 3)        # uniform [0,1)
rand_normal = np.random.randn(2, 3)        # standard normal distribution
rand_ints = np.random.randint(0, 100, (2, 3))  # random ints

print(zeros)
print(linspace_arr)
```

### Creating From Existing Data

```python
# From a Python list/tuple
a = np.array([1, 2, 3])

# From nested sequences
b = np.array([(1, 2), (3, 4)])

# Copy vs reference
c = np.array(a)          # always creates a copy
d = np.asarray(a)        # avoids copy if already an ndarray

# Like functions -- match shape/dtype of another array
e = np.zeros_like(b)
f = np.ones_like(b)
```

---

## 3. Data Types (`dtype`) Deep Dive

```python
# Explicit dtype specification
int_arr = np.array([1, 2, 3], dtype=np.int32)
float_arr = np.array([1, 2, 3], dtype=np.float64)
bool_arr = np.array([1, 0, 1], dtype=np.bool_)
complex_arr = np.array([1+2j, 3+4j], dtype=np.complex128)

print(int_arr.dtype)     # int32
print(float_arr.dtype)   # float64

# Type conversion (casting)
casted = int_arr.astype(np.float64)
print(casted.dtype)      # float64
```

### Common NumPy Dtypes

| Dtype | Description | Typical size |
|---|---|---|
| `int8`/`int16`/`int32`/`int64` | Signed integers | 1–8 bytes |
| `uint8`...`uint64` | Unsigned integers | 1–8 bytes |
| `float16`/`float32`/`float64` | Floating point | 2–8 bytes |
| `bool_` | Boolean | 1 byte |
| `complex64`/`complex128` | Complex numbers | 8–16 bytes |
| `object_` | Python object reference | pointer size |

### Why Dtype Matters

```python
# Memory impact of dtype choice
a_32 = np.ones(1_000_000, dtype=np.int32)
a_64 = np.ones(1_000_000, dtype=np.int64)

print(a_32.nbytes, "bytes")   # 4,000,000
print(a_64.nbytes, "bytes")   # 8,000,000
```

Choosing a smaller dtype (e.g., `int32` instead of `int64`, or `float32` instead of `float64`) can **halve memory usage** — critical when working with large datasets or GPU-bound machine learning pipelines.

---

## 4. Use Cases & Scenarios

1. **Memory-constrained systems (embedded/IoT)**: Using `int8` or `float16` for sensor data to fit within limited RAM.
2. **Deep learning**: Model weights are frequently stored as `float32` (or `float16` for mixed-precision training) to balance precision and GPU memory.
3. **Financial data**: Using `float64` for currency calculations where precision matters, avoiding rounding errors from lower precision types.
4. **Categorical/boolean masks**: Using `bool_` arrays to efficiently filter large datasets (e.g., marking fraudulent transactions).
5. **Scientific simulations**: `np.linspace` is used to generate time steps for simulations (e.g., 1000 evenly spaced points over 10 seconds).

### Real-World Scenario

> A machine learning engineer notices their model training uses excessive GPU memory. By auditing their NumPy preprocessing pipeline and converting `float64` arrays to `float32`, they cut memory usage in half with negligible accuracy loss — allowing a larger batch size and faster training.

```python
# Before
X = np.random.randn(100000, 128).astype(np.float64)
print("float64 memory:", X.nbytes / 1e6, "MB")

# After optimization
X_optimized = X.astype(np.float32)
print("float32 memory:", X_optimized.nbytes / 1e6, "MB")
```

---

## 5. Practice Problems

1. Create a `4x4` identity matrix and a `3x5` array of all 9s using built-in creation functions.
2. Use `np.linspace` to generate 10 evenly spaced values between -5 and 5.
3. Create an integer array `[1, 2, 3, 4]`, check its dtype, then convert it to `float32` and verify the change.
4. Calculate and compare the memory (`nbytes`) of a `1,000,000`-element array stored as `int8` vs `int64`. Explain the difference numerically.
5. **Scenario**: You're building a sensor-data pipeline for a battery-powered IoT device that only records values between 0–255. Which dtype would you choose and why? Write code to create such an array with 1,000 random readings using the most memory-efficient dtype.
6. Generate a `5x5` array of random integers between 1 and 100 using `np.random.randint`, then convert it to `bool_` (any non-zero becomes `True`). What does the resulting array represent?
