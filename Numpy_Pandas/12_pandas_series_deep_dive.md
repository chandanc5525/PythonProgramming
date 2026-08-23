# 12. Pandas Series: Deep Dive

While DataFrames get most of the attention, understanding Series deeply matters because **every column of a DataFrame is a Series** — everything you learn here applies directly to column-level operations.

## Creating Series

```python
import pandas as pd
import numpy as np

pd.Series([1, 2, 3])                          # default RangeIndex
pd.Series([1, 2, 3], index=['a', 'b', 'c'])   # custom index
pd.Series(5, index=['a', 'b', 'c'])            # scalar broadcast to every index
pd.Series({'a': 1, 'b': 2})                    # from dict -- keys become index
pd.Series(np.arange(5))                        # from a NumPy array
```

## Attributes and Inspection

```python
s = pd.Series([10, 20, 30, np.nan, 50], name='sales')

s.name        # 'sales'
s.dtype       # float64 (NaN forces float, since int can't represent NaN)
s.index       # RangeIndex(start=0, stop=5, step=1)
s.values      # underlying NumPy array: [10. 20. 30. nan 50.]
s.shape       # (5,)
s.size        # 5
s.isnull()    # boolean mask of missing values
s.notnull()   # inverse
```

**Important gotcha:** integer Series containing any `NaN` are automatically upcast to `float64`, because NumPy's `int64` cannot represent `NaN`. This is a very common source of "why did my ID column become a float?" confusion. Pandas' newer **nullable integer type** (`Int64`, capital I) solves this:

```python
s_nullable = pd.Series([1, 2, None], dtype='Int64')   # stays integer, uses pd.NA instead of NaN
print(s_nullable)
# 0       1
# 1       2
# 2    <NA>
# dtype: Int64
```

## Indexing a Series

```python
s = pd.Series([10, 20, 30, 40], index=['a', 'b', 'c', 'd'])

s['b']            # label-based access: 20
s.loc['b']        # explicit label-based access (preferred, unambiguous)
s.iloc[1]         # explicit position-based access: 20

s[['a', 'c']]     # multiple labels
s.iloc[0:2]       # positional slicing

s.loc['a':'c']    # label-based slicing -- INCLUSIVE of the end label (unlike Python slicing!)
```

**Critical distinction:** `.loc` slicing is **inclusive** of the endpoint (`'a':'c'` includes `'c'`), while `.iloc` slicing is exclusive like standard Python slicing (`0:2` excludes index 2). This asymmetry trips up almost everyone at some point.

## Vectorized Operations (Same Mental Model as NumPy)

```python
s = pd.Series([1, 2, 3, 4, 5])

s * 2                 # element-wise
s[s > 2]               # boolean filtering
s.apply(lambda x: x ** 2)   # apply a custom function element-wise
```

## `.map()`, `.apply()`, and Vectorized Alternatives

```python
s = pd.Series(['apple', 'banana', 'cherry'])

# .map() -- element-wise transform, great for simple lookups/dicts
s.map({'apple': 'fruit A', 'banana': 'fruit B', 'cherry': 'fruit C'})
s.map(len)                     # length of each string

# .apply() -- more general, can be a custom function
s.apply(lambda x: x.upper())

# String methods via the .str accessor (usually faster & cleaner than .apply for string ops)
s.str.upper()
s.str.len()
s.str.contains('an')
```

**Performance note:** `.apply()` with a Python lambda is convenient but runs a Python-level loop under the hood (similar to `np.vectorize`) — it is **not** truly vectorized. Whenever there's a built-in vectorized alternative (`.str.upper()` instead of `.apply(str.upper)`, or arithmetic operators instead of `.apply(lambda x: x*2)`), prefer it for performance on large datasets.

## Handling Duplicates

```python
s = pd.Series([1, 2, 2, 3, 3, 3])

s.unique()          # array([1, 2, 3]) -- unique values
s.nunique()          # 3 -- count of unique values
s.value_counts()     # frequency count of each unique value, sorted descending
s.duplicated()       # boolean mask: True where value is a duplicate of an earlier one
s.drop_duplicates()  # remove duplicate values
```

`.value_counts()` is one of the single most-used EDA commands — instantly reveals class balance in a target variable, or the frequency distribution of a categorical feature.

```python
labels = pd.Series(['spam', 'ham', 'ham', 'spam', 'ham', 'ham'])
print(labels.value_counts())
# ham     4
# spam    2

print(labels.value_counts(normalize=True))   # as proportions instead of counts
# ham     0.666667
# spam    0.333333
```

## Sorting

```python
s = pd.Series([30, 10, 20], index=['c', 'a', 'b'])

s.sort_values()          # sort by value, ascending
s.sort_values(ascending=False)
s.sort_index()           # sort by index label
```

## Combining Series (Alignment Behavior)

```python
a = pd.Series([1, 2, 3], index=['x', 'y', 'z'])
b = pd.Series([10, 20, 30], index=['x', 'y', 'z'])

a + b            # element-wise, aligned by index
a.add(b, fill_value=0)   # like + but fills missing alignment gaps with 0 instead of NaN
```

Using `.add()`, `.sub()`, `.mul()`, `.div()` with `fill_value` is the standard way to combine two Series that might not perfectly overlap, without silently losing data to `NaN`.

**Next:** `13_pandas_dataframe_basics.md`
