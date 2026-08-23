# 9. Probability Rules and Bayes' Theorem

## Overview
Bayes' Theorem lets us update our beliefs about an event as new evidence arrives — arguably the single most important formula for real-world decision-making under uncertainty.

## Bayes' Theorem
P(A | B) = [P(B | A) × P(A)] / P(B)

- **P(A)**: prior probability — belief before seeing evidence.
- **P(B | A)**: likelihood — probability of the evidence given A is true.
- **P(A | B)**: posterior probability — updated belief after seeing evidence B.
- **P(B)**: total probability of the evidence, across all scenarios.

## Worked Example: Fraud Detection
- 1% of transactions are fraudulent: P(Fraud) = 0.01
- The fraud model flags 95% of actual fraud: P(Flag | Fraud) = 0.95
- The model also flags 5% of legitimate transactions (false positive rate): P(Flag | No Fraud) = 0.05

P(Flag) = 0.95×0.01 + 0.05×0.99 = 0.059

P(Fraud | Flag) = (0.95 × 0.01) / 0.059 ≈ **16%**

Despite a "95% accurate" model, a flagged transaction is fraudulent only ~16% of the time — because fraud is rare. This is the classic base-rate fallacy Bayes' theorem corrects for.

## Python Example
```python
p_fraud = 0.01
p_flag_given_fraud = 0.95
p_flag_given_no_fraud = 0.05

p_flag = p_flag_given_fraud*p_fraud + p_flag_given_no_fraud*(1-p_fraud)
p_fraud_given_flag = (p_flag_given_fraud * p_fraud) / p_flag
print(round(p_fraud_given_flag, 3))
```

## Business Application
A marketing team updates its estimate of "will this lead convert?" as new data arrives (email opened, demo booked) — each event updates the posterior probability of conversion, allowing sales to prioritize the hottest leads dynamically rather than treating all leads equally.

## Key Takeaways
- Bayes' theorem formally combines prior belief with new evidence to produce an updated (posterior) probability.
- Ignoring base rates (how rare/common an event is) leads to badly miscalibrated conclusions — even with a highly "accurate" test.
- Bayesian thinking underlies spam filters, recommendation engines, medical testing, and fraud detection.
