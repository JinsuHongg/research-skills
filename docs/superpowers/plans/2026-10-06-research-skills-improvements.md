# Research Skills Improvement Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans for task-by-task implementation; use superpowers:subagent-driven-development only when delegation is authorized. Steps use checkbox (`- [ ]`) syntax for tracking. This document proposes implementation; creating it does not authorize implementation, commits, or external actions.

**Goal:** Resolve policy contradictions and improve audit accuracy and output verification without expanding the existing 15-skill collection.

**Architecture:** Preserve the current skill/shared/template layout. Keep common decisions in shared policies and synchronize their consuming skills and blank templates. Use small, documented synthetic behavioral checks rather than adding a test framework.

**Tech Stack:** Markdown and YAML frontmatter; existing tools only, with no new runtime dependencies or CI.

**Spec:** [Original collection design](../specs/2026-10-06-research-skills-design.md). The proposed corrections and acceptance criteria below refine that design; they are not already implemented.

## Scope and Analysis

The static review identified four instruction defects and one validation-evidence gap. Basic skill validation passed for all 15 skills, and 80 relative Markdown links resolved at review time. These checks do not establish behavioral reliability. No retained behavioral run results were found; this does not prove that no prior testing occurred.

| Priority | Finding | Decision | Deliverable |
|---|---|---|---|
| P1 | Shared policies permit test-set reuse when declared, while the designer prohibits it | Define protection by data role and evaluation claim; disclosure alone is insufficient | Consistent evaluation policy |
| P2 | Reproducibility statuses cannot express inapplicable checks | Add reasoned `not applicable` without hiding missing information | Synchronized audit vocabulary |
| P2 | Exploratory experiments are permitted in one step but excluded by output/template rules | Separate confirmatory claims from exploratory objectives | Consistent experiment artifact |
| P2 | LaTeX validation does not specify build/render checks | Report source, compilation, and visual verification separately | Conditional verification workflow |
| P2 | Behavioral validation cannot be inspected or repeated from retained evidence | Record synthetic inputs, criteria, and actual outcomes | Lightweight regression cases and run record |

Recommended approach: focused documentation changes plus behavioral checks. Wording-only fixes would leave reliability unmeasured; a new automated evaluation framework would exceed the demonstrated need and the original infrastructure constraints.

## Global Constraints

- Keep content public-safe and project-agnostic; use only explicitly synthetic fixtures.
- Never invent references, experimental results, verification outcomes, or venue rules.
- Preserve the 15 existing skill names, descriptions unless necessary, directory structure, and valid relative links.
- Keep templates blank; place synthetic validation inputs outside `templates/`.
- Do not add dependencies, CI, new skills, installer changes, or venue-policy updates.
- Do not rewrite historical design or implementation documents to imply these improvements were previously approved or tested.
- Do not stage, commit, push, or create a pull request without a separate request.
- Treat structural validation, behavioral validation, compilation, and rendered inspection as distinct evidence.

## Review Focus

- A protocol explicitly permits choosing the best test score: Task 1 must still identify selection bias and restrict final claims.
- A valid nested evaluation separates inner selection from outer evaluation: Task 1 must not reject it merely because data roles rotate.
- A deterministic method has no training, while another manuscript omits relevant training details: Task 2 must distinguish inapplicability from missingness.
- An exploratory result motivates a hypothesis: Task 3 must not relabel the same result as independent confirmation.
- A LaTeX fragment or unavailable compiler prevents full verification: Task 4 must preserve useful editing and report the actual verification limit.

## Task 1: Align Evaluation Integrity Rules

**Files to modify:**
- `shared/research-principles.md`: short cross-workflow rule.
- `shared/experiment-checklist.md`: operational checks and exceptions by protocol.
- `skills/experiment-designer/SKILL.md`: workflow, failure modes, and validation.

**Interface:** Consumes data-role and selection-policy descriptions; produces an evaluation plan with explicit permissible claims and unresolved contamination risks.

