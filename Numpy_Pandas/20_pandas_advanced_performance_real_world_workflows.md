# 20. Advanced Pandas: Performance & Real-World Data Science Workflows

This final file covers the "depth" concepts that separate someone who can *use* Pandas from someone who can build reliable, efficient, production-grade data pipelines with it.

## Method Chaining (Readable, Pipeline-Style Code)

Instead of reassigning `df` repeatedly, chain operations for a clear, linear, function-pipeline style that's easier to read and debug:

```python
import pandas as pd

result = (
    pd.read_csv('sales.csv')
    .dropna(subset=['amount'])
    .query('amount > 0')
    .assign(amount_log=lambda d: d['amount'].apply(lambda x: x ** 0.5))
    .groupby('region')
    .agg(total_sales=('amount', 'sum'), avg_sales=('amount', 'mean'))
    .sort_values('total_sales', ascending=False)
    .reset_index()
)
```

`.assign()` is the chaining-friendly way to add new columns without breaking the chain (unlike `df['new_col'] = ...`, which requires a separate statement).

## `.pipe()` — Chaining Custom Functions

```python
def remove_outliers(df, column, n_std=3):
    mean, std = df[column].mean(), df[column].std()
    return df[(df[column] - mean).abs() <= n_std * std]

def add_features(df):
    df = df.copy()
    df['amount_squared'] = df['amount'] ** 2
    return df

result = (
    pd.read_csv('sales.csv')
    .pipe(remove_outliers, column='amount')
    .pipe(add_features)
)
```

`.pipe()` lets you slot custom, reusable transformation functions into a chain — the standard pattern for building maintainable, testable Pandas preprocessing pipelines.

## Performance: Vectorization Over `.apply()` / Loops

The single biggest Pandas performance lesson, directly extending the NumPy vectorization lesson from file 10:

```python
import numpy as np
import time

df = pd.DataFrame({'a': np.random.default_rng(0).random(1_000_000)})

# SLOW: row-wise apply
start = time.time()
df['b_slow'] = df['a'].apply(lambda x: x ** 2 + 1)
print("apply:", time.time() - start)

# FAST: vectorized
start = time.time()
df['b_fast'] = df['a'] ** 2 + 1
print("vectorized:", time.time() - start)
```

**General performance hierarchy (fastest to slowest), from most to least preferred:**
1. Vectorized operations (`df['a'] * 2`, `np.where`, built-in `.str`/`.dt` accessors)
2. `.agg()` / `.transform()` with built-in string names (`'mean'`, `'sum'`) — these use optimized Cython implementations
3. `.apply()` with a vectorized-friendly function
4. `.apply(axis=1)` — row-wise Python loop, avoid on large data
5. Explicit Python `for` loop over `.iterrows()` — almost always avoid; `.iterrows()` is notoriously slow because it reconstructs a Series for every row

```python
# AVOID this pattern on anything but tiny DataFrames
for idx, row in df.iterrows():
    df.at[idx, 'b'] = row['a'] * 2   # extremely slow at scale

# Prefer vectorized:
df['b'] = df['a'] * 2
```

## Memory Optimization for Large DataFrames

```python
df.info(memory_usage='deep')     # accurate memory usage including object/string overhead

# Downcast numeric dtypes
df['count'] = pd.to_numeric(df['count'], downcast='integer')
df['price'] = pd.to_numeric(df['price'], downcast='float')

# Convert repetitive strings to category dtype (often 80-90%+ memory reduction)
df['status'] = df['status'].astype('category')

# Drop unused columns as early as possible in a pipeline
df = df.drop(columns=['unused_col_1', 'unused_col_2'])

# Read only needed columns from the start (best option when reading from disk)
df = pd.read_csv('big_file.csv', usecols=['id', 'amount', 'date'])
```

## Working with Data Too Large for Memory

```python
# Chunked processing (see also file 14)
chunks = pd.read_csv('huge.csv', chunksize=500_000)
result = pd.concat(
    (chunk.groupby('category')['amount'].sum() for chunk in chunks)
).groupby(level=0).sum()

# Parquet + column pruning avoids loading unnecessary data at all
df = pd.read_parquet('huge.parquet', columns=['id', 'amount'])
```

For datasets that consistently exceed memory, consider **Dask** or **Polars** — both offer Pandas-like APIs with out-of-core/parallel execution, and Polars in particular has become a common high-performance alternative for large tabular workloads while sharing much of Pandas' conceptual vocabulary.

## Categorical Dtype: Beyond Memory Savings

```python
df['size'] = pd.Categorical(df['size'], categories=['small', 'medium', 'large'], ordered=True)

df['size'] < 'large'                     # meaningful ordered comparison
df.sort_values('size')                    # sorts by the DEFINED category order, not alphabetically
```

Ordered categoricals are the correct way to represent ordinal data (e.g., education level, satisfaction rating, size) — preserving meaningful order for sorting, comparison, and downstream encoding (e.g., ordinal encoding for ML models).

## A Realistic End-to-End Cleaning & Feature Engineering Pipeline

Putting together concepts from files 11-20 into a representative real workflow:

```python
def load_and_prepare(filepath):
    df = pd.read_csv(filepath, parse_dates=['order_date'])

    # 1. Data quality checks
    print(df.info())
    print(df.isnull().sum())

    # 2. Clean
    df = df.drop_duplicates()
    df['customer_id'] = df['customer_id'].astype(str)
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df = df.dropna(subset=['amount', 'customer_id'])

    # 3. Feature engineering
    df['order_month'] = df['order_date'].dt.month
    df['order_dow'] = df['order_date'].dt.day_name()
    df['customer_avg_order'] = df.groupby('customer_id')['amount'].transform('mean')
    df['amount_vs_customer_avg'] = df['amount'] - df['customer_avg_order']

    # 4. Memory optimization
    df['order_dow'] = df['order_dow'].astype('category')

    return df

df = load_and_prepare('orders.csv')
```

## Bridging Back to NumPy / Scikit-learn

```python
# Preparing a DataFrame for a scikit-learn model
numeric_features = df.select_dtypes(include='number').columns
X = df[numeric_features].to_numpy()      # explicit conversion to NumPy for model input
y = df['target'].to_numpy()

# After prediction, results often go back into a DataFrame for reporting
df['prediction'] = model.predict(X)
```

This is the natural closing of the loop: NumPy (files 01-10) provides the numerical foundation, Pandas (files 11-20) provides labeled, tabular data wrangling on top of it, and the final `.to_numpy()` hands clean, validated data off to modeling libraries like scikit-learn, which return results that flow right back into a DataFrame for analysis and reporting.

## Final Checklist: A Data Scientist's Pandas/NumPy Habits

1. Always run `.info()`, `.describe()`, and `.isnull().sum()` immediately after loading new data
2. Prefer vectorized operations over `.apply()`, and `.apply()` over explicit loops
3. Know when `.loc`/`.iloc` and `.copy()` are needed to avoid `SettingWithCopyWarning` bugs
4. Validate merge/join results by checking row counts before and after
5. Set random seeds for reproducibility in any sampling, splitting, or simulation
6. Use `category` dtype and downcasted numeric types for memory efficiency at scale
7. Convert cleanly to NumPy arrays (`.to_numpy()`) at the model-input boundary

---

This completes the 20-file NumPy → Pandas learning path, from array fundamentals through production-grade tabular data workflows used daily in real data science practice.
