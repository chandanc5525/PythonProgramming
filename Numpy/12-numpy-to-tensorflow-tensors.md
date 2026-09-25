# NumPy Lecture Notes — 12: NumPy ↔ TensorFlow Tensors

## 1. Introduction

TensorFlow's `tf.Tensor` is the framework's core data structure, conceptually similar to NumPy's `ndarray` but built to support **automatic differentiation (via `GradientTape`)**, **graph-based execution/compilation (via `tf.function`)**, and **distributed/GPU-TPU computation**. Unlike PyTorch, TensorFlow tensors are **immutable by default** — a key conceptual difference from mutable NumPy arrays — and TensorFlow provides a separate `tf.Variable` type for mutable, trainable state.

### Installation

```bash
pip install tensorflow
```

---

## 2. Coding: Converting NumPy Arrays to Tensors

```python
import numpy as np
import tensorflow as tf

# Method 1: tf.convert_to_tensor() -- the standard, idiomatic way
arr = np.array([1, 2, 3, 4], dtype=np.float32)
tensor = tf.convert_to_tensor(arr)
print(tensor)          # tf.Tensor([1. 2. 3. 4.], shape=(4,), dtype=float32)

# Method 2: tf.constant() -- also creates a tensor from NumPy data
tensor2 = tf.constant(arr)
print(tensor2)

# IMPORTANT: TensorFlow tensors are IMMUTABLE
try:
    tensor[0] = 100.0         # this will raise an error!
except TypeError as e:
    print("Error:", e)
```

### Converting Tensors Back to NumPy

```python
t = tf.constant([1.0, 2.0, 3.0])

# Method 1: .numpy() method
back_to_np = t.numpy()
print(type(back_to_np))           # <class 'numpy.ndarray'>

# Method 2: np.array() works directly on tensors too
back_to_np2 = np.array(t)

# NumPy functions often work DIRECTLY on tensors (implicit conversion)
print(np.sum(t))                   # 6.0 -- NumPy auto-converts via __array__
```

> Unlike PyTorch's `torch.from_numpy()`, converting a NumPy array to a TensorFlow tensor with `tf.convert_to_tensor()` typically **copies** the data (TensorFlow does not guarantee shared memory across the Python/C++ boundary), making the two objects independent by default.

---

## 3. Coding: `tf.Variable` — Mutable, Trainable Tensors

```python
# tf.Tensor is immutable -- for trainable weights, use tf.Variable
initial_value = np.array([1.0, 2.0, 3.0], dtype=np.float32)
weights = tf.Variable(initial_value)

print(weights)                     # <tf.Variable ... numpy=[1. 2. 3.]>

# Variables CAN be updated in place
weights.assign([10.0, 20.0, 30.0])
weights.assign_add([1.0, 1.0, 1.0])   # element-wise increment
print(weights.numpy())              # [11. 21. 31.]
```

---

## 4. Coding: Dtype Mapping & Device Placement

```python
# Dtype correspondence
np_f32 = np.array([1, 2, 3], dtype=np.float32)
t_f32 = tf.convert_to_tensor(np_f32)
print(t_f32.dtype)                  # tf.float32

# TensorFlow, like PyTorch, expects float32 for most model computations
np_default = np.array([1, 2, 3])              # int64 by default
t_wrong = tf.cast(tf.convert_to_tensor(np_default), tf.float32)

# Checking / placing on GPU (TensorFlow manages this mostly automatically)
print("GPU available:", tf.config.list_physical_devices('GPU'))

with tf.device('/CPU:0'):
    cpu_tensor = tf.constant(np_f32)
```

---

## 5. Coding: GradientTape — TensorFlow's Autograd

```python
# NumPy has no gradient tracking -- TensorFlow's GradientTape provides this
x = tf.Variable(np.array([2.0, 3.0], dtype=np.float32))

with tf.GradientTape() as tape:
    y = x ** 2 + 3 * x
    loss = tf.reduce_sum(y)

grads = tape.gradient(loss, x)
print(grads.numpy())               # [7. 9.] -> matches PyTorch's autograd result
```

### Shape, Reshape & Broadcasting Parity with NumPy

```python
t = tf.range(12)
print(tf.reshape(t, (3, 4)))          # same semantics as np.reshape

a = tf.constant([[1, 2, 3]])           # shape (1,3)
b = tf.constant([[1], [2], [3]])       # shape (3,1)
print(a + b)                            # broadcasting works identically to NumPy
```

---

## 6. Use Cases & Scenarios

1. **Keras model input pipelines**: NumPy arrays (images, tabular features) are commonly fed directly into `model.fit(X, y)` — Keras internally converts them to tensors.
2. **`tf.data.Dataset` pipelines**: Building efficient, prefetched input pipelines from NumPy arrays using `tf.data.Dataset.from_tensor_slices()`.
3. **Custom training loops**: Using `GradientTape` with NumPy-derived data to manually implement training steps outside of `model.fit()`.
4. **TensorFlow Lite / mobile deployment**: Converting NumPy-preprocessed sensor input into tensors for on-device inference.
5. **Scientific ML (physics-informed neural networks)**: Combining NumPy-based numerical simulation data with TensorFlow's differentiable computation graph.

### Real-World Scenario

> A retail forecasting team has a NumPy array of shape `(2000, 30, 5)` representing 2000 store-week sequences with 5 features each. They build an efficient training pipeline using `tf.data.Dataset.from_tensor_slices()` to batch and shuffle this NumPy data without manually managing tensor conversion for every batch — TensorFlow handles the NumPy-to-tensor conversion internally and efficiently.

```python
X = np.random.rand(2000, 30, 5).astype(np.float32)
y = np.random.rand(2000, 1).astype(np.float32)

dataset = tf.data.Dataset.from_tensor_slices((X, y))
dataset = dataset.shuffle(buffer_size=2000).batch(32).prefetch(tf.data.AUTOTUNE)

for batch_X, batch_y in dataset.take(1):
    print(batch_X.shape, batch_y.shape)   # (32, 30, 5) (32, 1)
```

---

## 7. Practice Problems

1. Create a NumPy array of shape `(4,)` with `dtype=float32`, convert it using both `tf.convert_to_tensor()` and `tf.constant()`. Verify both produce equivalent tensors.
2. Attempt to modify an element of a `tf.Tensor` directly (e.g., `tensor[0] = 5`) and observe the error. Then create a `tf.Variable` from the same data and successfully update it using `.assign()`.
3. Convert a TensorFlow tensor to a NumPy array using `.numpy()`, then verify that modifying the resulting NumPy array does **not** affect the original tensor (i.e., confirm the copy behavior).
4. Create a `tf.Variable` with `requires_grad`-equivalent tracking, define `y = 2*x**3 + x`, and use `GradientTape` to compute `dy/dx`. Manually verify the result (`dy/dx = 6x^2 + 1`).
5. **Scenario**: Given a NumPy feature array `X` of shape `(5000, 8)` and labels `y` of shape `(5000,)`, build a `tf.data.Dataset` pipeline that batches the data in groups of 64 and shuffles it, ready for training.
6. Check whether your machine has GPU support using `tf.config.list_physical_devices('GPU')`. Create a tensor explicitly on the CPU using the `tf.device` context manager.
7. **Conceptual**: Explain the core philosophical difference between `tf.Tensor` (immutable) and `tf.Variable` (mutable), and why this distinction doesn't exist in plain NumPy arrays. Why does TensorFlow need this separation for building trainable neural networks?
