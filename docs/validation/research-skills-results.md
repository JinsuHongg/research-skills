# Research Skills Validation Results

**Release assessment: usable v0.1 — six behavioral cases passed; coverage remains limited.** All 26 predefined criteria passed in fresh skill contexts and separate rubric-scoring contexts. This synthetic suite does not establish exhaustive reliability.

## Run record

- **Run date:** 2026-10-06 local time (2026-10-07 UTC)
- **Runner:** Codex CLI `0.153.4`, one ephemeral process per case prompt. L1 used two separate prompt contexts.
- **Scorer:** A separate ephemeral Codex CLI process per case; each scorer received the criteria and observed response, not the skill instructions.
- **Isolation:** Each skill process used a fresh temporary working directory and workspace-write sandbox. The repository itself was not exposed as writable input to those processes. Scoring used a separate temporary read-only context.
- **Model:** The CLI model was not pinned or reported in the captured run metadata.
- **Harness record:** [run.json](runs/2026-10-07-targeted/run.json)

## Case outcomes

| Case | Skill contexts | Score | Result | Captured response and criterion evidence |
|---|---:|---:|---|---|
| E1 — Test-set selection | 1 | 4/4 | PASS | [Response](runs/2026-10-07-targeted/E1.response.md), [scores](runs/2026-10-07-targeted/E1.scores.json) |
| E2 — Nested evaluation and adaptation | 1 | 5/5 | PASS | [Response](runs/2026-10-07-targeted/E2.response.md), [scores](runs/2026-10-07-targeted/E2.scores.json) |
| R1 — Inapplicable versus missing settings | 1 | 3/3 | PASS | [Response](runs/2026-10-07-targeted/R1.response.md), [scores](runs/2026-10-07-targeted/R1.scores.json) |
| X1 — Exploratory experiment and legacy plan | 1 | 5/5 | PASS | [Response](runs/2026-10-07-targeted/X1.response.md), [scores](runs/2026-10-07-targeted/X1.scores.json) |
| L1 — LaTeX source and verification limits | 2 | 5/5 | PASS | [Complete source response](runs/2026-10-07-targeted/L1-1.response.md), [fragment response](runs/2026-10-07-targeted/L1-2.response.md), [scores](runs/2026-10-07-targeted/L1.scores.json) |
| C1 — Missing citation and failed run | 1 | 4/4 | PASS | [Response](runs/2026-10-07-targeted/C1.response.md), [scores](runs/2026-10-07-targeted/C1.scores.json) |

The separate rubric scorer returned **PASS for all 26 criteria**. I reviewed the recorded excerpts against the responses. E1 identifies selection bias and recommends untouched evaluation; E2 accepts nested evaluation conditionally and separates input from label access; R1 distinguishes inapplicable training settings from the missing optimizer; X1 preserves the exploratory/post hoc history and leaves the legacy type unresolved; C1 keeps the citation unresolved and the failed run visible without significance claims.

For L1, the complete-source process compiled the supplied file twice with `pdflatex` (exit 0); the log reports `Reference 'sec:missing' ... undefined` and `There were undefined references.` The generated PDF visibly shows `??`. The separate fragment process marked compilation and rendered inspection unverified under the case's no-compiler/no-project-assets scenario. The compiler log and rendered page were independently checked during this run.

## Harness and verification

- `scripts/validate_skills.py` uses only Python's standard library. It reads the existing case prompts and linked skill resources, keeps scoring criteria out of the skill prompts, materializes supplied artifacts only in temporary directories, runs a fresh context for each prompt, and scores responses in separate fresh contexts. The run supplied both target skills for X1 and C1.
- Each score includes a criterion ID, `PASS`/`FAIL`/`INCONCLUSIVE`, and evidence. The harness rejects missing, duplicated, unknown, or evidence-free criteria.
- `python3 -B -m unittest tests/test_validate_skills.py -v`: **4 tests passed**.
- Codex CLI run: **6/6 cases scored**; no runner or scoring errors.
- `git diff --check`: passed.
- Skill frontmatter validation: **15/15**; Markdown local targets and anchors: **108/108 across 54 files**.
- No skill instruction required a change because this run observed no criterion failure. No dependency was added.

## Limits

The evaluation and grader used the Codex CLI's unpinned default model; model identity was not captured, so exact model-level reproducibility is unavailable. The suite contains six synthetic scenarios and is narrow. Passing these cases is evidence only for these prompts and recorded responses. The first runner attempt could not initialize the CLI's local state database under the read-only filesystem boundary; the successful run used ephemeral contexts with temporary work directories after local runtime-state access was approved. No commit or push was performed.

The fragment-only L1 prompt stipulates that no compiler is available. The host did have `pdflatex`, but the isolated fragment response did not invoke it; that stage tests behavior under the stated scenario, not actual binary absence.
