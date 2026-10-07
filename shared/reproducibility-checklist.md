# Reproducibility Checklist

Report each item as **complete**, **incomplete**, **ambiguous**, **missing**, or **not applicable**, with a paper or artifact location. Use **not applicable** only when the item does not apply to the documented method or audit scope, and state why. Missing documentation is not evidence of inapplicability.

- [ ] Dataset identity, version, access, license, and preprocessing.
- [ ] Data splits, leakage controls, and any calibration data.
- [ ] Architecture, initialization, optimizer, learning rate, batch size, epochs, and stopping criteria.
- [ ] Hyperparameter search, model selection, and checkpoint selection.
- [ ] Random seeds, number of runs, and sources of nondeterminism.
- [ ] Metrics, aggregation, uncertainty, tests, and analysis protocol.
- [ ] Hardware, runtime, software/library versions, and relevant configuration.
- [ ] Checkpoints, code, data availability, and instructions for access or reproduction.
- [ ] Deviations, failed runs, and known limitations.

Do not infer missing settings from common practice. Mark them **missing** or **ambiguous** and state their likely effect on reproduction.
