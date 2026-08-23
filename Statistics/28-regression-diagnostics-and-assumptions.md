# 28. Regression Diagnostics and Assumptions

## Overview
A regression model's coefficients and p-values are only trustworthy if its underlying assumptions hold. Diagnostics are the essential quality-control step between fitting a model and acting on its conclusions.

## Key Diagnostic Checks
### 1. Linearity
Plot residuals vs fitted values — should show no clear pattern (random scatter around zero). A curved pattern suggests a non-linear relationship was forced into a linear model.

### 2. Homoscedasticity (equal variance)
Residual spread should be constant across all fitted values. A "funnel" or "fan" shape in the residual plot indicates **heteroscedasticity**, which biases standard errors (and thus p-values/confidence intervals).

### 3. Normality of Residuals
Check with a Q-Q plot or Shapiro-Wilk test. Important mainly for small samples — CLT makes this less critical at large n.

### 4. Independence of Residuals
Especially relevant for time-series data — check with the Durbin-Watson statistic; autocorrelated residuals violate the independence assumption.

### 5. No Severe Multicollinearity
Check VIF (Variance Inflation Factor) for each predictor in multiple regression (see Topic 26).

### 6. Influential Points and Outliers
Use **Cook's distance** to identify observations that disproportionately affect the fitted model — worth investigating (data errors? genuinely unusual cases?) rather than blindly dropping.

## Python Example
```python
import statsmodels.api as sm
import statsmodels.stats.api as sms

X = sm.add_constant(df[["ad_spend"]])
model = sm.OLS(df["sales"], X).fit()

# Breusch-Pagan test for heteroscedasticity
bp_test = sms.het_breuschpagan(model.resid, model.model.exog)
print("Breusch-Pagan p-value:", bp_test[1])  # low p-value flags heteroscedasticity
```

## Business Application
Before presenting a pricing-elasticity regression to leadership, an analyst checks residual plots and finds heteroscedasticity — variance in residuals grows with sales volume — and applies a log transformation to sales, producing standard errors (and business conclusions) that can actually be trusted.

## Key Takeaways
- Diagnostics aren't optional — a model that violates its own assumptions can produce misleading coefficients, p-values, and confidence intervals.
- Residual plots are the single most useful diagnostic tool, revealing linearity, homoscedasticity, and outlier issues at a glance.
- Fixing violated assumptions (via transformation, robust standard errors, or different model choice) should happen before any business conclusion is drawn.
