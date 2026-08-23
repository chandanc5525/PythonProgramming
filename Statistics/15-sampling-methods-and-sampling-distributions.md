# 15. Sampling Methods and Sampling Distributions

## Overview
How a sample is drawn determines whether inferences about the population will be valid. Good statistics starts with good sampling design, not just good analysis.

## Common Sampling Methods
- **Simple random sampling**: every member of the population has equal chance of selection — gold standard, minimizes bias.
- **Stratified sampling**: population divided into subgroups (strata) by a key characteristic (region, age group), then randomly sampled within each — ensures representation of subgroups.
- **Cluster sampling**: population divided into clusters (e.g., stores), a random subset of clusters is fully sampled — cost-efficient for geographically spread populations.
- **Systematic sampling**: select every kth member from a list (e.g., every 10th customer) — simple, but risks bias if there's periodicity in the list.
- **Convenience sampling**: sampling whoever is easiest to reach — fast but prone to significant bias; avoid for rigorous inference.

## Sampling Distribution
The probability distribution of a statistic (e.g., the sample mean) computed from repeated random samples of the same size from a population. Its spread — the **standard error** — quantifies how much the statistic varies from sample to sample.

## Choosing a Method
| Goal | Recommended Method |
|---|---|
| Ensure subgroup representation | Stratified |
| Minimize field costs, geographically spread population | Cluster |
| Fully unbiased, resources available | Simple random |
| Quick approximation, ordered list available | Systematic |

## Python Example
```python
import pandas as pd

df = pd.DataFrame({"region": ["N","S","E","W"]*250, "spend": range(1000)})

# Stratified sample: 10% from each region
stratified = df.groupby("region", group_keys=False).apply(lambda x: x.sample(frac=0.1))
print(stratified["region"].value_counts())
```

## Business Application
A national retailer uses stratified sampling by region when surveying customer satisfaction, ensuring that smaller regions aren't drowned out by larger ones in a simple random sample — producing more reliable, generalizable insight per region.

## Key Takeaways
- The sampling method determines whether a sample is representative — no amount of clever analysis fixes a biased sample.
- Stratified sampling improves precision when subgroups matter; cluster sampling improves cost-efficiency.
- The sampling distribution (not the raw data distribution) is what inferential statistics is actually built on.
