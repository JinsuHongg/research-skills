---
name: rebuttal
description: Use when analyzing peer-review feedback, planning author responses, or drafting a concise evidence-based rebuttal to reviewers.
---

# Rebuttal

## Purpose

Turn reviewer feedback into a prioritized, respectful response plan grounded in completed evidence and manuscript changes. This skill does not treat every criticism as a misunderstanding or promise future work as completed.

## When to Use

- Preparing a conference or journal rebuttal or response-to-reviewers letter.
- Clustering overlapping comments and deciding which changes or evidence to address.
- Checking whether proposed replies answer the reviewer's concern directly.

## Inputs

Required: reviewer comments and the current manuscript/revision context. Optional: venue response constraints, author decisions, completed experiments, and change locations. Treat confidential review material as private and retain it only in the user's authorized workspace.

## Workflow

1. Parse comments by reviewer and atomic issue. Preserve the reviewer's meaning; do not recast valid criticism as misunderstanding.
2. Cluster overlapping issues across reviewers while retaining each original ID and distinct concern.
3. For each issue, record severity, type (correctness, misunderstanding, evidence request, clarification, factual correction, presentation), validity assessment, evidence/location, requested action, and response priority.
4. Prioritize: (1) correctness concerns, (2) misunderstandings that materially affect evaluation, (3) requested evidence, (4) clarification, (5) minor presentation.
5. Decide what can be answered with existing evidence, what requires a completed analysis/experiment, what manuscript change is made, and what cannot be resolved within constraints.
6. Draft concise responses that answer the concern first, cite evidence or exact changes, acknowledge valid limits, and respectfully correct factual misunderstandings.
7. Cross-check every factual statement and promised change against the revised manuscript and actual completed work. Keep response constraints and unresolved concerns visible.

## Output

Return an issue map with reviewer, issue ID, cluster, severity, type, validity/misunderstanding assessment, requested evidence or clarification, priority, response, manuscript change/location, and unresolved action. Provide a draft response organized by reviewer/issue when requested.

## Validation

Check that all material comments are addressed or explicitly deferred; overlapping comments remain traceable; replies answer the specific point; evidence and change locations are accurate; and no promise exceeds completed work.

## Failure Modes

- Dismissing valid criticism as reviewer misunderstanding.
- Responding defensively or repeating manuscript text without addressing the issue.
- Promising experiments or analyses that are planned but unfinished.
- Losing a distinct concern while clustering similar comments.

## Research Integrity Rules

Never invent completed experiments, new results, citations, or manuscript changes. Clearly distinguish proposed future work from work completed for the response. Do not expose confidential reviews or identifying reviewer information in public examples or repository content.

## Interaction With Other Skills

Upstream: paper-reviewer, result-analyzer, claim-evidence-checker, and revised manuscript. Downstream: latex-paper-writer can implement verified wording changes; paper-consistency-checker and submission-readiness review the final revision.
