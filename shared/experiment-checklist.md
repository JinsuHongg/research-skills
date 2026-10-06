# Experiment Checklist

For each experiment, record:

- [ ] Paper claim and testable hypothesis.
- [ ] Dataset provenance, version, license/terms, preprocessing, and exclusions.
- [ ] Train/validation/calibration/test split policy and leakage controls.
- [ ] Baselines, rationale, implementation/version, and comparable tuning budget.
- [ ] Primary and guardrail metrics, aggregation, and direction of improvement.
- [ ] Ablations tied to specific method components or claims.
- [ ] Seeds, repetitions, stopping rules, and hyperparameter/model-selection policy.
- [ ] Statistical summaries planned: effect sizes, intervals, tests, assumptions, and multiplicity handling where appropriate.
- [ ] Robustness or subgroup analyses and their limits.
- [ ] Compute budget, hardware/software details, and failed-run handling.
- [ ] Falsification condition and failure analysis plan.
- [ ] Expected evidence and which conclusion would remain unsupported.

Do not use a test set to tune, choose, or calibrate a model unless the protocol explicitly defines and justifies that role. See [evidence-policy.md](evidence-policy.md) for claim scope.
