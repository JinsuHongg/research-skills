---
name: experiment-designer
description: Use when planning research experiments, evaluations, baselines, ablations, data splits, or statistical reporting for paper claims.
---

# Experiment Designer

## Purpose

Design a fair, reproducible experiment plan that directly tests stated research claims. The skill plans evidence collection; it does not report expected outcomes as results.

## When to Use

- A hypothesis needs an empirical protocol.
- A paper's experiment set needs alignment, leakage, fairness, or coverage review.
- Baselines, metrics, ablations, or statistical reporting need to be specified before results are observed.

## Inputs

Required: paper claim or research question. Optional: dataset candidates, method, compute budget, metrics, constraints, and existing protocols. Ask for missing choices that alter validity; label provisional assumptions.

## Workflow

1. Convert each claim into an experiment question and record which paper claim the experiment tests. Remove experiments that support no stated claim unless marked exploratory.
2. Choose datasets and document provenance, inclusion, preprocessing, and why they match the claim.
3. Define train/validation/calibration/test roles where applicable. Specify leakage controls and prohibit test-set tuning or selection.
4. Select baselines and state why they are relevant. Define comparable implementation, tuning, data, and compute policies.
5. Set primary and guardrail metrics, aggregation, seeds/repetitions, stopping rules, and hyperparameter/model-selection policy before evaluation.
6. Plan ablations that isolate claimed components; add robustness or subgroup conditions only when tied to a claim or risk.
7. Specify effect-size and uncertainty reporting; choose tests and assumptions where appropriate, including multiplicity handling. Do not imply a test will be performed unless it is in the plan.
8. Record computational budget, hardware needs, failure logging, and analysis of negative or unexpected results.
9. State expected evidence, a result that would weaken the claim, remaining confounders, and any claim this design cannot establish.

## Output

Return one [experiment-plan](../../templates/experiment-plan.md) entry per experiment. Every entry includes a claim, hypothesis, data/split policy, leakage risks, baselines, metrics, analysis plan, compute budget, expected evidence, falsification condition, and failure analysis.

## Validation

Use [experiment checklist](../../shared/experiment-checklist.md). Check every experiment maps to a claim, every claim has adequate planned evidence, the test set is protected, comparisons are fair, and all analysis choices precede results where possible.

## Failure Modes

- Adding experiments without a claim-level purpose.
- Reusing test data for model selection, tuning, or calibration without an explicit justified protocol.
- Giving baselines unequal tuning or compute without disclosure.
- Reporting only favorable seeds, metrics, or runs.

## Research Integrity Rules

Never invent dataset properties, baseline results, or statistical outcomes. Distinguish planned analyses from completed ones. Do not call a result significant before an appropriate test is run; do not treat repeated test-set use as independent confirmation. See [evidence policy](../../shared/evidence-policy.md).

## Interaction With Other Skills

Upstream: research-question-designer, plus dataset/method constraints. Downstream: result-analyzer consumes actual structured outputs; reproducibility-auditor checks reporting; publication-figure communicates measured results.
