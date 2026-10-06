---
name: submission-readiness
description: Use when performing a final internal audit of a research manuscript and its materials before submission or resubmission.
---

# Submission Readiness

## Purpose

Create a decision-ready internal audit of a manuscript, evidence package, and current submission requirements. It identifies blockers and unverified items; it does not guarantee acceptance or venue compliance.

## When to Use

- Preparing an internal go/no-go review before submission.
- Checking revisions, supplements, anonymization, or venue requirements.
- Consolidating findings from technical and reproducibility audits.

## Inputs

Required: manuscript and intended venue/track if venue compliance is requested. Optional: supplement, code/data statements, checklists, reviews, current official call/instructions, and submission metadata. If venue or track is unknown, venue-specific items remain **NOT CHECKED**.

## Workflow

1. Establish scope: manuscript version, materials checked, venue/track, and date of official-source verification.
2. Audit novelty, technical correctness, assumptions, claim-evidence alignment, baselines, ablations, statistics, and limitations.
3. Audit reproducibility, figures/tables, citation metadata and support, internal consistency, anonymization, and supplementary material.
4. For venue compliance, inspect current official call for papers, formatting rules, page limits, anonymity policy, supplementary-material rules, required declarations, and official LaTeX template. Record links and checked date; do not rely on memory or third-party summaries as authority.
5. Assign each item **PASS**, **WARNING**, **FAIL**, or **NOT CHECKED** with evidence/location, impact, and action. Use NOT CHECKED when required source/material is unavailable.
6. Prioritize blockers, warnings, and remaining decisions. Revisit status after corrections; do not upgrade status without checking.

## Output

Return a [submission checklist](../../templates/submission-checklist.md), summary of blockers and warnings, materials checked, official sources and verification date, and unresolved items. State clearly that this is an internal readiness audit, not a guarantee of compliance or acceptance.

## Validation

Confirm every PASS has evidence, every venue PASS cites a current official source, and unknowns are NOT CHECKED. Confirm FAIL/WARNING actions are concrete and do not conceal unresolved research-integrity issues.

## Failure Modes

- Treating remembered page limits or prior-year rules as current.
- Claiming venue compliance without checking official instructions.
- Marking unavailable evidence or supplements PASS.
- Conflating publication readiness with acceptance probability.

## Research Integrity Rules

Never fabricate results, citations, checklist completion, or venue policy. Preserve failed and unresolved scientific checks; anonymization must not remove evidence needed to assess the work. Keep confidential reviewer material private.

## Interaction With Other Skills

Upstream: paper-reviewer, claim-evidence-checker, citation-verifier, reproducibility-auditor, paper-consistency-checker, and author-supplied submission materials. Downstream: authors resolve findings and rerun this audit against the corrected manuscript.
