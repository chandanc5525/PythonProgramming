# 25. Simple Linear Regression

## Overview
Simple linear regression models the relationship between one predictor (independent variable) and one continuous outcome (dependent variable), enabling both explanation and prediction.

## The Model
y = β₀ + β₁x + ε

- **β₀ (intercept)**: predicted value of y when x = 0.
- **β₁ (slope)**: expected change in y for a one-unit increase in x.
- **ε (error term)**: the part of y not explained by x.

Coefficients are estimated via **Ordinary Least Squares (OLS)** — minimizing the sum of squared residuals (differences between actual and predicted y).

## Key Outputs to Interpret
- **R² (coefficient of determination)**: proportion of variance in y explained by x, ranges 0 to 1.
- **p-value on β₁**: tests H₀: β₁ = 0 (no linear relationship) vs H₁: β₁ ≠ 0.
- **Residuals**: should be randomly scattered around zero if the linear model is appropriate (see Topic 28).

## Assumptions (LINE)
- **L**inearity: the true relationship is linear.
- **I**ndependence: residuals are independent of each other.
- **N**ormality: residuals are approximately normally distributed.
- **E**qual variance (homoscedasticity): residual spread is constant across all values of x.

## Python Example
```python
import numpy as np
import statsmodels.api as sm

hours_studied = np.array([1,2,3,4,5,6,7,8])
exam_score = np.array([52,58,63,70,72,80,84,90])

X = sm.add_constant(hours_studied)
model = sm.OLS(exam_score, X).fit()
print(model.summary())
```

## Business Application
A SaaS company builds a simple linear regression of monthly recurring revenue (y) against number of active users (x) to quantify the average revenue impact of gaining new users, and to forecast revenue given user growth projections.

## Key Takeaways
- Simple linear regression quantifies both the direction/strength (slope) and predictive power (R²) of a relationship.
- Always check the LINE assumptions via residual plots before trusting the model's inferences.
- The slope coefficient has a real business interpretation: "for each additional unit of x, y changes by β₁ on average."
