# 8. Probability Fundamentals

## Overview
Probability is the mathematical language of uncertainty. It underlies every inferential statistical method, from confidence intervals to A/B testing to machine learning.

## Core Concepts
- **Experiment**: a process with an uncertain outcome (a customer visits a website).
- **Sample space (S)**: the set of all possible outcomes.
- **Event**: a subset of the sample space (customer makes a purchase).
- **Probability P(E)**: a number between 0 and 1 representing the likelihood of event E, where P(S) = 1.

## Basic Rules
- **Complement**: P(not E) = 1 − P(E)
- **Addition rule (mutually exclusive)**: P(A or B) = P(A) + P(B)
- **Addition rule (general)**: P(A or B) = P(A) + P(B) − P(A and B)
- **Multiplication rule (independent events)**: P(A and B) = P(A) × P(B)
- **Conditional probability**: P(A | B) = P(A and B) / P(B)

## Independence vs Dependence
Two events are **independent** if the occurrence of one doesn't affect the probability of the other (two separate coin flips). They're **dependent** if it does (drawing cards without replacement).

## Python Example
```python
import numpy as np

np.random.seed(0)
purchases = np.random.choice(["buy", "no_buy"], size=10000, p=[0.15, 0.85])
p_buy = np.mean(purchases == "buy")
print("Empirical P(buy):", p_buy)  # converges toward 0.15 as n grows (Law of Large Numbers)
```

## Business Application
An e-commerce team models the probability that a visitor both views a product page (P=0.4) and completes checkout given they viewed it (P=0.1) to estimate overall conversion probability: P(view) × P(checkout | view) = 0.04, informing revenue forecasts.

## Key Takeaways
- Probability quantifies uncertainty on a 0-to-1 scale and underlies all inferential statistics.
- Conditional probability — P(A | B) — is essential for realistic business modeling, since events are rarely independent.
- The Law of Large Numbers explains why larger samples give more reliable probability estimates.
