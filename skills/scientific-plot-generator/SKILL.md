---
name: scientific-plot-generator
description: Use when generating reproducible, data-backed scientific plots and Python plotting scripts from supplied or measured values, usually with matplotlib.
---

# Scientific Plot Generator

## Purpose

Create quantitative figure files and reproducible Python scripts from actual research data. Use `matplotlib` by default. For plot selection, visual specification, or figure review without generating files, use the `publication-figure` skill. For evidence and uncertainty rules, follow the [evidence policy](../../shared/evidence-policy.md).

## Inputs

Required: numeric data (provided values or an accessible file) and the scientific question or comparison. Identify missing inputs before plotting; never fill them with guesses. Optional: preferred plot type, audience, dimensions, output format, uncertainty estimates, and output location.

## Workflow

1. Inspect the data structure, variable types, units, groups, missing values, duplicates, and plausible ranges. Distinguish unavailable observations from zero or other valid values.
2. Select a chart that fits the question and data structure. Preserve the observations and disclose exclusions, aggregation, filtering, normalization, smoothing, or other transformations.
3. Show uncertainty only when supplied or validly computed from the available data. Do not imply statistical significance without an appropriate test and evidence.
4. Generate the plot with Python and `matplotlib`; use `pandas`, `numpy`, or `scipy` only when useful. Keep code tied to the supplied data source and make paths and required dependencies clear so the output can be regenerated.
5. Use readable labels with units, accessible color and marker choices, uncluttered legends, and scales that do not exaggerate differences. Prefer PDF or SVG for paper figures; use suitable-resolution PNG when requested. Keep titles, captions, and figure numbers outside the image unless explicitly requested.
6. Save the requested figure and its plotting script when requested or useful. Report the input source, plot type, transformations, uncertainty treatment, outputs, and limitations briefly.

## Validation

- Confirm plotted values and any aggregation against the input; check that missing and failed observations are not silently dropped or imputed.
- Check labels, units, axis ranges, uncertainty definitions, legend, readability at intended size, and that annotations do not make unsupported claims.
- Run the script when possible and inspect the rendered output for clipping, overlap, and unreadable text. State if execution or visual inspection was not possible.

## Failure Modes

- Inventing values, summary statistics, uncertainty, or significance.
- Hiding failed runs or exclusions without disclosure.
- Using misleading axis limits, transformations, or styling to magnify effects.
- Returning a figure that cannot be traced to its input data or regenerated from its script.
- Generating a quantitative result plot without data. If a mockup is explicitly requested, label all mock values clearly as synthetic and do not present it as a result.
