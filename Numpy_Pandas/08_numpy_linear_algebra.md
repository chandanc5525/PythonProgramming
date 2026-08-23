# 08. Linear Algebra with NumPy

Linear algebra is the mathematical foundation of machine learning — linear regression, PCA, neural networks, and recommendation systems are all, at their core, matrix operations. NumPy's `linalg` module and matrix multiplication operators are essential tools for understanding (and sometimes implementing) these algorithms from scratch.

## Matrix Multiplication (Not the Same as `*`)

```python
import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

A * B          # element-wise: [[5, 12], [21, 32]]  -- almost never what you want for "matrix math"
A @ B          # TRUE matrix multiplication: [[19, 22], [43, 50]]
np.matmul(A, B)  # same as @
np.dot(A, B)     # same as @ for 2D arrays (dot is more general for other dims)
```

**Rule to remember:** for real matrix multiplication (as in linear regression, neural network layers, etc.), always use `@` or `np.matmul` — never the plain `*` operator.

### Vector dot product

```python
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])
np.dot(v1, v2)     # 32  -- (1*4 + 2*5 + 3*6)
v1 @ v2            # same result
```

## Matrix Transpose, Inverse, Determinant

```python
A = np.array([[4, 7], [2, 6]])

A.T                    # transpose
np.linalg.inv(A)       # matrix inverse (A @ inv(A) ≈ Identity)
np.linalg.det(A)       # determinant: 10.0
np.linalg.matrix_rank(A)  # rank of the matrix
```

**Caution:** matrix inversion is numerically unstable for ill-conditioned matrices. In practice, use `np.linalg.solve()` instead of computing the inverse directly when solving linear systems — it's faster and more numerically stable.

## Solving Linear Systems (`Ax = b`)

```python
A = np.array([[3, 1], [1, 2]])
b = np.array([9, 8])

x = np.linalg.solve(A, b)
print(x)    # solution to the system of equations
```

## Linear Regression from Scratch (The "Normal Equation")

This shows exactly how the math you learned in linear algebra maps to real ML code — understanding this builds real intuition for what `LinearRegression().fit()` does internally.

```python
# X: feature matrix (n_samples, n_features), y: target vector (n_samples,)
X = np.array([[1, 1], [1, 2], [1, 3], [1, 4]], dtype=float)  # first col = bias/intercept term
y = np.array([2, 3, 5, 7], dtype=float)

# Normal equation: beta = (X^T X)^-1 X^T y
beta = np.linalg.inv(X.T @ X) @ X.T @ y
print(beta)   # [intercept, slope]

# More numerically stable version (preferred in practice):
beta_stable = np.linalg.lstsq(X, y, rcond=None)[0]
```

`np.linalg.lstsq` (least squares) is the numerically robust way to fit linear models and is what many libraries use under the hood for simple regression.

## Eigenvalues and Eigenvectors (Foundation of PCA)

```python
A = np.array([[2, 0], [0, 3]])

eigenvalues, eigenvectors = np.linalg.eig(A)
print(eigenvalues)     # [2. 3.]
print(eigenvectors)    # corresponding eigenvectors as columns
```

**Data science relevance:** Principal Component Analysis (PCA) — one of the most common dimensionality-reduction techniques — works by computing the eigenvectors of the covariance matrix of your features. The eigenvectors with the largest eigenvalues capture the directions of maximum variance in the data.

### A simplified PCA implementation using NumPy

```python
def simple_pca(X, n_components):
    X_centered = X - X.mean(axis=0)               # step 1: center the data
    cov_matrix = np.cov(X_centered, rowvar=False)  # step 2: covariance matrix
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)  # step 3: eigen-decomposition

    # sort eigenvectors by eigenvalue, descending
    idx = np.argsort(eigenvalues)[::-1]
    eigenvectors = eigenvectors[:, idx]

    components = eigenvectors[:, :n_components]
    X_transformed = X_centered @ components         # step 4: project onto principal components
    return X_transformed, components
```

This is a simplified but functionally accurate version of `sklearn.decomposition.PCA` — knowing this pattern helps you understand PCA's assumptions and limitations (e.g., sensitivity to feature scaling).

## Singular Value Decomposition (SVD)

SVD generalizes eigen-decomposition to non-square matrices and underlies recommendation systems, image compression, and more robust PCA implementations.

```python
A = np.array([[1, 2], [3, 4], [5, 6]])   # shape (3, 2), not square

U, S, Vt = np.linalg.svd(A, full_matrices=False)
print(U.shape, S.shape, Vt.shape)   # (3,2) (2,) (2,2)

# Reconstruct the original matrix
reconstructed = U @ np.diag(S) @ Vt
```

**Use case:** SVD-based dimensionality reduction (`TruncatedSVD` in scikit-learn) is standard for sparse data like text (TF-IDF matrices), and is the mathematical foundation of classic matrix-factorization recommender systems.

## Norms (Vector/Matrix Magnitude)

```python
v = np.array([3, 4])

np.linalg.norm(v)              # Euclidean (L2) norm: 5.0
np.linalg.norm(v, ord=1)       # Manhattan (L1) norm: 7.0
np.linalg.norm(v, ord=np.inf)  # max norm: 4.0

# Matrix (Frobenius) norm
M = np.array([[1, 2], [3, 4]])
np.linalg.norm(M)              # Frobenius norm
```

**Data science relevance:** L1 and L2 norms are exactly the regularization penalties in Lasso (L1) and Ridge (L2) regression. Understanding norms directly explains why L1 regularization tends to produce sparse (zeroed-out) coefficients while L2 shrinks them smoothly.

**Next:** `09_numpy_random_module.md`
