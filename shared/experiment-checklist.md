# Experiment Checklist

For each experiment, record:

- [ ] Experiment type (**confirmatory** or **exploratory**). For confirmatory work: paper claim and testable hypothesis. For exploratory work: question or diagnostic objective; identify any post hoc hypotheses for follow-up.
- [ ] Dataset provenance, version, license/terms, preprocessing, and exclusions.
- [ ] Train/validation/calibration/final-evaluation roles, accessible inputs and labels, and leakage controls. Keep outer/final evaluation results out of subsequent selection; protocol disclosure alone does not restore independence after reuse.
- [ ] Baselines, rationale, implementation/version, and comparable tuning budget.
- [ ] Primary and guardrail metrics, aggregation, and direction of improvement.
- [ ] Ablations tied to specific method components or claims.
- [ ] Seeds, repetitions, stopping rules, and hyperparameter/model-selection policy.
- [ ] Statistical summaries planned: effect sizes, intervals, tests, assumptions, and multiplicity handling where appropriate.
- [ ] Robustness or subgroup analyses and their limits.
- [ ] Compute budget, hardware/software details, and failed-run handling.
- [ ] Confirmatory: planned falsification condition. Exploratory: question or diagnostic objective and, if a hypothesis emerges, follow-up that could test it. Record failure analysis for either type.
- [ ] Expected evidence and which conclusion would remain unsupported.

If evaluation outcomes influence training, tuning, calibration, model selection, or later choices among procedures, identify the affected results as development evidence and scope claims accordingly. A fixed, prespecified transductive or test-time adaptation procedure may use evaluation inputs as part of the evaluated method; document input and label access, adaptation boundaries, and the estimand. For nested evaluation, keep selection within inner stages and do not feed outer results back into choices. Disclosure alone does not establish an independent final estimate. See [evidence-policy.md](evidence-policy.md) for claim scope.
