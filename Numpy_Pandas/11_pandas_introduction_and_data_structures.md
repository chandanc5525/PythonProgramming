# 11. Introduction to Pandas & Core Data Structures

## What is Pandas?

Pandas is the standard Python library for **tabular data manipulation and analysis** — it's the tool data scientists use to load, clean, transform, explore, and analyze structured/semi-structured data (think: spreadsheets, SQL query results, CSV files, JSON records).

Pandas is built on top of NumPy: internally, DataFrame columns are typically backed by NumPy arrays, which is why everything you learned in files 01–10 directly informs how Pandas behaves under the hood.

```bash
pip install pandas
```

```python
import pandas as pd
print(pd.__version__)
```

## The Two Core Data Structures

### 1. `Series` — a 1D labeled array

A Series is like a NumPy 1D array, but with an explicit **index** (labels) attached to each value.

```python
import pandas as pd

s = pd.Series([10, 20, 30, 40])
print(s)
# 0    10
# 1    20
# 2    30
# 3    40
# dtype: int64

# Custom index
s2 = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
print(s2['b'])   # 20

# From a dictionary -- keys become the index
s3 = pd.Series({'apple': 5, 'banana': 3, 'cherry': 8})
```

### 2. `DataFrame` — a 2D labeled table

A DataFrame is a collection of Series sharing a common index — conceptually, a table with rows and columns, each column potentially having a different dtype (unlike a pure NumPy 2D array, which requires one uniform dtype).

```python
data = {
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'salary': [50000, 60000, 75000]
}

df = pd.DataFrame(data)
print(df)
#       name  age  salary
# 0    Alice   25   50000
# 1      Bob   30   60000
# 2  Charlie   35   75000
```

## Why Pandas over Raw NumPy for Tabular Data?

| Feature | NumPy | Pandas |
|---|---|---|
| Column dtypes | Must be uniform across the array | Each column can have its own dtype |
| Labels | Integer-only indices | Named, meaningful row/column labels |
| Missing data | Manual handling with `nan` | Built-in `NaN`/`NA` handling throughout |
| Grouping/aggregation | Manual, verbose | `.groupby()` — concise, powerful |
| Time series | No native support | Extensive datetime indexing/resampling |
| I/O | Limited (mostly plain text/binary) | Reads/writes CSV, Excel, SQL, JSON, Parquet, and more |

**Rule of thumb:** use NumPy for pure numerical arrays/matrices (especially in ML model math); use Pandas for anything resembling a real-world dataset with mixed types, labels, or missing values — which is most raw data science work.

## Key DataFrame Attributes

```python
df.shape        # (3, 3) -- (rows, columns)
df.columns      # Index(['name', 'age', 'salary'], dtype='object')
df.index        # RangeIndex(start=0, stop=3, step=1)
df.dtypes       # dtype of each column
df.values       # underlying NumPy array (loses column dtype heterogeneity if mixed)
df.info()       # summary: dtypes, non-null counts, memory usage
df.describe()   # summary statistics for numeric columns
```

```python
df.info()
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 3 entries, 0 to 2
# Data columns (total 3 columns):
#  #   Column  Non-Null Count  Dtype
# ---  ------  --------------  -----
#  0   name    3 non-null      object
#  1   age     3 non-null      int64
#  2   salary  3 non-null      int64
# dtypes: int64(2), object(1)
```

`.info()` and `.describe()` should be the **first two commands** you run on any new dataset — they immediately reveal dtypes, missing values, and the basic statistical shape of your numeric columns.

## Creating DataFrames: Common Patterns

```python
# From a dict of lists (most common in tutorials)
pd.DataFrame({'a': [1, 2], 'b': [3, 4]})

# From a list of dicts (common when parsing JSON/API responses)
pd.DataFrame([{'a': 1, 'b': 3}, {'a': 2, 'b': 4}])

# From a NumPy array, with explicit column names
import numpy as np
pd.DataFrame(np.random.default_rng(0).random((3, 2)), columns=['x', 'y'])

# Empty DataFrame with defined columns (useful for incrementally building results)
pd.DataFrame(columns=['id', 'prediction', 'confidence'])
```

## The Index: Pandas' Most Underrated Feature

Every Series and DataFrame has an **index** — labels for rows that persist through most operations (filtering, sorting, merging) and are used for **alignment**.

```python
df = pd.DataFrame({'value': [100, 200, 300]}, index=['x', 'y', 'z'])

df.loc['y']          # access by label
df.reset_index()      # move index back into a column, replace with default integer index
df.set_index('value') # promote a column to become the index
```

**Key insight:** unlike a NumPy array, Pandas objects are automatically **aligned by index** during arithmetic — this is powerful but can silently introduce `NaN`s if indices don't match between two Series/DataFrames being combined. Understanding index alignment prevents a very common class of bugs.

```python
a = pd.Series([1, 2, 3], index=['x', 'y', 'z'])
b = pd.Series([10, 20, 30], index=['y', 'z', 'w'])

print(a + b)
# w      NaN   <- no match in 'a'
# x      NaN   <- no match in 'b'
# y     12.0
# z     33.0
```

**Next:** `12_pandas_series_deep_dive.md`
