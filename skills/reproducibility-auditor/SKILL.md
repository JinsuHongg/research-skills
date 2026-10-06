---
name: reproducibility-auditor
description: Use when assessing whether a paper or report provides enough detail to reproduce its methods, training, calibration, evaluation, and reported results.
---

# Reproducibility Auditor

## Purpose

Audit the information needed to reproduce a reported method and its results. The auditor records what is documented and what is missing; it does not infer undocumented settings from convention.

## When to Use

- Reviewing a manuscript, supplement, or artifact package for reproducibility.
- Preparing a reproducibility statement or author checklist.
- Identifying gaps that block implementation or result comparison.

## Inputs

Required: paper/report sections and available supplements or artifacts. Optional: code, configurations, checkpoints, dataset documentation, software environment, and reproduction target. State which materials were accessible.

## Workflow

1. Define the claimed reproduction scope: method, selected results, datasets, and evaluation conditions.
2. Inspect documentation for dataset/version, license/access, preprocessing, exclusions, and data splits.
3. Check model architecture, initialization, optimizer, learning rate, batch size, epochs, stopping, seeds, and nondeterminism.
4. Check hyperparameter search, model/checkpoint selection, calibration procedure, evaluation metrics, aggregation, and statistical reporting.
5. Check hardware, runtime, operating environment, software/library versions, code, configurations, checkpoints, and data availability.
6. For every item, record **complete**, **incomplete**, **ambiguous**, or **missing**, with a precise source location or an explicit “not reported.”
7. Summarize reproduction blockers and likely effect. Do not claim irreproducibility solely because code is unavailable if sufficient methods are described; distinguish access barriers from methodological omissions.

## Output

Return a [reproducibility report](../../templates/reproducibility-report.md) with scope, status per item, evidence location, missing detail, impact, major blockers, and unresolved questions.

## Validation

Check that every status has evidence or is explicitly not reported; compare numbers/settings across paper, supplement, and code when available; ensure ambiguous statements are not upgraded to complete. Use [reproducibility checklist](../../shared/reproducibility-checklist.md).

## Failure Modes

- Guessing common defaults for unreported hyperparameters or seeds.
- Treating code availability as equivalent to sufficient reproducibility detail.
- Overlooking differences between paper, supplement, and released artifacts.
- Calling an item complete when it lacks version, protocol, or selection information.

## Research Integrity Rules

Do not invent implementation settings, software versions, dataset properties, or results. Preserve conflicts between sources and identify what needs author clarification. Do not expose credentials, private data paths, or confidential material in public reports.

## Interaction With Other Skills

Upstream: paper-reviewer or submission-readiness may request an audit. Downstream: experiment-designer can use blockers to improve protocol reporting; latex-paper-writer can incorporate verified details; claim-evidence-checker checks reproducibility claims.
