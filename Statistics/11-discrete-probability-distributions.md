# 11. Discrete Probability Distributions (Binomial, Poisson)

## Overview
Discrete distributions model random variables that take countable values — critical for modeling events like conversions, defects, or arrivals.

## Binomial Distribution
Models the number of successes in n independent trials, each with success probability p.
- PMF: P(X=k) = C(n,k) pᵏ (1−p)ⁿ⁻ᵏ
- Mean: np | Variance: np(1−p)
- Use case: "Out of 100 emails sent, how many will be opened?" (fixed n, constant p, binary outcome)

## Poisson Distribution
Models the number of events occurring in a fixed interval of time/space, given a known average rate λ.
- PMF: P(X=k) = (λᵏ e^-λ) / k!
- Mean = Variance = λ
- Use case: "How many customer service calls arrive per hour?" (no fixed n, rare independent events)

## Binomial vs Poisson — When to Use Which
| Feature | Binomial | Poisson |
|---|---|---|
| Trials | Fixed n | No fixed upper limit |
| Parameter | n and p | λ (rate) |
| Example | Conversions out of 500 visitors | Website crashes per day |

## Python Example
```python
from scipy.stats import binom, poisson

# Binomial: 500 visitors, 4% conversion rate
p_at_least_30 = 1 - binom.cdf(29, n=500, p=0.04)
print("P(at least 30 conversions):", round(p_at_least_30, 4))

# Poisson: avg 3 support tickets per hour
p_exactly_5 = poisson.pmf(5, mu=3)
print("P(exactly 5 tickets in an hour):", round(p_exactly_5, 4))
```

## Business Application
A staffing manager uses the Poisson distribution (with λ = average calls/hour) to determine the probability of receiving more than 20 calls in an hour, directly informing how many agents to schedule to keep wait times acceptable.

## Key Takeaways
- Binomial fits fixed-trial, binary-outcome scenarios; Poisson fits rare-event, rate-based scenarios.
- Both distributions let you compute exact probabilities of business-relevant thresholds ("at least," "exactly," "no more than").
- Poisson is a natural model for operational planning: call volume, defects, website errors, arrivals.
