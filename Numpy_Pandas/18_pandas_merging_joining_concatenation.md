# 18. Merging, Joining, and Concatenating DataFrames

Real data science work rarely involves a single, clean, already-joined dataset. Combining data from multiple tables/sources (customers + orders + products, or logs from multiple days) is a core daily skill — this is the Pandas equivalent of SQL JOINs.

## `pd.concat()` — Stacking DataFrames

Use `concat` to combine DataFrames along an axis, when the DataFrames are conceptually the same "shape" (same columns, or same rows).

```python
import pandas as pd

df1 = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
df2 = pd.DataFrame({'a': [5, 6], 'b': [7, 8]})

# Stack rows (axis=0, default) -- e.g., combining monthly data files
pd.concat([df1, df2])                       # keeps original indices (may have duplicates!)
pd.concat([df1, df2], ignore_index=True)    # reset to a clean 0..n index -- usually what you want

# Stack columns (axis=1) -- e.g., combining features computed separately
pd.concat([df1, df2], axis=1)
```

**Common real-world pattern:** combining many CSV files (e.g., daily logs) into one DataFrame:

```python
import glob
files = glob.glob('data/sales_*.csv')
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
```

## `pd.merge()` — SQL-Style Joins

```python
customers = pd.DataFrame({
    'customer_id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Carol']
})

orders = pd.DataFrame({
    'order_id': [101, 102, 103, 104],
    'customer_id': [1, 2, 2, 4],   # note: customer_id 4 doesn't exist in customers; 3 has no orders
    'amount': [250, 100, 75, 300]
})

pd.merge(customers, orders, on='customer_id', how='inner')  # only matching rows in BOTH
pd.merge(customers, orders, on='customer_id', how='left')   # all customers, matching orders (NaN if none)
pd.merge(customers, orders, on='customer_id', how='right')  # all orders, matching customers (NaN if none)
pd.merge(customers, orders, on='customer_id', how='outer')  # everything, NaN where no match on either side
```

### Join Types Explained (Same as SQL)

| `how` | Result |
|---|---|
| `inner` (default) | Only rows with matching keys in BOTH DataFrames |
| `left` | All rows from the left DataFrame; matching rows from the right (NaN if no match) |
| `right` | All rows from the right DataFrame; matching rows from the left (NaN if no match) |
| `outer` | All rows from both; NaN where there's no match on either side |

**Choosing the right join is a modeling decision, not just a syntax choice** — e.g., using `inner` when you meant `left` will silently drop customers who never placed an order, which could badly bias a churn analysis.

## Handling Mismatched Column Names

```python
customers2 = customers.rename(columns={'customer_id': 'cust_id'})

pd.merge(customers2, orders, left_on='cust_id', right_on='customer_id')
```

## Merging on the Index

```python
pd.merge(customers.set_index('customer_id'), orders.set_index('customer_id'),
          left_index=True, right_index=True)

# Shortcut for index-based joins:
customers.set_index('customer_id').join(orders.set_index('customer_id'), how='left')
```

`.join()` is a convenience method specifically for merging on the index — slightly more concise syntax than `merge()` for that common case.

## Detecting and Handling Merge Issues

```python
# Check for duplicate keys BEFORE merging -- a major source of "row explosion" bugs
print(orders['customer_id'].duplicated().sum())

# The indicator flag reveals exactly where rows came from -- invaluable for debugging joins
merged = pd.merge(customers, orders, on='customer_id', how='outer', indicator=True)
print(merged['_merge'].value_counts())
# both          2
# left_only     1   <- customer with no orders
# right_only    1   <- order with no matching customer
```

**Critical habit:** always check `merged.shape[0]` against `left.shape[0]` and `right.shape[0]` after a merge. If the merged row count is unexpectedly large, you likely have duplicate keys causing a many-to-many "row explosion" (a very common and hard-to-notice bug — e.g., 100 rows becoming 10,000 rows).

```python
# Validate assumptions about the join's cardinality explicitly
pd.merge(customers, orders, on='customer_id', validate='one_to_many')
# Raises a clear MergeError immediately if the assumption is violated
```

## Concatenating with Different Columns

```python
df1 = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
df2 = pd.DataFrame({'a': [5, 6], 'c': [7, 8]})

pd.concat([df1, df2])
#      a    b    c
# 0    1  3.0  NaN
# 1    2  4.0  NaN
# 0    5  NaN  7.0
# 1    6  NaN  8.0
```

Mismatched columns produce `NaN` for missing values — always check `df.columns` on inputs before concatenating to avoid unintentionally sparse results.

## `.combine_first()` — Filling Gaps from Another DataFrame

```python
df_primary = pd.DataFrame({'a': [1, None, 3]})
df_backup = pd.DataFrame({'a': [10, 20, 30]})

df_primary.combine_first(df_backup)   # fills NaN in df_primary using df_backup's values at same position
```

**Use case:** merging data from a primary and fallback/backup source — e.g., combining survey responses from two collection rounds, using round 2 to fill in gaps left from round 1.

**Next:** `19_pandas_time_series_analysis.md`
