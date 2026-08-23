# NumPy & Pandas: Beginner to Depth (20 Files)

A structured learning path through NumPy and Pandas, written from a **data scientist's implementation perspective** — every concept is tied to a real EDA, feature engineering, or modeling use case, not just syntax.

Inspired by / complementary to [chandanc5525/PythonProgramming](https://github.com/chandanc5525/PythonProgramming).

## How to Use This

Read the files in order — each builds on the last. Files 01–10 build the NumPy foundation (arrays, broadcasting, linear algebra). Files 11–20 build on top of that foundation with Pandas (DataFrames, cleaning, groupby, time series). File 20 ties everything together into an end-to-end workflow.

## NumPy (Foundations)

| # | File | Covers |
|---|---|---|
| 01 | `01_numpy_introduction_and_installation.md` | What NumPy is, why it's fast, the `ndarray` object |
| 02 | `02_numpy_arrays_basics.md` | dtypes, type conversion, creation shortcuts, copies vs. views |
| 03 | `03_numpy_array_creation_methods.md` | arange/linspace/logspace, random arrays, meshgrids, file I/O |
| 04 | `04_numpy_indexing_slicing.md` | Basic/boolean/fancy indexing, `np.where`, `np.select` |
| 05 | `05_numpy_array_operations_broadcasting.md` | Vectorized math, broadcasting rules, normalization, distances |
| 06 | `06_numpy_mathematical_statistical_functions.md` | Aggregations, the `axis` parameter, percentiles, NaN-safe stats |
| 07 | `07_numpy_reshaping_stacking_splitting.md` | reshape, transpose, stack/concatenate, train/test-style splits |
| 08 | `08_numpy_linear_algebra.md` | Matrix multiplication, inverse, normal equation, PCA, SVD, norms |
| 09 | `09_numpy_random_module.md` | Modern `Generator` API, sampling, bootstrapping, Monte Carlo |
| 10 | `10_numpy_advanced_performance_optimization.md` | Vectorization, strides, einsum, numerical stability |

## Pandas (Tabular Data Workflows)

| # | File | Covers |
|---|---|---|
| 11 | `11_pandas_introduction_and_data_structures.md` | Series & DataFrame basics, index alignment |
| 12 | `12_pandas_series_deep_dive.md` | Series indexing, `.map`/`.apply`, value_counts, alignment |
| 13 | `13_pandas_dataframe_basics.md` | `.loc`/`.iloc`, filtering, sorting, column ops |
| 14 | `14_pandas_reading_writing_data.md` | CSV/Excel/JSON/SQL/Parquet I/O, chunking, memory reduction |
| 15 | `15_pandas_indexing_selection.md` | SettingWithCopyWarning, MultiIndex, `.query()`, dtype selection |
| 16 | `16_pandas_data_cleaning_missing_data.md` | Missing data, imputation strategies, outliers, string cleaning |
| 17 | `17_pandas_groupby_aggregation.md` | split-apply-combine, `.transform()`, pivot tables, crosstab |
| 18 | `18_pandas_merging_joining_concatenation.md` | SQL-style joins, concat, merge validation, row-explosion bugs |
| 19 | `19_pandas_time_series_analysis.md` | Datetime parsing, resampling, rolling windows, lag features |
| 20 | `20_pandas_advanced_performance_real_world_workflows.md` | Method chaining, performance, categoricals, end-to-end pipeline |

## Prerequisites

```bash
pip install numpy pandas
# Optional, used in some examples:
pip install scipy openpyxl pyarrow
```

## Philosophy

Each file explains **why** a concept matters for real data science work — not just the syntax, but the connection to EDA, feature engineering, model input requirements (scikit-learn conventions), and common real-world bugs (shape mismatches, SettingWithCopyWarning, join row-explosions, NaN propagation). Code examples are runnable and self-contained.
