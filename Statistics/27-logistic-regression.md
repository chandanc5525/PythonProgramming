# 27. Logistic Regression for Classification

## Overview
When the outcome is binary (yes/no, churn/stay, convert/don't convert) rather than continuous, logistic regression — not linear regression — is the appropriate statistical model.

## The Model
Logistic regression models the **log-odds** of the outcome as a linear function of predictors:
log[p / (1−p)] = β₀ + β₁x₁ + ... + βₖxₖ

The predicted probability p is recovered via the sigmoid function, always bounded between 0 and 1 — unlike linear regression, which could predict impossible values like a "probability" of 1.4.

## Interpreting Coefficients: Odds Ratios
Exponentiating a coefficient, e^β, gives the **odds ratio** — how the odds of the outcome multiply for a one-unit increase in that predictor, holding others constant. An odds ratio of 1.5 means the odds increase by 50%.

## Evaluating a Logistic Regression Model
- **Confusion matrix**: true/false positives and negatives at a chosen probability threshold.
- **Accuracy, precision, recall, F1-score**: derived from the confusion matrix.
- **ROC curve and AUC**: measures how well the model discriminates between classes across all thresholds; AUC of 0.5 = no better than random, 1.0 = perfect.

## Python Example
```python
import pandas as pd
import statsmodels.api as sm

df = pd.DataFrame({
    "tenure_months": [1,3,6,12,18,24,30,36,42,48],
    "monthly_charge": [70,65,60,55,50,45,40,38,35,30],
    "churned": [1,1,1,0,0,0,0,0,0,0]
})

X = sm.add_constant(df[["tenure_months", "monthly_charge"]])
model = sm.Logit(df["churned"], X).fit(disp=0)
print(model.summary())
```

## Business Application
A telecom company builds a logistic regression predicting customer churn probability from tenure, monthly charges, and support ticket count — using the resulting probability scores to proactively target retention offers at the highest-risk customers rather than blanket-targeting everyone.

## Key Takeaways
- Logistic regression is the standard statistical model for binary classification problems, producing interpretable probability estimates.
- Coefficients are interpreted through odds ratios, not raw unit changes as in linear regression.
- AUC and the confusion matrix (not R²) are the right tools for evaluating classification model performance.
