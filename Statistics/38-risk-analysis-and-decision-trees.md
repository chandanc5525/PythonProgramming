# 38. Risk Analysis and Decision Trees

## Overview
Business decisions often involve explicit trade-offs between uncertain outcomes. Statistical decision theory — including decision trees and expected value analysis — provides a structured way to choose among risky alternatives.

## Expected Value (EV) Decision Rule
EV = Σ (probability of outcome × value of outcome)

Comparing the expected value of different choices provides a rational, quantifiable basis for decisions under uncertainty — though it should be balanced against risk tolerance (see below).

## Decision Trees
A decision tree maps out sequential decisions and uncertain events as branches, with probabilities and payoffs at each outcome node, allowing the EV of complex, multi-stage decisions to be calculated by "folding back" from the end.

```
Launch Product? 
├── Yes → Market succeeds (P=0.6) → Profit: $2M
│         Market fails (P=0.4) → Loss: $500K
│         EV = 0.6(2M) + 0.4(-0.5M) = $1.0M
└── No → EV = $0
Decision: Launch (higher EV)
```

## Risk Tolerance Beyond Expected Value
Expected value treats a 50% chance of $1M the same as a certain $500K — but many businesses are risk-averse and would prefer the certain outcome. Concepts like **utility functions** and **Value at Risk (VaR)** incorporate risk tolerance beyond raw expected value.

## Sensitivity Analysis
Since probabilities and payoffs in a decision tree are estimates, sensitivity analysis tests how much the recommended decision would change if key assumptions (e.g., success probability) were off by a reasonable margin — protecting against false confidence in uncertain inputs.

## Python Example
```python
scenarios = {
    "launch": [(0.6, 2_000_000), (0.4, -500_000)],
    "no_launch": [(1.0, 0)]
}

for decision, outcomes in scenarios.items():
    ev = sum(p*v for p, v in outcomes)
    print(f"{decision}: EV = ${ev:,.0f}")
```

## Business Application
A pharmaceutical company uses a decision tree to evaluate whether to continue investing in a drug through each clinical trial phase, incorporating the probability of success at each stage and the cost/payoff of each path, to make a statistically grounded go/no-go decision at every stage gate.

## Key Takeaways
- Expected value gives a rational baseline for comparing risky alternatives, but should be weighed against actual risk tolerance.
- Decision trees make multi-stage uncertain decisions tractable by breaking them into sequential probability-weighted branches.
- Sensitivity analysis protects decisions from being overly reliant on single-point probability/payoff estimates.
