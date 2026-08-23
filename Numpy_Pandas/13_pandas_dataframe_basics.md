# 13. DataFrame Basics

## Creating and Inspecting DataFrames

```python
import pandas as pd

df = pd.DataFrame({
    'employee': ['Alice', 'Bob', 'Charlie', 'Dana'],
    'department': ['Eng', 'Sales', 'Eng', 'HR'],
    'salary': [95000, 65000, 105000, 72000],
    'years': [3, 5, 8, 2]
})

df.head()        # first 5 rows (default) -- your first look at any dataset
df.tail(2)        # last 2 rows
df.sample(3)      # 3 random rows -- better than head() for spotting data issues
df.shape          # (4, 4)
df.info()         # dtypes + non-null counts + memory
df.describe()     # statistical summary of numeric columns
df.describe(include='object')   # summary of categorical/string columns
```

**Best practice:** always use `.sample()` in addition to `.head()` during initial EDA — `.head()` only shows the top of the file, which can hide data quality issues that appear later (e.g., a format change halfway through a scraped dataset).

## Selecting Columns

```python
df['salary']              # single column -> returns a Series
df[['salary', 'years']]   # multiple columns -> returns a DataFrame (note the double brackets!)

df.salary                  # attribute-style access -- works but AVOID for columns with
                            # spaces, special characters, or names matching DataFrame methods
```

**Common beginner mistake:** `df['salary']` returns a Series, while `df[['salary']]` (double brackets) returns a single-column DataFrame. This distinction matters when chaining `.merge()`, `.join()`, or any method expecting a DataFrame shape.

## Selecting Rows: `.loc` vs `.iloc`

This is the single most important distinction to master in Pandas.

```python
df = pd.DataFrame({'a': [10, 20, 30], 'b': [40, 50, 60]}, index=['x', 'y', 'z'])

# .loc -- LABEL-based selection (inclusive of end label in slices)
df.loc['x']              # row with label 'x'
df.loc['x':'y']          # rows x through y, INCLUSIVE
df.loc['x', 'a']         # specific cell by label
df.loc[:, 'a']           # all rows, column 'a'
df.loc[df['a'] > 15]     # boolean condition (very common!)

# .iloc -- POSITION-based selection (exclusive of end, like Python lists)
df.iloc[0]                # first row by position
df.iloc[0:2]               # rows 0 and 1, position-based, EXCLUDES position 2
df.iloc[0, 1]               # cell at row 0, column 1
df.iloc[:, 0]               # all rows, first column
```

| | `.loc` | `.iloc` |
|---|---|---|
| Selects by | Labels | Integer positions |
| Slice end | Inclusive | Exclusive |
| Use when | You know column/index names | You need positional access (e.g., first N rows) |

**Rule of thumb:** default to `.loc` for anything condition-based or when working with named columns (the vast majority of real work); use `.iloc` when you specifically need positional slicing (e.g., "give me the first 100 rows for a quick sample").

## Adding, Modifying, Dropping Columns

```python
df['bonus'] = df['salary'] * 0.1                    # new column from vectorized computation
df['seniority'] = df['years'].apply(lambda y: 'senior' if y >= 5 else 'junior')

df['salary'] = df['salary'] + 5000                   # modify existing column in place

df.drop(columns=['bonus'])                            # returns a NEW DataFrame (original untouched)
df.drop(columns=['bonus'], inplace=True)               # modifies in place -- use cautiously
df = df.drop(columns=['bonus'])                         # the safer, more explicit pattern
```

**Best practice:** avoid `inplace=True` in most modern pandas workflows. It doesn't actually save memory in most cases, makes method chaining harder, and has been a source of subtle bugs and deprecation churn across pandas versions. Prefer reassignment (`df = df.drop(...)`).

## Renaming and Reordering

```python
df.rename(columns={'employee': 'name'})               # rename specific columns
df.columns = ['name', 'dept', 'salary', 'years']        # replace ALL column names at once

df[['salary', 'name', 'dept', 'years']]                  # reorder by selecting in desired order
```

## Filtering Rows (Boolean Indexing — Same Concept as NumPy)

```python
df[df['salary'] > 70000]
df[(df['department'] == 'Eng') & (df['years'] > 2)]     # AND -- use & with parentheses
df[(df['department'] == 'Eng') | (df['department'] == 'HR')]  # OR

# Cleaner alternative to multiple == | chains:
df[df['department'].isin(['Eng', 'HR'])]

# Negation
df[~(df['department'] == 'Sales')]

# String-based filtering
df[df['employee'].str.startswith('A')]
df[df['employee'].str.contains('a', case=False)]
```

## Sorting

```python
df.sort_values('salary')                              # ascending by default
df.sort_values('salary', ascending=False)
df.sort_values(['department', 'salary'], ascending=[True, False])  # multi-column sort
df.sort_index()                                         # sort by row index/label
```

## Applying Functions Row-wise / Column-wise

```python
df.apply(lambda col: col.max(), axis=0)     # apply down each COLUMN (axis=0, default)
df.apply(lambda row: row['salary'] / row['years'], axis=1)  # apply across each ROW (axis=1)
```

**Performance warning:** `axis=1` row-wise `.apply()` is notoriously slow on large DataFrames because it essentially loops in Python, row by row. Whenever possible, replace it with vectorized column operations:

```python
# SLOW
df['salary_per_year'] = df.apply(lambda row: row['salary'] / row['years'], axis=1)

# FAST -- vectorized, operates on entire columns at once
df['salary_per_year'] = df['salary'] / df['years']
```

**Next:** `14_pandas_reading_writing_data.md`
