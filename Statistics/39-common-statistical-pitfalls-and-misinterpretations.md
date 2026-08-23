# 39. Common Statistical Pitfalls and Misinterpretations

## Overview
Even technically correct statistical analysis can lead to bad business decisions if the results are misinterpreted. This topic catalogs the most common and costly mistakes in applied statistics.

## The Pitfall Catalog
- **Confusing correlation with causation** (Topic 24): a relationship between two variables doesn't establish that one causes the other — confounders and reverse causation are always possible without a controlled experiment.
- **Misinterpreting p-values**: a p-value is not the probability that H₀ is true, and it's not the probability the result happened by chance — it's the probability of seeing data this extreme *if H₀ were true*.
- **Misinterpreting confidence intervals**: a 95% CI does not mean "95% probability the true value is in this interval" (Topic 16) — it's a statement about the long-run performance of the method.
- **Multiple comparisons / p-hacking**: testing many hypotheses (or many cuts of the same data) and reporting only the significant ones dramatically inflates the true false-positive rate.
- **Simpson's Paradox** (Topic 34): aggregate trends can reverse when data is disaggregated by a lurking subgroup variable.
- **Survivorship bias**: drawing conclusions only from units that "survived" a selection process, ignoring those that dropped out.
- **Regression to the mean**: extreme results (a best-ever or worst-ever sales month) tend to be followed by more average results naturally, even with no intervention — don't credit an intervention for what's actually a statistical artifact.
- **Base rate neglect**: ignoring how common/rare an event is when interpreting a positive test result (Topic 9's fraud example).
- **Overfitting**: a model that fits historical data extremely well but fails to generalize to new data, often from including too many predictors relative to the amount of data.

## A Practical Checklist Before Trusting a Result
1. Was this a controlled experiment, or observational data? (Affects causal claims.)
2. Was the hypothesis and metric decided *before* looking at the data?
3. Were multiple metrics/segments tested? If so, was that accounted for statistically?
4. Does the result hold up in subgroups, or only in aggregate?
5. Is the effect size practically meaningful, not just statistically significant?

## Business Application
A sales director notices their newly hired "star" reps' performance regresses toward the team average in their second quarter and mistakenly concludes onboarding quality is declining — when this is largely regression to the mean, since reps were selected for an exceptionally strong (partly lucky) first quarter.

## Key Takeaways
- Most costly statistical mistakes come from misinterpretation, not miscalculation — the numbers were right, but the conclusion drawn from them wasn't.
- Regression to the mean and survivorship bias are subtle enough that they routinely fool experienced analysts and executives alike.
- A short "trust checklist" before acting on a statistical finding catches most of these pitfalls.
