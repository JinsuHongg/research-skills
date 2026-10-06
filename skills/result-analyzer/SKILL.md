---
name: result-analyzer
description: Use when interpreting structured experiment outputs, comparing findings across runs, or preparing evidence-bounded results for a paper.
---

# Result Analyzer

## Purpose

Analyze supplied experiment results without upgrading observations into unsupported conclusions. It identifies effects, variability, failures, trade-offs, and uncertainty from the data provided.

## When to Use

- Results from a documented protocol need synthesis.
- Runs, seeds, subgroups, or robustness conditions need comparison.
- Authors need to distinguish observed outcomes from interpretation and publishable claims.

## Inputs

Required: structured results and enough protocol context to identify metrics, baselines, splits, runs, and intended claims. Optional: raw data, analysis scripts, uncertainty estimates, significance tests, and known deviations. Mark missing context.

## Workflow

1. Check data shape, metric definitions, run counts, missing values, protocol deviations, and whether metrics align with the planned analysis.
2. Report primary observations, including direction and magnitude. Compute summaries only from supplied/reproducible data; state aggregation and sample size.
3. Report effect sizes and mean/standard deviation or confidence intervals only when calculable and appropriate; name their method and unit.
4. Compare variation across seeds and conditions; surface failed runs, failure cases, unexpected findings, and trade-offs.
5. Describe statistical tests only when actually performed and supplied or reproducibly run. State test, assumptions, multiplicity handling, and limits.
6. Separate **observations**, **interpretations**, **claims justified by evidence**, and **claims still unsupported**.
7. Identify plausible confounders and analyses needed to resolve them. Do not convert an explanation into a result.

## Output

Use four explicit sections: **Observations**, **Interpretations**, **Justified claims**, and **Unsupported or unresolved claims**. Include protocol/data caveats, failed runs, uncertainty, and source locations as applicable.

## Validation

Reconcile summaries with supplied tables or raw outputs; verify denominators and run counts; ensure failed runs are represented; confirm language does not exceed evidence. Use [evidence policy](../../shared/evidence-policy.md) and [claim-evidence matrix](../../templates/claim-evidence-matrix.md).

## Failure Modes

- Calling an improvement “statistically significant” without a performed appropriate test.
- Hiding failed runs, seed variation, or unfavorable conditions.
- Treating a metric difference as causal or generalizable beyond the tested conditions.
- Reporting unsupported intervals, effect sizes, or fabricated result values.

## Research Integrity Rules

Never fabricate, silently repair, or selectively omit results. If a significance test was not performed, do not use “statistically significant.” Distinguish missing data from zero and planned analyses from completed analyses. Mark unsupported claims rather than writing around missing evidence.

## Interaction With Other Skills

Upstream: experiment-designer and structured, verified outputs. Downstream: publication-figure visualizes results; latex-paper-writer uses validated findings; claim-evidence-checker tests claim strength.
