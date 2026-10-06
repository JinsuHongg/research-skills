---
name: claim-evidence-checker
description: Use when auditing whether a manuscript's claims, conclusions, or abstract statements are supported by its actual evidence.
---

# Claim-Evidence Checker

## Purpose

Make the support for material paper claims inspectable. The checker maps claims to required and actual evidence, identifies overreach, and suggests revisions; it does not invent evidence to repair a claim.

## When to Use

- Reviewing an abstract, introduction, results, discussion, or conclusion for claim strength.
- Checking “significant,” “state of the art,” “robust,” “generalizable,” or causal statements.
- Preparing a claim-evidence matrix before review or submission.

## Inputs

Required: manuscript text and the relevant data, analysis, theory, or literature sources. Optional: figures/tables, experiment plan, analysis reports, and claim scope. If evidence artifacts are unavailable, mark support unverifiable.

## Workflow

1. Extract each material empirical, theoretical, comparative, causal, novelty, robustness, or generalization claim. Assign a stable claim ID and source location.
2. Define the evidence that would be required for that claim type and scope.
3. Locate actual evidence in the manuscript, data, analysis, proof, or verified sources; cite exact section/table/figure/equation/artifact.
4. Compare scope and strength: conditions, baselines, metrics, domains, sample size, tests, assumptions, and limitations.
5. Assign one status: **supported**, **partially supported**, **unsupported**, **overstated**, or **unverifiable**. Add severity based on impact on the paper's conclusions.
6. Recommend a specific evidence request or narrower wording. Do not assume planned experiments have been completed.
7. Review the matrix for claims omitted from abstract/conclusion and for evidence reused beyond its scope.

## Output

Return a [claim-evidence matrix](../../templates/claim-evidence-matrix.md) with claim text/type, required and actual evidence, location, status, severity, and suggested revision. Summarize the most consequential unsupported or overstated claims.

## Validation

Check every status against cited evidence; verify locations; confirm “supported” does not rely only on author interpretation; and confirm suggested wording does not retain the same overclaim. Apply [evidence policy](../../shared/evidence-policy.md).

## Failure Modes

- Accepting “statistically significant” without an appropriate performed test.
- Accepting “state of the art” from a narrow or unfair comparison.
- Calling a method robust from one condition or generalizable from one domain.
- Inferring causation from correlation or treating absence of evidence as proof of no effect.

## Research Integrity Rules

Do not fabricate tests, citations, results, or source locations. Novelty requires verified literature coverage; broad robustness/generalization requires evidence across relevant conditions; causal language requires an identifying design. If evidence is missing, say so and lower or withhold the claim.

## Interaction With Other Skills

Upstream: result-analyzer, literature-review, citation-verifier, and manuscript artifacts. Downstream: latex-paper-writer revises claims from the matrix; submission-readiness and paper-reviewer use it for final evaluation.
