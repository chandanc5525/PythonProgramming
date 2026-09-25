# NumPy Lecture Notes — 13: Deep Dive — NumPy vs PyTorch vs TensorFlow

## 1. Introduction

This capstone session directly compares the three array/tensor systems side by side, covering memory-sharing semantics, performance benchmarking, GPU acceleration, automatic differentiation internals, and practical guidance on **when to stay in NumPy vs when to convert to a deep learning tensor**.

---

## 2. Conceptual Comparison Table

| Feature | NumPy `ndarray` | PyTorch `Tensor` | TensorFlow `Tensor` |
|---|---|---|---|
| Mutability | Mutable | Mutable | **Immutable** (use `tf.Variable` for mutable state) |
| GPU support | No (CPU only) | Yes (`.to('cuda')`) | Yes (automatic device placement) |
| Autograd | No | Yes (`requires_grad`, `.backward()`) | Yes (`GradientTape`) |
| Execution model | Eager only | Eager (default) | Eager (default in TF2) + graph mode (`tf.function`) |
| Zero-copy NumPy interop | N/A | Yes, via `torch.from_numpy()` | No (typically copies) |
| Primary use case | General numeric computing | Research-oriented deep learning | Production-oriented deep learning |

---

## 3. Coding: Zero-Copy vs Copy Semantics — Side by Side

```python
import numpy as np
import torch
import tensorflow as tf

arr = np.array([1.0, 2.0, 3.0], dtype=np.float32)

# PyTorch: torch.from_numpy() SHARES memory
t_torch = torch.from_numpy(arr)
arr[0] = 999.0
print("PyTorch (shared):", t_torch)     # reflects the change -> [999. 2. 3.]

# Reset
arr = np.array([1.0, 2.0, 3.0], dtype=np.float32)

# TensorFlow: tf.convert_to_tensor() COPIES memory
t_tf = tf.convert_to_tensor(arr)
arr[0] = 999.0
print("TensorFlow (copied):", t_tf)     # unaffected -> [1. 2. 3.]
```

> **Key takeaway**: If you mutate a NumPy array after converting it, PyTorch's zero-copy tensors silently reflect the change (a common bug source), while TensorFlow tensors do not. Always be explicit — use `.copy()` on the array or `torch.tensor()` (which copies) if you want PyTorch to be independent too.

---

## 4. Coding: Performance Benchmark — CPU Array Math

```python
import time

n = 10_000_000
np_a = np.random.rand(n).astype(np.float32)
np_b = np.random.rand(n).astype(np.float32)

torch_a = torch.from_numpy(np_a.copy())
torch_b = torch.from_numpy(np_b.copy())

tf_a = tf.constant(np_a)
tf_b = tf.constant(np_b)

# NumPy
start = time.time()
_ = np_a + np_b
print("NumPy (CPU):", time.time() - start)

# PyTorch (CPU)
start = time.time()
_ = torch_a + torch_b
print("PyTorch (CPU):", time.time() - start)

# TensorFlow (CPU)
start = time.time()
_ = tf_a + tf_b
print("TensorFlow (CPU):", time.time() - start)

# GPU (if available) -- typically dramatically faster for large tensors
if torch.cuda.is_available():
    gpu_a = torch_a.cuda()
    gpu_b = torch_b.cuda()
    torch.cuda.synchronize()
    start = time.time()
    _ = gpu_a + gpu_b
    torch.cuda.synchronize()
    print("PyTorch (GPU):", time.time() - start)
```

For small arrays, NumPy and CPU tensors perform similarly (framework overhead can even make NumPy faster). For **large arrays with GPU availability**, PyTorch/TensorFlow tensors dramatically outperform NumPy since NumPy has no GPU support at all.

---

## 5. Coding: Autograd Internals — Comparing the Two Frameworks

```python
# Same computation, same gradient result, two different APIs

# --- PyTorch ---
x_torch = torch.tensor([2.0, 3.0], requires_grad=True)
y_torch = (x_torch ** 3).sum()
y_torch.backward()
print("PyTorch grad:", x_torch.grad)     # dy/dx = 3x^2 -> [12., 27.]

# --- TensorFlow ---
x_tf = tf.Variable([2.0, 3.0])
with tf.GradientTape() as tape:
    y_tf = tf.reduce_sum(x_tf ** 3)
grad_tf = tape.gradient(y_tf, x_tf)
print("TensorFlow grad:", grad_tf.numpy())   # [12. 27.] -- matches!

# --- NumPy (manual gradient -- what autograd replaces) ---
x_np = np.array([2.0, 3.0])
manual_grad = 3 * x_np ** 2
print("NumPy manual grad:", manual_grad)      # [12. 27.] -- same answer, hand-derived
```

