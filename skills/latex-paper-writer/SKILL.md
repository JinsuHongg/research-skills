---
name: latex-paper-writer
description: Use when drafting, revising, or restructuring research manuscripts or sections written in LaTeX.
---

# LaTeX Paper Writer

## Purpose

Write clear academic prose in LaTeX from validated research artifacts while preserving technical meaning. This skill edits and structures evidence; it does not supply missing results, sources, or theoretical claims.

## When to Use

- Drafting or revising an abstract, introduction, related work, method, theory, experiments, results, discussion, limitations, conclusion, or appendix.
- Improving precision, flow, or concision while retaining LaTeX syntax and scientific meaning.
- Mapping validated artifacts into a manuscript section.

## Inputs

Required: target section, research materials/artifacts, and desired scope. Optional: LaTeX source, venue template, style constraints, citations, equations, and reviewer feedback. Identify missing evidence or metadata before drafting affected claims.

## Workflow

1. Inventory available validated artifacts and map each planned paragraph/claim to its source: literature matrix to Related Work; method specification to Method; experiment plan plus verified results to Experiments/Results; claim-evidence matrix to Abstract/Conclusion.
2. Identify unsupported inputs, contradictions, missing values, unresolved citations, or unverified venue requirements. Ask for or mark gaps; do not fill them by inference.
3. Draft the requested section in precise, direct language. State conditions and limitations alongside claims when needed.
4. Preserve commands, math, labels, citation keys, cross-references, and notation. Do not alter technical statements during copyediting without flagging the change.
5. Ensure each empirical statement corresponds to verified results and each literature statement to checked sources. Distinguish observed result from interpretation.
6. Review for scope, repetition, unsupported certainty, consistency, and LaTeX integrity; return an issue list for unresolved matters.

## Output

Provide revised LaTeX (or a clearly marked prose draft if source is absent), a concise change summary, and an **unresolved evidence / author input** list. Preserve all supplied factual content and mark every new claim that needs confirmation.

## Validation

Trace factual statements to source artifacts, verify numbers and citations verbatim against inputs, check braces/commands and references touched, and compare technical meaning before/after. Use [academic writing guidelines](../../shared/academic-writing-guidelines.md), [citation policy](../../shared/citation-policy.md), and [claim-evidence matrix](../../templates/claim-evidence-matrix.md).

## Failure Modes

- Writing a polished narrative around missing evidence as though it exists.
- Inventing numbers, references, theorem statements, data splits, implementation settings, or significance.
- Inflating novelty or certainty, adding filler, or deleting meaningful limitations.
- Breaking LaTeX syntax or silently changing notation or technical meaning.

## Research Integrity Rules

Paper writing consumes validated artifacts. Literature matrix supports Related Work; experiment plan plus verified results supports experiment/result prose; claim-evidence matrix supports abstract and conclusion. Never invent missing evidence. Preserve uncertainty and limitations and leave unsupported claims clearly marked.

## Interaction With Other Skills

Upstream: literature-review, experiment-designer, result-analyzer, and claim-evidence-checker. Downstream: citation-verifier, paper-consistency-checker, paper-reviewer, and submission-readiness audit the draft.
