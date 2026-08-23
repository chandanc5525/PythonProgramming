# 15. Advanced Indexing and Selection

Building on file 13's `.loc`/`.iloc` basics, this file covers more advanced selection patterns that show up constantly in real data science workflows.

## Setting Values Safely: `SettingWithCopyWarning`

One of the most common (and most confusing to beginners) warnings in Pandas.

```python
import pandas as pd

df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

# BAD -- ambiguous whether this modifies a view or a copy; triggers a warning
subset = df[df['a'] > 1]
subset['b'] = 0    # SettingWithCopyWarning!

# GOOD -- use .loc for chained selection + assignment in one step
df.loc[df['a'] > 1, 'b'] = 0

# GOOD -- explicitly copy when you intend to work on a separate subset
subset = df[df['a'] > 1].copy()
subset['b'] = 0    # safe, no warning, no ambiguity
```

**Rule to internalize:** whenever you filter a DataFrame and intend to modify the result, either (1) do the assignment in a single `.loc[...]` statement, or (2) call `.copy()` explicitly. Chained indexing like `df[condition]['col'] = value` is unreliable — sometimes it works, sometimes it silently fails to modify the original.

## MultiIndex (Hierarchical Indexing)

MultiIndex lets you index by more than one level — common after `groupby()` with multiple keys, or for naturally hierarchical data (e.g., Year > Quarter > Month).

```python
arrays = [['2023', '2023', '2024', '2024'], ['Q1', 'Q2', 'Q1', 'Q2']]
index = pd.MultiIndex.from_arrays(arrays, names=['year', 'quarter'])
df = pd.DataFrame({'revenue': [100, 120, 130, 150]}, index=index)

df.loc['2023']              # all rows for 2023 -- returns a DataFrame
df.loc[('2023', 'Q1')]      # a specific (year, quarter) combination
df.loc[('2023', 'Q1'), 'revenue']   # specific cell

df.reset_index()             # flatten the MultiIndex back into regular columns
df.unstack()                 # pivot the inner index level into columns
```

**Data science use case:** MultiIndex is what you get automatically from `df.groupby(['year', 'quarter']).sum()` — understanding how to navigate it is essential for working with grouped/aggregated results.

## `.at[]` and `.iat[]` — Fast Scalar Access

```python
df = pd.DataFrame({'a': [1, 2, 3]}, index=['x', 'y', 'z'])

df.at['x', 'a']    # fast label-based single-value access (faster than .loc for scalars)
df.iat[0, 0]        # fast position-based single-value access
```

Use `.at`/`.iat` instead of `.loc`/`.iloc` when accessing a **single scalar value** in performance-sensitive loops (e.g., inside a function called millions of times) — they skip overhead that `.loc`/`.iloc` incur for supporting more general selections.

## Conditional Selection with `.query()`

An alternative, often more readable syntax for filtering, especially with multiple conditions:

```python
df = pd.DataFrame({'age': [25, 35, 45], 'salary': [50000, 70000, 90000], 'dept': ['Eng', 'Sales', 'Eng']})

df.query('age > 30 and salary > 60000')
df.query('dept == "Eng"')

# Referencing external variables with @
threshold = 60000
df.query('salary > @threshold')
```

`.query()` can also be faster than boolean indexing on very large DataFrames because it uses the `numexpr` library for optimized expression evaluation (if installed).

## `.isin()` for Membership Testing

```python
df[df['dept'].isin(['Eng', 'HR'])]           # keep rows where dept is in this list
df[~df['dept'].isin(['Eng', 'HR'])]           # keep rows where dept is NOT in this list
```

Much cleaner than chaining multiple `==` conditions with `|`.

## `.between()` for Range Filtering

```python
df[df['age'].between(25, 40)]     # inclusive range filter, cleaner than (age>=25) & (age<=40)
```

## Selecting Columns by dtype

```python
df.select_dtypes(include='number')      # only numeric columns
df.select_dtypes(include='object')      # only string/object columns
df.select_dtypes(exclude='number')      # everything except numeric
df.select_dtypes(include=['int64', 'float64'])
```

**Data science use case:** essential for preprocessing pipelines that need to apply different transformations to numeric vs. categorical columns (e.g., scaling numeric features, one-hot encoding categorical ones).

```python
numeric_cols = df.select_dtypes(include='number').columns
categorical_cols = df.select_dtypes(include='object').columns
```

## Filtering Columns by Name Pattern

```python
df.filter(like='sales')             # columns containing 'sales' in the name
df.filter(regex='^price_')          # columns matching a regex pattern
df.filter(items=['a', 'b'])          # exact column name matches (like a safer subset selection)
```

## Reindexing

```python
df = pd.DataFrame({'a': [1, 2, 3]}, index=['x', 'y', 'z'])

new_index = ['w', 'x', 'y', 'z']
df.reindex(new_index)          # rows not present become NaN; 'w' will be NaN
df.reindex(new_index, fill_value=0)   # fill missing rows with 0 instead of NaN
```

**Data science use case:** reindexing is common when aligning time series data to a complete, regular date range (filling in gaps for missing dates) — covered further in file 19.

**Next:** `16_pandas_data_cleaning_missing_data.md`
