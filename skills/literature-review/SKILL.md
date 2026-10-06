---
name: literature-review
description: Use when mapping prior research, verifying candidate papers, comparing methods, or preparing a literature matrix or Related Work outline.
---

# Literature Review

## Purpose

Build an evidence-traceable map of relevant research. This skill collects and compares source-backed facts; it does not establish novelty from a limited search or draft claims before sources are checked.

## When to Use

- A research question needs foundational, representative, or recent work mapped.
- A manuscript needs a verified Related Work outline.
- Candidate papers need comparison by contribution, method, assumptions, data, metrics, or limits.

## Inputs

Required: topic/question and scope (field, time span, methods, or task). Optional: seed papers, databases/search results, inclusion criteria, desired coverage, and a literature-matrix file. If scope is unclear, state a provisional scope and ask for the missing constraint.

## Workflow

1. Translate the question into search concepts, synonyms, inclusion/exclusion criteria, and source priorities. Identify likely primary-source venues or repositories.
2. Search only sources available to you. Record query, date, source, and selection reason; describe coverage limits.
3. Verify each selected paper's existence and metadata using an authoritative record. Prefer a published primary version when relevant; retain a preprint identifier when it is the canonical or only accessible version.
4. Inspect the source itself before extracting claims. Record contribution, problem, method, assumptions, datasets, metrics, baselines, strengths, limitations, and exact supporting locations.
5. Separate **verified source facts** from **your synthesis or interpretation**. Mark unavailable or conflicting details as unresolved.
6. Group papers by meaningful methodological or conceptual category; identify closest related work with explicit reasons and comparison dimensions.
7. Produce the structured matrix first. Draft a Related Work outline only from checked entries and preserve unresolved gaps as caveats.

## Output

Return (a) scope and search record, (b) a filled [literature matrix](../../templates/literature-matrix.md), (c) synthesis categories and closest-work comparison, and (d) coverage limitations and unresolved verification items. Each source row identifies a verified source and separates facts from interpretation.

## Validation

Check every included citation against its source; confirm extracted facts have a source location; compare related-work groupings to the matrix; ensure search limits and unresolved metadata are visible. Use [citation-policy](../../shared/citation-policy.md).

## Failure Modes

- Treating search-result snippets or citations-in-another-paper as source verification.
- Calling a work seminal, representative, or closest without a stated basis.
- Reporting “no prior work” when search coverage is incomplete.
- Mixing interpretation into a paper's reported facts or drafting Related Work before checking sources.

## Research Integrity Rules

Never invent papers, metadata, quotes, methods, datasets, or source support. Prefer primary sources. Distinguish published and preprint versions when they differ. Mark uncertain claims **unverified** and avoid novelty conclusions beyond the documented search scope. Follow [citation policy](../../shared/citation-policy.md) and [evidence policy](../../shared/evidence-policy.md).

## Interaction With Other Skills

Upstream: research question or scoped topic; citation-verifier can independently check records. Downstream: research-gap-finder uses the matrix; latex-paper-writer may outline Related Work only from verified entries; claim-evidence-checker audits resulting novelty claims.
