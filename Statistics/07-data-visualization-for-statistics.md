# 7. Data Visualization for Statistical Analysis

## Overview
Visualization is exploratory statistics made visible — the fastest way to detect patterns, outliers, and distribution shape before running formal tests.

## Core Chart Types and Their Statistical Purpose
- **Histogram**: shows distribution shape, skew, modality.
- **Box plot**: shows median, quartiles, and outliers at a glance (five-number summary).
- **Scatter plot**: reveals relationships/correlation between two continuous variables.
- **Bar chart**: compares a metric across categorical groups.
- **Line chart**: shows a metric's trend over time (time series).
- **Heatmap**: visualizes a correlation matrix across many variables at once.

## Reading a Box Plot
```
   min |---[ Q1 --- median --- Q3 ]---| max
              (IQR = Q3 - Q1)
Outliers plotted as individual points beyond 1.5 × IQR from Q1/Q3.
```

## Best Practices
- Match the chart to the data type (categorical vs continuous, see Topic 2).
- Always label axes and units — an unlabeled chart is not analysis.
- Avoid 3D effects and truncated y-axes; both distort statistical perception.
- Use small multiples (faceting) to compare distributions across groups fairly.

## Python Example
```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.DataFrame({"dept": ["Sales"]*50 + ["Eng"]*50,
                    "salary": list(np.random.normal(70,10,50)) + list(np.random.normal(95,15,50))})
sns.boxplot(data=df, x="dept", y="salary")
plt.title("Salary Distribution by Department")
plt.show()
```

## Business Application
Before running a formal A/B test, a growth analyst plots histograms of conversion rates for the control and treatment groups — immediately spotting a skewed distribution and outlier days (e.g., a promo event) that would otherwise distort a naive t-test.

## Key Takeaways
- Visualization is the first, essential step of exploratory data analysis (EDA), not an afterthought.
- Box plots and histograms reveal shape and outliers that summary numbers alone can hide.
- Good visualization practice prevents both analytical errors and misleading stakeholder communication.
