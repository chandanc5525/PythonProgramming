# 3. Population vs Sample

## Overview
Almost all real-world analytics is built on **samples**, not entire populations. Understanding the distinction — and the parameters/statistics that describe each — is the gateway to inferential statistics.

## Definitions
- **Population**: the entire group you want to draw conclusions about (all customers, all transactions ever).
- **Sample**: a subset of the population actually observed/measured.
- **Parameter**: a numerical summary of a population (population mean μ, population proportion p) — usually unknown.
- **Statistic**: a numerical summary of a sample (sample mean x̄, sample proportion p̂) — used to estimate the parameter.

## Why We Sample
- Populations are often too large, expensive, or impossible to fully measure (e.g., "all future customers").
- A well-drawn sample, analyzed correctly, lets us infer population characteristics with quantifiable uncertainty.

## Sampling Error vs Bias
- **Sampling error**: natural variation between a sample statistic and the true population parameter, purely from randomness — shrinks as sample size grows.
- **Bias**: systematic error from a flawed sampling method (e.g., only surveying app users about a website feature) — does **not** shrink with more data.

## Notation Convention
| Concept | Population | Sample |
|---|---|---|
| Mean | μ | x̄ |
| Std. Dev. | σ | s |
| Proportion | p | p̂ |
| Size | N | n |

## Python Example
```python
import numpy as np

population = np.random.normal(loc=50, scale=10, size=100000)
sample = np.random.choice(population, size=200, replace=False)

print("Population mean:", population.mean())
print("Sample mean:", sample.mean())  # close, but not identical — sampling error
```

## Business Application
A telecom company cannot survey all 20 million subscribers about satisfaction. It draws a random sample of 2,000, computes the sample mean satisfaction score, and uses inferential statistics to estimate the true population satisfaction with a margin of error.

## Key Takeaways
- Population parameters are usually unknown; sample statistics estimate them.
- Random sampling minimizes bias; larger samples reduce (but never eliminate) sampling error.
- Every inferential technique later in this series exists to quantify the gap between statistic and parameter.
