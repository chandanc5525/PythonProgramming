# 26. Multiple Linear Regression

## Overview
Multiple linear regression extends simple regression to model an outcome using **several** predictors simultaneously, allowing you to isolate each predictor's effect while controlling for the others.

## The Model
y = β₀ + β₁x₁ + β₂x₂ + ... + βₖxₖ + ε

Each βᵢ represents the expected change in y for a one-unit increase in xᵢ, **holding all other predictors constant** — a much more realistic real-world statement than simple regression's single-variable claim.

## Key Concepts
- **Adjusted R²**: like R², but penalizes adding predictors that don't meaningfully improve the model — use this (not raw R²) when comparing models with different numbers of predictors.
- **Multicollinearity**: when predictors are highly correlated with each other, coefficient estimates become unstable and hard to interpret. Diagnose with **Variance Inflation Factor (VIF)**; VIF > 5–10 signals a problem.
- **Categorical predictors**: included via dummy/one-hot encoding (e.g., region as three 0/1 indicator variables for four regions).

## Model Selection
- **Forward selection**: start empty, add the most significant predictor at each step.
- **Backward elimination**: start with all predictors, remove the least significant iteratively.
- **Regularization (Ridge/Lasso)**: penalizes coefficient size to prevent overfitting, especially useful with many correlated predictors.

## Python Example
```python
import pandas as pd
import statsmodels.api as sm

df = pd.DataFrame({
    "ad_spend": [10,15,20,25,30,35,40,45],
    "price_discount": [0,5,5,10,10,15,15,20],
    "sales": [100,120,135,160,170,190,200,230]
})

X = sm.add_constant(df[["ad_spend", "price_discount"]])
model = sm.OLS(df["sales"], X).fit()
print(model.summary())
```

## Business Application
A pricing team builds a multiple regression of sales on ad spend, discount percentage, and seasonality indicators — allowing them to isolate the true incremental effect of discounting on sales *after* controlling for advertising and seasonal effects, rather than confusing the two.

## Key Takeaways
- Multiple regression isolates each predictor's independent effect, controlling for the others — critical for avoiding confounded conclusions.
- Watch for multicollinearity, which inflates standard errors and destabilizes coefficient interpretation.
- Use adjusted R² (not R²) to fairly compare models with different numbers of predictors.
