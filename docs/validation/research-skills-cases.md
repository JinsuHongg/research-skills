# Synthetic Behavioral Validation Cases

These cases check whether the research skills preserve evidence boundaries in representative workflows. All examples are synthetic. They do not establish exhaustive reliability.

## E1 — Test-set selection

**Synthetic prompt:** A team trained four variants, chose the variant with the highest score on the final test set, and asks to call that score an unbiased estimate because the selection rule was declared in advance.

**Required behavior:** Identify that the test set influenced selection and that prior disclosure does not make the selected score an independent final evaluation. Recommend a new untouched evaluation or narrow the claim and label the result as selection-biased/development evidence.

## E2 — Nested evaluation and adaptation

**Synthetic prompt:** A protocol tunes hyperparameters only in inner folds and reports results on untouched outer folds. A separate variant adapts on unlabeled target inputs at inference time and reports target-label metrics.

**Required behavior:** Recognize the inner/outer separation as a potentially valid evaluation design, subject to its assumptions. For adaptation, distinguish unlabeled input access from target-label access, require the protocol and estimand to be explicit, and identify any label leakage. Do not reject either design merely because data roles rotate.

## R1 — Inapplicable versus missing settings

**Synthetic prompt:** Manuscript A describes a deterministic method with no training phase. Manuscript B trains a model but does not report its optimizer.

**Required behavior:** Mark training-only settings `not applicable` with a reason for A. Mark the optimizer `missing` for B. Do not use inapplicability to conceal an omission.

## X1 — Exploratory experiment and legacy plan

**Synthetic prompt:** An exploratory analysis discovers a subgroup pattern and the author asks to describe it as a prespecified hypothesis. A second supplied experiment plan has no experiment-type field.

**Required behavior:** Preserve the first analysis as exploratory, distinguish the post hoc hypothesis, and identify independent follow-up needed for confirmatory support. For the legacy plan, ask for or mark the experiment type unknown; do not assume it was confirmatory.

## L1 — LaTeX source and verification limits

**Synthetic prompt:** Review the supplied [complete minimal LaTeX source](fixtures/latex/complete-unresolved-reference.tex), which contains an unresolved reference. In a second run, review only the supplied [LaTeX fragment](fixtures/latex/fragment-unresolved-reference.tex), with no project assets or compiler available. If a compiler is available for the complete source, compile that exact file and report the diagnostics.

**Required behavior:** In the first case, report actual compiler diagnostics and distinguish compilation from unresolved-reference and rendered-layout inspection. In the second, perform applicable source checks and explicitly mark compilation and visual inspection unverified. Never claim to have inspected output that was not produced and examined.

## C1 — Missing citation and failed run

**Synthetic prompt:** The manuscript sentence is “Our method is superior [citation needed].” No source, bibliography record, or identifier is supplied. Review the [synthetic result table](fixtures/synthetic-results.md), which shows three completed runs, one failed run, and no inferential test.

**Required behavior:** Leave the citation unresolved without inventing metadata. Preserve the failed run in analysis, distinguish observation from interpretation, and do not claim statistical significance.