- [ ] Define the final evaluation boundary: outcomes used to choose among methods, settings, or procedures cannot also be presented as independent confirmation of the selected procedure. A fixed, prespecified transductive or test-time adaptation method may consume evaluation inputs when its access and estimand are explicit.
- [ ] Replace declaration-only exceptions with protocol conditions: document accessible data/labels, adaptation or selection stages, evaluation units, and how the reported estimand is evaluated. For nested evaluation, selection stays inside the inner procedure and outer results do not drive subsequent selection.
- [ ] Preserve legitimate transductive or test-time adaptation settings when explicitly scoped; distinguish allowed access to inputs from target-label leakage. If validity cannot be established, mark the design unresolved rather than approve it by disclosure alone.
- [ ] Require contaminated evaluations to be labeled exploratory or selection-biased, with an appropriate independent evaluation or justified alternative needed for stronger claims.
- [ ] Check cases E1 and E2 from Task 5 against all three documents; verify neither unsafe reuse nor blanket rejection of legitimate evaluation remains.

**Acceptance:** All three documents express the same rule. Stating a protocol in advance does not by itself permit an independent-performance claim.

## Task 2: Add Applicability to Reproducibility Audits

**Files to modify:**
- `skills/reproducibility-auditor/SKILL.md`
- `shared/reproducibility-checklist.md`
- `templates/reproducibility-report.md`

**Interface:** Extend the existing status vocabulary with `not applicable`; retain existing statuses and add space for an applicability rationale in the blank report.

- [ ] Determine whether each item applies before judging reporting completeness.
- [ ] Permit `not applicable` only with a reason grounded in the supplied method or audit scope. An omitted setting is not evidence that the setting is unnecessary.
- [ ] Keep applicable but unreported details `missing`; keep uncertain applicability `ambiguous` and identify what would resolve it.
- [ ] Update workflow, validation, checklist, and template together. Do not count justified inapplicability as a reproduction blocker.
- [ ] Evaluate both variants in case R1; verify the new status does not become a shortcut for missing evidence.

**Acceptance:** Non-training methods are not penalized for absent optimizers; trained methods with undocumented optimizers still receive an actionable finding.

## Task 3: Make Exploratory Experiments First-Class

**Files to modify:**
- `skills/experiment-designer/SKILL.md`
- `shared/experiment-checklist.md`
- `templates/experiment-plan.md`
- `skills/result-analyzer/SKILL.md`: preserve experiment type and post-result deviations when interpreting evidence.

**Interface:** Add `Experiment type: confirmatory / exploratory` and an exploratory objective to the experiment artifact. Retain existing claim and hypothesis fields, explicitly conditional on applicability. Older plans without a type remain usable; clarify or mark the type unknown rather than silently assuming confirmatory status.

- [ ] Require confirmatory experiments to identify the prespecified claim/hypothesis; require exploratory experiments to identify the question or diagnostic objective without fabricating a prior hypothesis.
- [ ] Synchronize the designer's workflow, output, validation, and failure modes with both supporting documents; remove unconditional claim requirements where exploration is allowed.
- [ ] Record hypotheses generated after observing results and the independent follow-up needed to evaluate them. Do not require a new experiment merely to report descriptive exploration.
- [ ] Have result-analyzer preserve that distinction and identify post-result analysis choices without treating every deviation as invalid.
- [ ] Evaluate case X1 and one legacy plan without an experiment-type field.

**Acceptance:** Useful exploration is retained and clearly labeled; its findings do not become prespecified or independently confirmed claims by wording alone.

## Task 4: Define Conditional LaTeX Verification

**Files to modify:** `skills/latex-paper-writer/SKILL.md` only.

**Interface:** Add verification reporting for source checks, compilation, and rendered inspection, each with actual outcome or an explicit limitation.

- [ ] For a complete supported document, use the host's supported compiler or the project's established build workflow within existing permissions; do not invent a universal shell command or install TeX/dependencies.
- [ ] Inspect diagnostics for build errors and unresolved citations/references. Distinguish compilation success from a clean bibliography or verified layout.
- [ ] When rendering is available, inspect changed pages, equations, tables, figures, and relevant overflow warnings at intended size. Record what was actually inspected.
- [ ] For snippets, missing project assets, unsupported projects, or unavailable tools, perform possible source checks and explicitly report compilation/rendering as unverified. Do not expand a prose-edit request into project/environment repair.
- [ ] Evaluate case L1 in available and unavailable-tool variants; distinguish a reasoned response to a simulated limitation from an actual compiler execution.

**Acceptance:** Editing remains useful without a compiler, but no unperformed compilation or visual inspection is reported as successful.

## Task 5: Retain Small Behavioral Validation Cases

**Files to create:**
- `docs/validation/research-skills-cases.md`: synthetic input prompts and separate evaluator criteria.
- `docs/validation/research-skills-results.md`: actual run metadata, observed outcomes, evidence, and limitations.

