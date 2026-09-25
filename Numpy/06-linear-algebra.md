# NumPy Lecture Notes — 06: Linear Algebra with NumPy

## 1. Introduction

Linear algebra underpins nearly all of machine learning, computer graphics, and scientific computing. NumPy's `numpy.linalg` module provides efficient implementations of matrix multiplication, decompositions, determinants, inverses, and eigenvalue computations — all backed by optimized BLAS/LAPACK libraries.

---

## 2. Coding: Matrix Operations

```python
import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# Element-wise multiplication (NOT matrix multiplication)
print(A * B)
# [[ 5 12]
#  [21 32]]

# True matrix multiplication (dot product)
print(A @ B)               # preferred modern syntax
print(np.matmul(A, B))     # equivalent
print(np.dot(A, B))        # also equivalent for 2D arrays

# Transpose
print(A.T)

# Determinant
print(np.linalg.det(A))    # -2.0

# Inverse
A_inv = np.linalg.inv(A)
print(A_inv)

# Verify: A @ A_inv should be the identity matrix
print(np.round(A @ A_inv))  # [[1. 0.] [0. 1.]]
```

### Solving Linear Systems (Ax = b)

```python
# Solve: 3x + y = 9
#        x + 2y = 8
A = np.array([[3, 1], [1, 2]])
b = np.array([9, 8])

x = np.linalg.solve(A, b)
print(x)   # [2. 3.]  -> x=2, y=3
```

### Eigenvalues & Eigenvectors

```python
A = np.array([[4, 2], [1, 3]])
eigenvalues, eigenvectors = np.linalg.eig(A)

print("Eigenvalues:", eigenvalues)
print("Eigenvectors:\n", eigenvectors)
```

### Vector Operations

```python
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])

print(np.dot(v1, v2))               # dot product -> 32
print(np.linalg.norm(v1))            # magnitude (L2 norm)
print(np.cross(v1, v2))              # cross product (3D vectors only)
```

### Matrix Decompositions

```python
A = np.array([[4, 0], [0, 9]])

# Singular Value Decomposition
U, S, Vt = np.linalg.svd(A)
print("Singular values:", S)

# QR decomposition
Q, R = np.linalg.qr(A)
print("Q:\n", Q)
print("R:\n", R)

# Rank
print(np.linalg.matrix_rank(A))
```

---

## 3. Use Cases & Scenarios

1. **Machine learning — Linear Regression**: The closed-form (normal equation) solution `θ = (XᵀX)⁻¹Xᵀy` relies directly on matrix inversion and multiplication.
2. **Computer graphics**: 3D transformations (rotation, scaling, translation) are represented and applied as matrix multiplications.
3. **Principal Component Analysis (PCA)**: Dimensionality reduction relies on eigenvalue/eigenvector decomposition of the covariance matrix.
4. **Recommendation systems**: Matrix factorization (via SVD) decomposes a user-item rating matrix to predict missing ratings.
5. **Physics/engineering simulations**: Solving systems of simultaneous equations (structural loads, circuit analysis) using `np.linalg.solve`.

### Real-World Scenario

> A recommendation engine for a streaming platform has a sparse user-movie ratings matrix. Using Singular Value Decomposition (`np.linalg.svd`), the engineering team factorizes this matrix into latent "taste" dimensions, enabling predictions for movies a user hasn't rated yet — the mathematical foundation of collaborative filtering.

```python
# Simplified example: closed-form linear regression using the normal equation
X = np.array([[1, 1], [1, 2], [1, 3], [1, 4]])   # bias term + feature
y = np.array([3, 5, 7, 9])

# theta = (X^T X)^-1 X^T y
theta = np.linalg.inv(X.T @ X) @ X.T @ y
print("Intercept, Slope:", theta)   # ~[1. 2.] -> y = 1 + 2x
```

---

## 4. Practice Problems

1. Create two `3x3` matrices and compute both their element-wise product and their true matrix product. Explain the difference in results.
2. Compute the determinant and inverse of `[[2, 1], [1, 1]]`. Verify the inverse is correct by multiplying it with the original matrix.
3. Solve the system of equations: `2x + 3y = 12` and `x - y = 1` using `np.linalg.solve`.
4. Compute the eigenvalues and eigenvectors of `[[2, 0], [0, 3]]`. What do you notice about the eigenvectors of a diagonal matrix?
5. Given two 3D vectors `v1 = [1, 0, 0]` and `v2 = [0, 1, 0]`, compute their dot product and cross product. Explain geometrically what each result represents.
6. **Scenario**: Implement simple linear regression from scratch using the normal equation on the dataset `X = [1,2,3,4,5]`, `y = [2,4,6,8,10]`. Verify your model correctly learns the relationship `y = 2x`.
7. **Challenge**: Compute the rank of the matrix `[[1,2,3],[2,4,6],[1,1,1]]`. Explain why the rank is less than 3 despite the matrix having 3 rows.
