---
name: publication-figure
description: Use when choosing, designing, revising, or auditing quantitative figures for a research manuscript or supplement.
---

# Publication Figure

## Purpose

Select and specify figures that communicate a scientific claim accurately and readably. The skill guides plot choice and presentation; it does not alter data or infer unavailable uncertainty.

## When to Use

- Choosing among line, bar, scatter, distribution, calibration/reliability, ablation, or efficiency plots.
- Preparing confidence intervals/error bars and accessibility choices.
- Reviewing figure scale, normalization, labels, layout, or vector-output suitability.

## Inputs

Required: scientific claim, variables, and data or table to visualize. Optional: audience, single/double-column target, page constraints, output format, uncertainty estimates, color requirements, and related figures. If uncertainty data are absent, report that.

## Workflow

1. Identify the message the figure must support and the comparison or distribution that carries it.
2. Inspect variable types, units, sample sizes, aggregation, uncertainty availability, and data quality.
3. Choose the plot form that communicates the claim: trends, comparisons, relationships, distributions, calibration, ablations, or performance-efficiency trade-offs.
4. Specify honest scales, axis limits, normalization, baselines, and uncertainty encoding. Explain choices that could change interpretation.
5. Check legibility at intended column width: labels, font size, line/marker contrast, legend placement, and annotation density.
6. Use color-blind-accessible encodings and check grayscale distinction; do not rely on color alone.
7. Prefer vector output when supported and suitable; state dimensions, font embedding/format, and raster needs where relevant.
8. Reconcile the figure with underlying values and paper claims. State limitations and any data not shown.

## Output

Return the figure's intended claim, recommended chart type, mapping of variables/series, scale and uncertainty decisions, layout/accessibility specifications, export guidance, and validation checks. If generating a figure, provide the artifact and source data/code when available.

## Validation

Verify plotted values against the source table/data; check units, axis range, denominators, uncertainty definitions, legend, readability at publication scale, and paper-text consistency. Flag misleading truncation or normalization.

## Failure Modes

- Choosing a plot type for visual appeal rather than the scientific question.
- Hiding variation, using unsupported error bars, or distorting axes.
- Overloading colors, relying only on color, or using unreadable labels.
- Normalizing away a relevant difference or omitting unfavorable conditions.

## Research Integrity Rules

Do not modify data, suppress observations, or imply uncertainty estimates not supplied or calculated from valid data. Explain axis breaks, truncation, transformations, exclusions, and normalization. Keep the plotted scope aligned with evidence; see [evidence policy](../../shared/evidence-policy.md).

## Interaction With Other Skills

Upstream: result-analyzer and verified structured results. Downstream: latex-paper-writer and paper-consistency-checker can check figure references and reported values; submission-readiness checks figure legibility and venue-specific current rules.
