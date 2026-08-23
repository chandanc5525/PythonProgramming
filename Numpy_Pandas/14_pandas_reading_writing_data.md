# 14. Reading and Writing Data

Real data science work starts with getting data *into* Pandas correctly, and often ends with saving results *out*. This is where subtle bugs (wrong dtypes, encoding issues, memory blowups) commonly begin.

## CSV Files (Most Common Format)

```python
import pandas as pd

df = pd.read_csv('data.csv')

# Common, important parameters:
df = pd.read_csv(
    'data.csv',
    sep=',',                     # delimiter (use '\t' for TSV)
    header=0,                    # row to use as column names (None if no header)
    index_col=0,                 # use first column as the row index
    usecols=['name', 'salary'],  # load only specific columns -- saves memory
    dtype={'id': str},           # force specific dtypes (e.g., keep IDs as strings, not int)
    parse_dates=['signup_date'], # automatically parse date columns to datetime64
    na_values=['NA', 'missing', '?'],  # additional strings to treat as missing
    nrows=1000,                  # load only first N rows (useful for quick testing on big files)
    encoding='utf-8',            # explicit encoding (try 'latin-1' if utf-8 fails)
)

df.to_csv('output.csv', index=False)   # index=False avoids writing the row index as a column
```

**Critical habit:** always inspect `df.dtypes` immediately after loading a CSV. Numeric-looking columns are sometimes loaded as `object` (string) due to stray characters, mixed formats, or missing-value placeholders that pandas doesn't recognize automatically.

```python
# Common cleanup pattern for a numeric column loaded as text
df['price'] = pd.to_numeric(df['price'], errors='coerce')   # invalid parsing becomes NaN
```

## Excel Files

```python
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')
df = pd.read_excel('data.xlsx', sheet_name=None)   # dict of ALL sheets: {sheet_name: DataFrame}

df.to_excel('output.xlsx', index=False, sheet_name='Results')

# Writing multiple sheets
with pd.ExcelWriter('output.xlsx') as writer:
    df1.to_excel(writer, sheet_name='Summary', index=False)
    df2.to_excel(writer, sheet_name='Details', index=False)
```

Requires `openpyxl` (`pip install openpyxl`) for `.xlsx` files.

## JSON

```python
df = pd.read_json('data.json')

# For nested JSON (very common with API responses), flatten with json_normalize
import json
with open('nested.json') as f:
    raw = json.load(f)
df = pd.json_normalize(raw, record_path='items', meta=['id', 'timestamp'])

df.to_json('output.json', orient='records', lines=True)   # 'records' + lines=True = JSONL, common for logs
```

## SQL Databases

```python
import sqlite3
# or: from sqlalchemy import create_engine

conn = sqlite3.connect('database.db')
df = pd.read_sql('SELECT * FROM sales WHERE year = 2025', conn)
df = pd.read_sql_table('sales', conn)   # read entire table

df.to_sql('results_table', conn, if_exists='replace', index=False)
```

Using SQLAlchemy engines (`create_engine('postgresql://...')`) is preferred over raw `sqlite3`/DB-API connections when working with production databases (Postgres, MySQL) — it's the officially supported interface for `read_sql`.

## Parquet (Preferred for Large Data / Production Pipelines)

```python
df.to_parquet('data.parquet', index=False)
df = pd.read_parquet('data.parquet')
```

**Why Parquet over CSV for real pipelines:**
- Preserves exact dtypes (no re-parsing/inference needed on load)
- Columnar storage — much faster reads when you only need specific columns
- Compressed by default — significantly smaller file sizes
- Standard format in the modern data stack (Spark, data lakes, BigQuery, dbt)

Requires `pyarrow` or `fastparquet` (`pip install pyarrow`).

## Handling Large Files: Chunking

When a file is too large to fit comfortably in memory:

```python
chunk_iter = pd.read_csv('huge_file.csv', chunksize=100_000)

total = 0
for chunk in chunk_iter:
    total += chunk['sales'].sum()    # process one chunk at a time

# Or filter/aggregate and concatenate results
filtered_chunks = []
for chunk in pd.read_csv('huge_file.csv', chunksize=100_000):
    filtered_chunks.append(chunk[chunk['status'] == 'active'])
result = pd.concat(filtered_chunks, ignore_index=True)
```

## Reducing Memory Usage on Load

```python
df.memory_usage(deep=True)          # actual memory usage per column, including object overhead
df.memory_usage(deep=True).sum() / 1024**2   # total memory in MB

# Downcast numeric types where the range allows it
df['id'] = pd.to_numeric(df['id'], downcast='integer')
df['price'] = pd.to_numeric(df['price'], downcast='float')

# Convert low-cardinality string columns to 'category' dtype -- huge memory savings
df['department'] = df['department'].astype('category')
```

Converting repetitive string columns (e.g., country, category, status) to `category` dtype is one of the highest-leverage memory optimizations in Pandas — it stores each unique value once and uses compact integer codes internally, often cutting memory usage for that column by 80-90%+.

## Quick Reference: Common `read_*` / `to_*` Pairs

| Format | Read | Write |
|---|---|---|
| CSV | `pd.read_csv()` | `df.to_csv()` |
| Excel | `pd.read_excel()` | `df.to_excel()` |
| JSON | `pd.read_json()` | `df.to_json()` |
| SQL | `pd.read_sql()` | `df.to_sql()` |
| Parquet | `pd.read_parquet()` | `df.to_parquet()` |
| Pickle | `pd.read_pickle()` | `df.to_pickle()` |
| HTML tables | `pd.read_html()` | `df.to_html()` |
| Clipboard | `pd.read_clipboard()` | `df.to_clipboard()` |

`pd.read_clipboard()` is a handy trick for quickly pulling in a small table you've copied from a spreadsheet or webpage during interactive exploration.

**Next:** `15_pandas_indexing_selection.md`
