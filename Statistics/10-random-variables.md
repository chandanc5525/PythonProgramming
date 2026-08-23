# 10. Random Variables

## Overview
A random variable maps outcomes of a random process to numbers, allowing us to apply mathematical and statistical tools to uncertain events.

## Types
- **Discrete random variable**: takes on a countable set of values (number of support tickets per day: 0, 1, 2, ...).
- **Continuous random variable**: takes on any value in a range (time until next customer arrival: 2.37 minutes).

## Describing a Random Variable
- **Probability Mass Function (PMF)** — for discrete variables: P(X = x) for each possible value x.
- **Probability Density Function (PDF)** — for continuous variables: describes relative likelihood; probability is area under the curve over an interval.
- **Cumulative Distribution Function (CDF)**: P(X ≤ x), works for both discrete and continuous variables.

## Expected Value and Variance
- **Expected value (mean)**: E[X] = Σ x·P(X=x) (discrete) — the long-run average outcome.
- **Variance**: Var(X) = E[(X − E[X])²] — spread of the random variable.

## Worked Example
A support ticket resolution can be "resolved same day" (value 1, P=0.7) or "not resolved same day" (value 0, P=0.3).
E[X] = 1(0.7) + 0(0.3) = 0.7 → on average, 70% of tickets resolve same day.

## Python Example
```python
import numpy as np

# simulate a discrete random variable: number of daily sign-ups
outcomes = np.arange(0, 10)
probs = [0.05,0.10,0.15,0.20,0.20,0.15,0.08,0.04,0.02,0.01]
expected_signups = np.sum(outcomes * probs)
print("Expected daily sign-ups:", expected_signups)
```

## Business Application
A call center models "number of calls per hour" as a random variable to plan staffing — computing the expected value and variance lets them staff for the average load while keeping enough buffer capacity for high-variance hours.

## Key Takeaways
- Random variables translate uncertain real-world outcomes into numbers we can analyze mathematically.
- Expected value gives the long-run average; variance gives the spread/risk around that average.
- Nearly every probability distribution used in analytics (binomial, normal, Poisson) is a model for some random variable.
