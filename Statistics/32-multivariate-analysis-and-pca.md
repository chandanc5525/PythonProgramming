# 32. Multivariate Analysis and PCA

## Overview
Real business datasets often have dozens or hundreds of correlated variables. Multivariate techniques like Principal Component Analysis (PCA) reduce this complexity while preserving as much information as possible.

## The Problem PCA Solves
- **Multicollinearity**: many correlated variables make models unstable and hard to interpret (see Topic 26).
- **Curse of dimensionality**: too many variables relative to observations degrades model performance.
- **Visualization**: humans can't visualize 20-dimensional data — PCA can compress it to 2-3 dimensions for plotting.

## How PCA Works (Conceptually)
PCA finds new variables — **principal components** — that are linear combinations of the original variables, ordered so that:
1. The first component captures the maximum possible variance in the data.
2. Each subsequent component captures the maximum remaining variance, subject to being uncorrelated (orthogonal) with all previous components.

## Key Outputs
- **Explained variance ratio**: how much of the total variance each component captures — used to decide how many components to keep (e.g., "keep enough components to explain 90% of variance").
- **Loadings**: how strongly each original variable contributes to each component — used for interpretation.
- **Scree plot**: visualizes explained variance per component to spot the "elbow" where additional components add little value.

## Python Example
```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np

X = np.random.rand(100, 10)  # 100 customers, 10 correlated behavioral metrics
X_scaled = StandardScaler().fit_transform(X)

pca = PCA(n_components=3)
components = pca.fit_transform(X_scaled)
print("Explained variance ratio:", pca.explained_variance_ratio_)
```

## Business Application
A customer analytics team has 40 correlated engagement metrics (logins, clicks, session time, feature usage, etc.) and uses PCA to compress them into 3-4 composite "engagement dimensions," which are then used as clean, uncorrelated inputs to a churn prediction model.

## Key Takeaways
- PCA reduces dimensionality while retaining maximum variance, addressing multicollinearity and enabling visualization.
- Always standardize variables before PCA — otherwise variables with larger scales dominate the components artificially.
- Principal components are combinations of original variables, so interpretability requires examining the loadings.
