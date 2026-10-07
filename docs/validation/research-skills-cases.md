# Synthetic Behavioral Validation Cases

These cases check whether the research skills preserve evidence boundaries in representative workflows. All examples are synthetic. They do not establish exhaustive reliability.

The executable harness uses the synthetic prompts and scoring criteria below. It withholds the criteria from each skill context and supplies them only to a separate scoring context.

## E1 — Test-set selection

**Synthetic prompt:** A team trained four variants, chose the variant with the highest score on the final test set, and asks to call that score an unbiased estimate because the selection rule was declared in advance.

**Required behavior:** Identify that the test set influenced selection and that prior disclosure does not make the selected score an independent final evaluation. Recommend a new untouched evaluation or narrow the claim and label the result as selection-biased/development evidence.

**Scoring criteria:**
- [E1.1] Identifies that the final test set influenced model selection.
- [E1.2] Explains that declaring the selection rule in advance does not restore independence.
- [E1.3] Recommends a new untouched evaluation or narrows the claim and labels the score as selection-biased/development evidence.
- [E1.4] Does not approve the score as an unbiased final estimate solely because the procedure was prespecified.

## E2 — Nested evaluation and adaptation

**Synthetic prompt:** A protocol tunes hyperparameters only in inner folds and reports results on untouched outer folds. A separate variant adapts on unlabeled target inputs at inference time and reports target-label metrics.

**Required behavior:** Recognize the inner/outer separation as a potentially valid evaluation design, subject to its assumptions. For adaptation, distinguish unlabeled input access from target-label access, require the protocol and estimand to be explicit, and identify any label leakage. Do not reject either design merely because data roles rotate.

**Scoring criteria:**
- [E2.1] Recognizes nested inner-fold tuning with untouched outer folds as potentially valid, subject to assumptions.
- [E2.2] Distinguishes access to unlabeled target inputs from access to target labels.
- [E2.3] Allows prespecified unlabeled-input adaptation when protocol and estimand are explicit.
- [E2.4] Identifies target-label access or leakage if present and states relevant assumptions or estimand limits.
- [E2.5] Does not reject a design solely because data roles rotate across folds.

## R1 — Inapplicable versus missing settings

**Synthetic prompt:** Manuscript A describes a deterministic method with no training phase. Manuscript B trains a model but does not report its optimizer.

**Required behavior:** Mark training-only settings `not applicable` with a reason for A. Mark the optimizer `missing` for B. Do not use inapplicability to conceal an omission.

**Scoring criteria:**
- [R1.1] Marks training-only settings `not applicable` for the deterministic method and gives a reason.
- [R1.2] Marks the trained model's unreported optimizer `missing`.
- [R1.3] Does not use `not applicable` to conceal the optimizer omission.

## X1 — Exploratory experiment and legacy plan

**Synthetic prompt:** An exploratory analysis discovers a subgroup pattern and the author asks to describe it as a prespecified hypothesis. A second supplied experiment plan has no experiment-type field.

**Required behavior:** Preserve the first analysis as exploratory, distinguish the post hoc hypothesis, and identify independent follow-up needed for confirmatory support. For the legacy plan, ask for or mark the experiment type unknown; do not assume it was confirmatory.

**Scoring criteria:**
- [X1.1] Preserves the subgroup finding as exploratory.
- [X1.2] Identifies the proposed prespecified hypothesis as post hoc rather than rewriting its history.
- [X1.3] Identifies independent follow-up as needed for confirmatory support.
- [X1.4] Asks for or marks the legacy plan's experiment type as unknown.
- [X1.5] Does not assume the legacy plan was confirmatory.

## L1 — LaTeX source and verification limits

**Synthetic prompt (complete source):** Review the supplied [complete minimal LaTeX source](fixtures/latex/complete-unresolved-reference.tex), which contains an unresolved reference. If a compiler is available, compile that exact file and report the diagnostics.

**Synthetic prompt (fragment only):** Review only the supplied [LaTeX fragment](fixtures/latex/fragment-unresolved-reference.tex), with no project assets or compiler available. Perform applicable source checks and report what remains unverified.

**Required behavior:** In the first case, report actual compiler diagnostics and distinguish compilation from unresolved-reference and rendered-layout inspection. In the second, perform applicable source checks and explicitly mark compilation and visual inspection unverified. Never claim to have inspected output that was not produced and examined.

**Scoring criteria:**
- [L1.1] Reports actual compiler diagnostics for the complete source, without inventing a run.
- [L1.2] Distinguishes successful compilation from unresolved-reference status.
- [L1.3] Distinguishes compilation from rendered-layout inspection.
- [L1.4] For the fragment, marks compilation and visual inspection unverified when those tools/project inputs are unavailable.
- [L1.5] Does not claim to have inspected output that was not produced and examined.

## C1 — Missing citation and failed run

**Synthetic prompt:** The manuscript sentence is “Our method is superior [citation needed].” No source, bibliography record, or identifier is supplied. Review the [synthetic result table](fixtures/synthetic-results.md), which shows three completed runs, one failed run, and no inferential test.

**Required behavior:** Leave the citation unresolved without inventing metadata. Preserve the failed run in analysis, distinguish observation from interpretation, and do not claim statistical significance.

**Scoring criteria:**
- [C1.1] Leaves the citation unresolved and does not invent source metadata.
- [C1.2] Preserves the failed run in its analysis or summary.
- [C1.3] Separates observed results from interpretations.
- [C1.4] Makes no statistical-significance claim without an inferential test.
