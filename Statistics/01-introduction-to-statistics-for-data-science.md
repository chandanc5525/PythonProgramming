# 1. Introduction to Statistics for Data Science

## Overview
Statistics is the discipline of collecting, organizing, analyzing, interpreting, and presenting data. In data science and analytics, statistics is the engine that turns raw numbers into trustworthy insight — it tells us not just *what* the data shows, but *how confident* we should be in that conclusion.

## Why Statistics Matters in Data Science
- **Descriptive layer**: summarizing what happened (sales last quarter, churn rate this month).
- **Inferential layer**: generalizing from a sample to a population (will this campaign work company-wide?).
- **Predictive layer**: statistics underlies machine learning — regression, classification, and probability models all rest on statistical foundations.
- **Decision layer**: statistics quantifies uncertainty so business leaders can make decisions under risk rather than guesswork.

## Two Branches of Statistics
1. **Descriptive statistics** — mean, median, mode, variance, charts. Answers "what happened?"
2. **Inferential statistics** — hypothesis tests, confidence intervals, regression. Answers "what can we conclude, and how sure are we?"

## The Data Science Workflow and Where Statistics Fits
`Business Question → Data Collection → Cleaning → Descriptive Stats (EDA) → Inferential Stats/Modeling → Communication → Decision`

Statistics touches every stage: designing how data is collected (sampling), summarizing it (EDA), testing hypotheses (A/B tests), building predictive models (regression/ML), and validating that results generalize (cross-validation, confidence intervals).

## Python Example
```python
import pandas as pd

df = pd.DataFrame({"revenue": [120, 135, 98, 140, 110, 150, 125]})
print(df.describe())  # instant descriptive statistics summary
```

## Business Application
A retail analyst uses descriptive statistics to summarize weekly sales, then inferential statistics to test whether a new store layout significantly increased average basket size — moving from "what happened" to "what should we do next."

## Key Takeaways
- Statistics is the foundation beneath data science, analytics, and machine learning.
- Descriptive statistics summarize; inferential statistics generalize and quantify uncertainty.
- Every business decision backed by data is, implicitly, a statistical decision.
