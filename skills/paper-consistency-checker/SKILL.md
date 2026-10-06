---
name: paper-consistency-checker
description: Use when checking a complete manuscript for conflicting terminology, notation, values, cross-references, or descriptions across sections and artifacts.
---

# Paper Consistency Checker

## Purpose

Find internal mismatches in a manuscript and report precise locations so authors can resolve them. This skill detects inconsistency; it does not decide which conflicting value is correct without evidence.

## When to Use

- Before submission or after substantial manuscript edits.
- When tables, text, code, appendices, and figures may have drifted apart.
- When reviewing terminology, notation, numbers, or cross-references globally.

## Inputs

Required: full manuscript source or a sufficiently complete rendered paper. Optional: supplementary files, source data, experiment configs, glossary, and known intended conventions. Record material not supplied.

## Workflow

1. Inventory sections and artifacts. Extract a reference list of notation, acronyms, method names, datasets, split sizes, metrics, hyperparameters, and cross-references.
2. Compare each item across abstract, main text, equations, algorithms, figures, tables, appendices, and supplements.
3. Check dataset counts and splits, metric definitions, table/text values, figure/text trends, method naming, and hyperparameter settings.
4. Check theorem/algorithm notation, equation and section references, citation keys, figure/table references, and acronym first use where inspectable.
5. Report each confirmed mismatch with both locations, conflicting forms, and likely impact. Separate a confirmed mismatch from an item requiring manual verification.
6. Do not resolve conflicts by choosing the most plausible value. Request an authoritative source such as the experiment record or author decision.

## Output

Return a prioritized issue list: ID, category, location A/value, location B/value, status (**confirmed mismatch**, **needs verification**, or **no issue found in checked scope**), impact, and resolution needed. State which files/sections were checked.

## Validation

Re-open cited locations; ensure each issue is reproducible and not a formatting difference; verify the report distinguishes conflicts from unverified checks. Recheck corrections across all affected references after authors resolve them.

## Failure Modes

- Silently editing one of two conflicting values.
- Reporting a suspected mismatch without both source locations.
- Comparing values with different units or definitions as though equivalent.
- Claiming the full paper is consistent when only selected sections were checked.

## Research Integrity Rules

Do not invent the intended notation, value, method name, or result. Preserve ambiguity and flag it for author resolution. Keep private paths, unpublished data, and credentials out of public issue reports.

## Interaction With Other Skills

Upstream: latex-paper-writer or a full manuscript package. Downstream: paper-reviewer and submission-readiness use findings; result-analyzer or reproducibility-auditor can identify authoritative source values.
