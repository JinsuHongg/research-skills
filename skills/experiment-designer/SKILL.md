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

1. Classify each experiment as **confirmatory** or **exploratory**. For confirmatory work, record the prespecified paper claim and hypothesis tested. For exploratory work, state the question or diagnostic objective; it need not test a paper claim.
2. Choose datasets and document provenance, inclusion, preprocessing, and why they match the research question or claim.
3. Define train/validation/calibration/final-evaluation roles where applicable, including which inputs and labels each stage can access. Keep final evaluation outcomes out of subsequent choices among methods, settings, or procedures. A fixed, prespecified transductive or test-time adaptation procedure may use evaluation inputs as part of the method; document its access and adaptation boundaries. For nested evaluation, confine selection to inner stages and do not feed outer results back into the procedure.
4. Select baselines and state why they are relevant. Define comparable implementation, tuning, data, and compute policies.
5. Set primary and guardrail metrics, aggregation, seeds/repetitions, stopping rules, and hyperparameter/model-selection policy before evaluation.
6. Plan ablations that isolate claimed components; add robustness or subgroup conditions only when tied to a claim or risk.
7. Specify effect-size and uncertainty reporting; choose tests and assumptions where appropriate, including multiplicity handling. Do not imply a test will be performed unless it is in the plan.
8. Record computational budget, hardware needs, failure logging, and analysis of negative or unexpected results.
9. For confirmatory work, state the expected evidence and a result that would weaken the claim. For exploratory work, state what evidence would refine or challenge the interpretation and what follow-up would test any resulting hypothesis. For both, record remaining confounders and claims the design cannot establish.

## Output

Return one [experiment-plan](../../templates/experiment-plan.md) entry per experiment. Confirmatory entries include a paper claim and hypothesis; exploratory entries include an exploratory objective and mark claim-specific fields not applicable when appropriate. Both document data/split policy, leakage risks, relevant baselines and metrics, analysis plan, compute budget, expected informative evidence, and failure analysis. State a falsification condition for confirmatory hypotheses; for exploration, state what follow-up would test a resulting hypothesis.

## Validation

Use [experiment checklist](../../shared/experiment-checklist.md). Check every confirmatory experiment maps to a claim and has adequate planned evidence. Check every exploratory experiment has a clear question or diagnostic purpose and is not presented as prespecified confirmation. For both types, verify final evaluation data are protected from subsequent choices, comparisons are fair, and analysis choices precede results where possible. For adaptation protocols, verify data access and estimand are explicit; mark unresolved validity concerns rather than treating disclosure alone as sufficient.

## Failure Modes

- Presenting exploratory analyses as prespecified confirmation or as independent validation of hypotheses generated from their results.
- Treating a result as an independent final evaluation after its outcomes influenced choices among models, settings, or procedures.
- Rejecting a nested evaluation or test-time adaptation design without checking its data-access assumptions and estimand.
- Giving baselines unequal tuning or compute without disclosure.
- Reporting only favorable seeds, metrics, or runs.

## Research Integrity Rules

Never invent dataset properties, baseline results, or statistical outcomes. Distinguish planned analyses from completed ones. Do not call a result significant before an appropriate test is run; do not treat results whose outcomes informed later choices among models, settings, or procedures as independent confirmation. A fixed, prespecified test-time adaptation procedure may use evaluation inputs when its access and estimand are documented. See [evidence policy](../../shared/evidence-policy.md) and [research principles](../../shared/research-principles.md).

## Interaction With Other Skills

Upstream: research-question-designer, plus dataset/method constraints. Downstream: result-analyzer consumes actual structured outputs; reproducibility-auditor checks reporting; publication-figure communicates measured results.