**File to modify:** `README.md`: link to the validation resources and state their limited coverage.

**Interface:** Stable case IDs below connect each changed behavior to an inspectable outcome. Results record revision or working-tree state, date, runner/model if known, available tools, supplied files, observed response/artifact, criterion results, and limitations. Unknown metadata stays unknown.

| Case | Synthetic input | Required behavior |
|---|---|---|
| E1 | A plan selects a model using final test scores and calls the selected score unbiased because reuse was declared | Identify the invalid independence claim; explain evaluation repair or claim restriction |
| E2 | Inner selection with untouched outer evaluation, plus a separately scoped unlabeled adaptation variant | Distinguish valid role separation from leakage; allow fixed input adaptation under explicit access and estimand; state remaining assumptions |
| R1 | Explicitly non-training deterministic method; paired variant describing training but omitting optimizer settings | Use justified `not applicable` in the first and `missing` in the second |
| X1 | Exploration discovers a pattern and requests confirmatory wording; paired older plan omits experiment type | Preserve exploration and propose follow-up; leave unspecified type unresolved |
| L1 | [`complete-unresolved-reference.tex`](../../validation/fixtures/latex/complete-unresolved-reference.tex) with an unresolved reference; paired [`fragment-unresolved-reference.tex`](../../validation/fixtures/latex/fragment-unresolved-reference.tex) without build assets/tools | Report actual diagnostics when run and explicit limitations otherwise; never claim unseen rendered output was checked |
| C1 | Unresolvable synthetic citation placeholder with no source; [`synthetic-results.md`](../../validation/fixtures/synthetic-results.md) has one failed run and no inferential test | Do not fabricate reference metadata, omit the failure, or assert statistical significance |

- [ ] Write the synthetic prompts and evaluator criteria before editing the target skills. Label all toy values and placeholders synthetic; do not invent plausible academic citations.
- [ ] Run a baseline against current instructions when a fresh evaluation context is available. Give the runner only the prompt, target skill, and required resources, not expected answers or proposed fixes.
- [ ] Retain concise observed evidence. If no suitable runner is available, record `NOT RUN`; manual walkthroughs are not behavioral passes.
- [ ] After Tasks 1–4, rerun affected cases under comparable conditions. A baseline pass does not disprove a textual contradiction; report both evidence types honestly.
- [ ] For each failed criterion, make only a focused correction and rerun that case plus directly affected cases. Stop after two correction rounds per case and report remaining failures for review.
- [ ] Populate the results file only from completed runs and explicit non-runs. Link the cases/results from README without claiming exhaustive reliability.

**Acceptance:** Every case has an actual outcome or `NOT RUN` with a reason. Behavioral completion requires passing all required criteria; structural checks cannot substitute for these runs. No agent delegation or external evaluation service is assumed to be authorized by this plan.

## Execution Order and Final Checks

1. Prepare Task 5 cases and capture the baseline before behavioral edits.
2. Implement Task 1, then Task 3 because they share experiment-design files.
3. Implement Tasks 2 and 4.
4. Finish Task 5 with post-change runs and documentation.
5. Perform final scoped verification and report remaining limitations.

- [x] Run the available skill frontmatter validator on all 15 skills; if unavailable, report the limitation without installing dependencies.
- [x] Resolve every relative Markdown link against its containing directory using existing Python 3 standard-library tooling; require zero broken local targets. External venue URLs are outside this change's verification scope.
- [x] Run `git diff --check`; require no whitespace errors.
- [x] Review `git diff -- shared skills templates README.md` and all new validation documents for contradictions, unintended scope changes, fabricated evidence, and private content.
- [x] Use `git status --short` to verify that only planned files changed and no build outputs or temporary evaluation files entered the repository.
- [x] Report changed files, structural checks, behavioral results, and any unverified compilation/rendering separately. Do not mark the plan complete while required behavioral cases remain unrun or failing.

## Completion and Deferred Work

Completion means the four instruction defects are corrected consistently, all required behavioral criteria pass, and structural/link/diff checks pass. Full statistical-method coverage, comprehensive auditing of all 15 skills, automated evaluation infrastructure, and installation/discovery improvements remain outside this plan.

The current deliverable is this plan only. Implementation should begin only after the user requests it; a single implementer is sufficient for the overlapping Markdown changes.
