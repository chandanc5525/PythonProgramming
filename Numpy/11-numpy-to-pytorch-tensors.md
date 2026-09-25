# NumPy Lecture Notes — 11: NumPy ↔ PyTorch Tensors

## 1. Introduction

PyTorch's core data structure, `torch.Tensor`, is deliberately designed to feel like a NumPy `ndarray` — same slicing syntax, similar broadcasting rules, similar function names (`torch.sum`, `torch.mean`, etc.) — but with two superpowers NumPy lacks natively: **GPU acceleration** and **automatic differentiation (autograd)**, which together make PyTorch a training engine for neural networks.

Understanding how data moves between NumPy and PyTorch — and where memory is shared vs copied — is essential for building efficient ML data pipelines.

### Installation

```bash
pip install torch
```

---

## 2. Coding: Converting NumPy Arrays to Tensors

```python
import numpy as np
import torch

# Method 1: torch.from_numpy() -- SHARES memory with the original array
arr = np.array([1, 2, 3, 4], dtype=np.float32)
tensor_shared = torch.from_numpy(arr)

print(tensor_shared)              # tensor([1., 2., 3., 4.])

# Because memory is shared, modifying one modifies the other!
arr[0] = 999
print(tensor_shared)              # tensor([999.,   2.,   3.,   4.])

# Method 2: torch.tensor() -- ALWAYS COPIES data (safer, more common)
arr2 = np.array([5, 6, 7, 8], dtype=np.float32)
tensor_copy = torch.tensor(arr2)
arr2[0] = -1
print(tensor_copy)                # tensor([5., 6., 7., 8.]) -> unaffected
```

### Converting Tensors Back to NumPy

```python
t = torch.tensor([1.0, 2.0, 3.0])

# .numpy() also shares memory (only works for CPU tensors)
back_to_np = t.numpy()
print(type(back_to_np))            # <class 'numpy.ndarray'>

t[0] = 100.0
print(back_to_np)                  # [100.   2.   3.] -> shared memory
```

> **Rule of thumb**: `torch.from_numpy()` and `.numpy()` are zero-copy (fast, but memory-linked). `torch.tensor()` always makes an independent copy (slightly slower, but safe).

---

## 3. Coding: Dtype Mapping & Device Placement

```python
# NumPy -> PyTorch dtype correspondence
np_float32 = np.array([1, 2, 3], dtype=np.float32)
t_float32 = torch.from_numpy(np_float32)
print(t_float32.dtype)              # torch.float32

np_int64 = np.array([1, 2, 3], dtype=np.int64)
t_int64 = torch.from_numpy(np_int64)
print(t_int64.dtype)                # torch.int64

# PyTorch neural networks expect float32 by default -- a common gotcha:
np_default = np.array([1, 2, 3])            # dtype defaults to int64
t_wrong = torch.from_numpy(np_default).float()  # explicit cast needed

# Moving tensors to GPU (if available) -- NumPy CANNOT do this natively
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
gpu_tensor = t_float32.to(device)
print(gpu_tensor.device)

# IMPORTANT: GPU tensors must be moved back to CPU before converting to NumPy
if gpu_tensor.is_cuda:
    back = gpu_tensor.cpu().numpy()
```

---

## 4. Coding: Autograd — What NumPy Cannot Do

```python
# NumPy has NO concept of gradients -- this is PyTorch's key advantage
x = torch.tensor([2.0, 3.0], requires_grad=True)

y = x ** 2 + 3 * x
loss = y.sum()

loss.backward()          # automatically computes dLoss/dx
print(x.grad)             # tensor([7., 9.])  -> gradients computed automatically!
```

### Shape, Reshape & Broadcasting Parity with NumPy

```python
t = torch.arange(12)
print(t.reshape(3, 4))        # same as np.reshape
print(t.view(3, 4))            # view -- PyTorch's analogue of np.ravel's memory sharing

a = torch.tensor([[1, 2, 3]])         # shape (1,3)
b = torch.tensor([[1], [2], [3]])      # shape (3,1)
print(a + b)                            # broadcasting works identically to NumPy
```

---

## 5. Use Cases & Scenarios

1. **Loading a NumPy-preprocessed dataset into a neural network**: Data cleaned/normalized with NumPy/Pandas is converted to tensors just before model training.
2. **Custom Dataset classes**: PyTorch's `Dataset.__getitem__` often returns NumPy arrays that get auto-converted to tensors via `DataLoader`'s default collation.
3. **Interfacing with scientific libraries**: Using SciPy/NumPy for signal preprocessing, then converting the final feature array to a tensor for a PyTorch model.
4. **GPU-accelerated simulations**: Migrating a NumPy-based physics simulation to PyTorch tensors to leverage GPU parallelism for large-scale computation.
5. **Model output post-processing**: Converting a model's tensor predictions back to NumPy for plotting with Matplotlib or further Pandas analysis (which don't understand tensors).

### Real-World Scenario

> A computer vision team preprocesses a dataset of images using OpenCV and NumPy (resizing, normalization) to produce a `(50000, 3, 224, 224)` float32 array. Just before training, they wrap this array in a PyTorch `Dataset`, converting batches to tensors with `torch.from_numpy()` inside `__getitem__` for zero-copy efficiency, then move each batch to GPU with `.to(device)` for training.

```python
class ImageDataset(torch.utils.data.Dataset):
    def __init__(self, numpy_images, numpy_labels):
        self.images = numpy_images    # stays as NumPy until needed
        self.labels = numpy_labels

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image = torch.from_numpy(self.images[idx]).float()
        label = torch.tensor(self.labels[idx], dtype=torch.long)
        return image, label
```

---

## 6. Practice Problems

1. Create a NumPy array of shape `(5,)` with `dtype=float32`, convert it to a tensor using `torch.from_numpy()`, modify an element in the NumPy array, and verify the tensor reflects the change.
2. Repeat the above using `torch.tensor()` instead and verify the tensor does **not** change when the NumPy array is modified.
3. Create a NumPy integer array, convert it to a tensor, and explicitly cast it to `float32` (required for most neural net operations). Explain why this cast is often necessary.
4. Create a tensor with `requires_grad=True`, define `y = 3*x**3 - 2*x`, call `.backward()`, and print `x.grad`. Manually verify the gradient calculation (`dy/dx = 9x^2 - 2`) matches.
5. **Scenario**: You've computed a `(1000, 10)` feature matrix using NumPy. Write a function that converts it to a float32 tensor, moves it to GPU if available, and returns it — handling the case where CUDA is unavailable gracefully.
6. Convert a PyTorch tensor result (e.g., `torch.tensor([1.5, 2.5, 3.5])`) back into a NumPy array and use `np.mean()` on it directly.
7. **Conceptual**: Explain why a tensor with `requires_grad=True` cannot be directly converted with `.numpy()` (hint: research `.detach()`). Demonstrate the fix with code.