This demonstrates precisely *why* deep learning frameworks exist: they automate the calculus that would otherwise need to be manually derived (as in the NumPy example) for every new model architecture.

---

## 6. Use Cases & Scenarios

1. **Research prototyping**: PyTorch's eager, Pythonic, NumPy-like API and dynamic computation graphs make it popular for fast iteration in academic/research settings.
2. **Production deployment**: TensorFlow's `tf.function` graph compilation, TensorFlow Serving, and TensorFlow Lite ecosystem make it popular for deploying models at scale (mobile, embedded, web via TF.js).
3. **Scientific computing baseline**: NumPy remains the standard for non-differentiable numeric work — data cleaning, statistics, classical algorithms — even in ML-heavy organizations, because it has no training/inference overhead.
4. **Framework interoperability**: Libraries like ONNX allow models to be converted between frameworks; NumPy arrays act as the common "lowest common denominator" data format when exchanging data between systems built on different frameworks.
5. **Hybrid pipelines**: A single production system might use NumPy/Pandas for ETL, PyTorch for model training, and TensorFlow Lite for edge deployment — with NumPy arrays as the universal handoff format between stages.

### Real-World Scenario

> An ML platform team supports both research (PyTorch) and production deployment (TensorFlow Lite) teams. To avoid duplicating data pipelines, they standardize all data preprocessing in NumPy/Pandas, producing clean `.npz` feature archives. The research team loads these with `torch.from_numpy()` for fast experimentation; the deployment team loads the same archives with `tf.convert_to_tensor()` for the production graph — NumPy acts as the neutral, framework-agnostic interchange format across the entire organization.

```python
# Shared preprocessing artifact (framework-agnostic)
np.savez('features.npz', X=np.random.rand(1000, 20).astype(np.float32),
                          y=np.random.randint(0, 2, 1000))

# Research team (PyTorch)
data = np.load('features.npz')
X_torch = torch.from_numpy(data['X'])
y_torch = torch.from_numpy(data['y']).long()

# Deployment team (TensorFlow)
data2 = np.load('features.npz')
X_tf = tf.convert_to_tensor(data2['X'])
y_tf = tf.convert_to_tensor(data2['y'])
```

---

## 7. Practice Problems

1. Reproduce the zero-copy vs copy experiment above: convert the same NumPy array to a PyTorch tensor and a TensorFlow tensor, mutate the original array, and document which tensor reflects the change.
2. Write the same element-wise multiplication of two `5,000,000`-element arrays in NumPy, PyTorch (CPU), and TensorFlow (CPU). Benchmark all three with `time.time()` and report which is fastest on your machine.
3. Compute the gradient of `f(x) = x^4 - 2x^2 + 1` at `x = 3` three ways: (a) manually derive the derivative and evaluate it with NumPy, (b) using PyTorch's `.backward()`, (c) using TensorFlow's `GradientTape`. Confirm all three results match.
4. **Scenario**: You receive a `.npz` file containing preprocessed image features. Write two short loader functions — one that prepares the data as PyTorch tensors ready for a `DataLoader`, and one that prepares it as a `tf.data.Dataset` — from the exact same source array.
5. If you have GPU access, benchmark a large matrix multiplication (`2000x2000`) using NumPy (CPU-only), PyTorch on CPU, and PyTorch on GPU. Report the speedup GPU provides over NumPy.
6. **Conceptual**: Explain why TensorFlow tensors are immutable by design while PyTorch tensors and NumPy arrays are mutable. What software engineering benefit does immutability provide for TensorFlow's graph-compilation model (`tf.function`)?
7. **Capstone challenge**: Build one small linear regression model trained three different ways on the same synthetic NumPy dataset: (a) NumPy with manually coded gradient descent, (b) PyTorch using `autograd` + an optimizer (`torch.optim.SGD`), (c) TensorFlow using `GradientTape` + an optimizer (`tf.keras.optimizers.SGD`). Compare the final learned parameters and note differences in code length/complexity between the three approaches.

---

## Full Series Summary (Sessions 1–13)

| # | Topic |
|---|---|
| 01 | Introduction & Array Basics |
| 02 | Array Creation & Dtypes |
| 03 | Indexing, Slicing, Reshaping |
| 04 | Operations & Broadcasting |
| 05 | Math & Statistical Functions |
| 06 | Linear Algebra |
| 07 | Random Module & Simulations |
| 08 | Advanced Indexing & Masking |
| 09 | Performance Optimization |
| 10 | Real-World Workflows (Pandas/ML/I-O) |
| 11 | NumPy ↔ PyTorch Tensors |
| 12 | NumPy ↔ TensorFlow Tensors |
| 13 | Deep Dive: NumPy vs PyTorch vs TensorFlow |

This 13-session series now spans pure NumPy fundamentals through to production-grade deep learning tensor interoperability.
