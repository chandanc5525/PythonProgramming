# 35. Data-Driven Decision Making Framework

## Overview
Statistical analysis only creates business value when it's embedded in a disciplined decision-making process — turning numbers into action, not just reports.

## A Practical Framework
1. **Frame the decision, not just the analysis**: start with "what decision will this inform?" not "what can I analyze?" — this determines what data and precision actually matter.
2. **Define the metric and the decision threshold in advance**: e.g., "we'll roll this out if conversion lift ≥ 2% with 95% confidence" — set *before* seeing results, to avoid post-hoc rationalization.
3. **Choose the right method for the question**: descriptive stats for "what happened," hypothesis testing/regression for "why," A/B testing for "what should we do."
4. **Account for uncertainty explicitly**: present confidence intervals or ranges, not single point estimates, when communicating to decision-makers.
5. **Separate statistical significance from practical significance**: a statistically significant 0.1% improvement may not be worth implementation cost — weigh effect size against business impact.
6. **Decide, document, and monitor**: make the call, record the reasoning and evidence, then track outcomes against the prediction to calibrate future decisions.

## The Cost of Skipping Steps
- Skipping step 1 → "analysis paralysis," generating interesting but irrelevant insights.
- Skipping step 2 → moving the goalposts after seeing results (HARKing — Hypothesizing After Results are Known).
- Skipping step 4 → overconfidence in noisy point estimates, leading to reactive whiplash decisions.

## A Simple Decision Matrix
| Effect Size | Statistically Significant | Recommended Action |
|---|---|---|
| Large | Yes | Act with confidence |
| Large | No (likely underpowered) | Collect more data before deciding |
| Small | Yes | Weigh against implementation cost |
| Small | No | Likely no meaningful effect; deprioritize |

## Business Application
Before testing a new pricing model, a pricing team writes down in advance: "we'll adopt the new price only if revenue per user increases by at least 5% with p < 0.05" — this pre-commitment prevents them from rationalizing a marginal, statistically fragile result into a full rollout after the fact.

## Key Takeaways
- Good data-driven decisions start by framing the decision, then working backward to the right analysis — not the reverse.
- Pre-committing to decision thresholds prevents motivated reasoning after results are in.
- Statistical significance is necessary but not sufficient — practical significance and implementation cost complete the picture.
