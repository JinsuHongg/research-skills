---
name: paper-reviewer
description: Use when assessing a research manuscript for conference, journal, methodological, statistical, reproducibility, or internal review.
---

# Paper Reviewer

## Purpose

Produce a fair, evidence-based assessment of a manuscript's contribution, methods, evidence, and clarity. Review the work presented; do not substitute personal methodological preference for a correctness or significance concern.

## When to Use

- Preparing an internal critique or structured conference/journal review.
- Evaluating methods, statistics, reproducibility, or a manuscript under adversarial scrutiny.
- Prioritizing issues before submission or revision.

## Inputs

Required: manuscript or specified sections. Optional: review mode, venue criteria, review rubric, supplemental materials, and limits on review scope. If materials are incomplete, identify what was and was not reviewed.

## Workflow

1. Confirm the review mode and scope. If a venue rubric is supplied, use its current official version and keep general scientific assessment distinct from venue-specific criteria.
2. Summarize the question, claimed contribution, method, and main evidence neutrally before judging.
3. Assess problem importance, novelty, technical correctness, assumptions, methodology, experiment design, baseline fairness, statistical validity, reproducibility, clarity, limitations, and evidence strength as applicable.
4. For every issue, record the manuscript location, observed evidence, why it matters, and a concrete clarification or remedy. Distinguish a flaw from missing information, uncertainty, and preference.
5. Classify findings as **fatal**, **major**, **minor**, or **optional**. State confidence and what evidence could change the assessment.
6. Summarize strengths, decision-relevant concerns, and actionable priorities using the structure in [paper-review template](../../templates/paper-review.md).

## Output

Return review mode and scope, neutral contribution summary, confidence, strengths, categorized issues with evidence locations and impact, limitations/questions, and prioritized requests. Flag unreviewed material explicitly.

## Validation

Check that every factual criticism points to manuscript evidence; categories reflect impact rather than tone; preferences are labeled; and proposed requests can address a stated issue. Apply [review rubric](../../shared/review-rubric.md) and [evidence policy](../../shared/evidence-policy.md).

## Failure Modes

- Recommending rejection because the method differs from the reviewer's preferred approach.
- Treating absent detail as proof of incorrectness without identifying the uncertainty.
- Repeating the paper summary instead of evaluating evidence.
- Giving generic requests, unsupported novelty judgments, or conflicting severity labels.

## Research Integrity Rules

Do not invent experiments, results, citations, or manuscript content. Do not claim a statistical flaw without identifying the analysis and reason. Keep confidential reviewer material private and out of public examples or this repository. Separate verified defects from questions and preferences.

## Interaction With Other Skills

Use reproducibility-auditor, claim-evidence-checker, citation-verifier, or paper-consistency-checker for focused audits. The review may produce a paper-review artifact for authors or feed rebuttal prioritization; do not convert reviewer criticism into a promise of work not completed.
