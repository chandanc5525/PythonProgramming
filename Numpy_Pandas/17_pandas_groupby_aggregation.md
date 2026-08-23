# 17. GroupBy & Aggregation

`groupby()` is arguably Pandas' single most powerful feature for data science — it implements the "split-apply-combine" pattern that underlies most real-world aggregate analysis (sales by region, average score by category, retention by cohort, etc).

## The Split-Apply-Combine Pattern

1. **Split** the data into groups based on some key(s)
2. **Apply** a function (aggregation, transformation, or filter) to each group independently
3. **Combine** the results back into a single output structure

```python
import pandas as pd

df = pd.DataFrame({
    'department': ['Eng', 'Eng', 'Sales', 'Sales', 'HR'],
    'employee': ['Alice', 'Bob', 'Carol', 'Dave', 'Eve'],
    'salary': [95000, 105000, 65000, 72000, 68000],
    'years': [3, 8, 5, 2, 4]
})

grouped = df.groupby('department')
print(grouped.groups)   # dict-like view of which rows belong to each group
```

## Basic Aggregation

```python
df.groupby('department')['salary'].mean()
df.groupby('department')['salary'].sum()
df.groupby('department')['salary'].agg(['mean', 'sum', 'count', 'std', 'min', 'max'])

df.groupby('department').mean(numeric_only=True)   # mean of ALL numeric columns per group
df.groupby('department').size()                     # row count per group (includes NaN rows)
df.groupby('department')['employee'].count()         # count of NON-NULL values per group
```

**`.size()` vs `.count()`:** `.size()` counts all rows per group (including NaN); `.count()` counts non-null values per column per group. This distinction matters when your grouping/aggregation columns have missing values.

## Multiple Grouping Keys

```python
df.groupby(['department', 'years']).mean(numeric_only=True)

# Group by a derived condition (not just an existing column)
df.groupby(df['years'] > 4)['salary'].mean()

# Group by multiple columns, custom aggregations per column
df.groupby('department').agg({
    'salary': ['mean', 'max'],
    'years': 'sum'
})
```

## Named Aggregations (Clean Output Column Names)

```python
df.groupby('department').agg(
    avg_salary=('salary', 'mean'),
    max_salary=('salary', 'max'),
    headcount=('employee', 'count')
).reset_index()
```

This produces clean, immediately usable column names instead of the default MultiIndex columns that come from `.agg(['mean', 'max'])` — strongly preferred for production reporting code.

## Custom Aggregation Functions

```python
df.groupby('department')['salary'].agg(lambda x: x.max() - x.min())   # custom range function

def salary_range(x):
    return x.max() - x.min()

df.groupby('department')['salary'].agg(salary_range)
```

## `.transform()` — Broadcasting Group Results Back to Row Level

Unlike `.agg()` (which collapses each group to one row), `.transform()` returns a result with the **same shape as the original DataFrame** — essential for feature engineering.

```python
# Add a column showing each employee's salary relative to their department's average
df['dept_avg_salary'] = df.groupby('department')['salary'].transform('mean')
df['salary_vs_dept_avg'] = df['salary'] - df['dept_avg_salary']

print(df[['employee', 'department', 'salary', 'dept_avg_salary', 'salary_vs_dept_avg']])
```

This "compare to group average" pattern is extremely common in feature engineering — e.g., "how does this transaction compare to the customer's average transaction," or "how does this player's score compare to their team's average."

## `.filter()` — Keeping/Dropping Entire Groups

```python
# Keep only departments with more than 1 employee
df.groupby('department').filter(lambda x: len(x) > 1)

# Keep only departments where average salary exceeds 70000
df.groupby('department').filter(lambda x: x['salary'].mean() > 70000)
```

## `.apply()` on Groups — Maximum Flexibility

```python
def top_earner(group):
    return group.loc[group['salary'].idxmax()]

df.groupby('department').apply(top_earner, include_groups=False)
```

`.apply()` on groups is the most flexible but slowest option — use `.agg()`/`.transform()` when possible, and reserve `.apply()` for genuinely custom, row-order-dependent, or multi-column logic that can't be expressed otherwise.

## Pivot Tables (GroupBy's Spreadsheet-Style Cousin)

```python
df.pivot_table(
    values='salary',
    index='department',
    columns='years',
    aggfunc='mean',
    fill_value=0
)

# Multiple aggregation functions
df.pivot_table(values='salary', index='department', aggfunc=['mean', 'count'])
```

`pivot_table` is essentially `groupby` + reshape combined, and is the direct equivalent of an Excel pivot table — extremely useful for building summary reports and cross-tabulations during EDA.

## `pd.crosstab` — Frequency Cross-Tabulation

```python
df2 = pd.DataFrame({
    'department': ['Eng', 'Eng', 'Sales', 'Sales', 'HR'],
    'level': ['Senior', 'Junior', 'Senior', 'Junior', 'Senior']
})

pd.crosstab(df2['department'], df2['level'])                 # counts
pd.crosstab(df2['department'], df2['level'], normalize='index')  # row-wise proportions
```

`crosstab` is the standard tool for quickly checking the relationship between two categorical variables (e.g., checking for class imbalance across a segmentation variable).

## Grouped Sorting: Top-N per Group

A very common real-world task — e.g., "top 2 highest-paid employees per department":

```python
df.sort_values('salary', ascending=False).groupby('department').head(2)

# Or using rank
df['rank_in_dept'] = df.groupby('department')['salary'].rank(ascending=False)
df[df['rank_in_dept'] <= 2]
```

**Next:** `18_pandas_merging_joining_concatenation.md`
