# Research Skills v0.1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the approved public-safe, project-agnostic research skill collection described in [the design spec](../specs/2026-10-06-research-skills-design.md).

**Architecture:** Keep each skill in its own `skills/<name>/SKILL.md`, shared rules in `shared/`, reusable blank artifacts in `templates/`, and short non-authoritative venue notes in `venues/`. Root documentation explains discovery, contribution, and the evidence-preserving research workflow; skills link to shared policy instead of duplicating it.

**Tech Stack:** Markdown, YAML frontmatter, Mermaid; no code or runtime dependencies in v0.1.

**Spec:** `docs/superpowers/specs/2026-10-06-research-skills-design.md`

## Global Constraints

- Keep all content public-safe, project-agnostic, and free of personal, institutional, credential, unpublished-project, user-specific, proprietary, and confidential reviewer information.
- Examples use synthetic data, toy problems, or fully public benchmark tasks.
- Never fabricate references, results, significance, theorem statements, venue facts, or support for claims.
- Verify dynamic venue requirements against current official sources; do not encode deadlines or page limits as permanent facts.
- Keep the 15 skills modular and use shared policy links to avoid unnecessary duplication.
- Do not add software infrastructure in v0.1.

## Review Focus

- An agent might write prose despite missing evidence; verify the LaTeX writer requires validated artifacts and surfaces evidence gaps.
- A result summary might imply unperformed statistical tests; verify the analyzer distinguishes observations, interpretations, and supported claims.
- A gap statement might turn missing literature coverage into a novelty assertion; verify the gap finder marks uncertainty and substantiation needs.
- A venue profile might imply stale rules are current; verify each profile points to official, current instructions.
- A public-safe example might accidentally contain identifiable/private context; review every example and template for synthetic/generic-only content.

---

### Task 1: Shared Research Policies

**Files:** Create `shared/research-principles.md`, `shared/academic-writing-guidelines.md`, `shared/citation-policy.md`, `shared/evidence-policy.md`, `shared/experiment-checklist.md`, `shared/reproducibility-checklist.md`, `shared/review-rubric.md`.

- [ ] Define cross-cutting public-safety, evidence, citation, writing, experiment, reproducibility, and review guidance in the corresponding files.
- [ ] Keep policies concise, actionable, complementary, and free of fabricated references or project examples.
- [ ] Review all seven documents against their design-spec responsibilities and cross-links; remove duplicate rules where a link suffices.

### Task 2: Reusable Templates

**Files:** Create `templates/literature-matrix.md`, `templates/experiment-plan.md`, `templates/claim-evidence-matrix.md`, `templates/paper-review.md`, `templates/reproducibility-report.md`, `templates/submission-checklist.md`.

- [ ] Add the fields listed in the design spec, with support statuses and blank placeholders that cannot be mistaken for factual example content.
- [ ] Check that each template is usable on its own, cross-references applicable shared policy, and contains no personal or research-specific data.

### Task 3: Literature Review Skill

**Files:** Create `skills/literature-review/SKILL.md`.

- [ ] Write searchable frontmatter and the agreed operational sections; make source verification and facts-versus-interpretation explicit.
- [ ] Define literature-matrix output, source hierarchy, uncertainty handling, and the condition for writing a Related Work outline.
- [ ] Validate with a synthetic prompt containing unverified citation details; ensure the workflow leaves them unresolved instead of inventing metadata or source support.

### Task 4: Paper Reviewer Skill

**Files:** Create `skills/paper-reviewer/SKILL.md`.

- [ ] Cover all six review modes and distinguish fatal, major, minor, and optional findings.
- [ ] Require evidence/location for findings and prevent rejection based on methodological preference alone.
- [ ] Validate with a toy manuscript scenario that mixes one evidence-backed technical issue, one preference, and one uncertainty; verify each is categorized appropriately.

### Task 5: Research Gap Finder Skill

**Files:** Create `skills/research-gap-finder/SKILL.md`.

- [ ] Cover theoretical, methodological, empirical, evaluation, dataset, robustness, and reproducibility gaps.
- [ ] Require evidence, importance, novelty uncertainty, likely objection, and substantiation for every candidate gap.
- [ ] Validate with a synthetic sparse-literature scenario; ensure “not found” is not reported as proven novelty or a meaningful contribution by itself.

### Task 6: Research Question Designer Skill

**Files:** Create `skills/research-question-designer/SKILL.md`.

- [ ] Define outputs for questions, testable hypotheses, claims, falsification criteria, evidence, baselines, and confounders.
- [ ] Require conditions, metric, comparator, and guardrail where applicable; reject vague “better” hypotheses.
- [ ] Validate using a broad toy idea and confirm the result is falsifiable without inventing expected outcomes.

### Task 7: Experiment Designer Skill

**Files:** Create `skills/experiment-designer/SKILL.md`.

- [ ] Connect every proposed experiment to a named paper claim and cover data/splits, leakage controls, baselines, ablations, metrics, seeds, statistics, selection policy, robustness, compute, and failure analysis.
- [ ] Include calibration split policy where appropriate and avoid experiments without a claim-level purpose.
- [ ] Validate with a synthetic experiment brief containing leakage and model-selection risks; check both are made explicit.

### Task 8: Result Analyzer Skill

**Files:** Create `skills/result-analyzer/SKILL.md`.

- [ ] Define separate output sections for observations, interpretations, justified claims, and unsupported claims.
- [ ] Require effect size and uncertainty only when provided; forbid significance language without an actual test and supplied results.
- [ ] Validate with synthetic results lacking significance tests and containing a failed run; confirm neither is silently omitted or overstated.

### Task 9: Publication Figure Skill

**Files:** Create `skills/publication-figure/SKILL.md`.

- [ ] Require selection of a visualization that matches the scientific claim and cover supported plot types, uncertainty, dimensions, vector output, accessibility, grayscale, legends, normalization, and axes.
- [ ] Forbid changing or omitting data to make a figure look stronger.
- [ ] Validate with a toy quantitative claim and confirm figure choice, uncertainty display, and axis risks are addressed.

### Task 10: Method Diagram Skill

**Files:** Create `skills/method-diagram/SKILL.md`.

- [ ] Cover model, training/calibration/inference, data pipelines, comparisons, and UQ workflows as applicable.
- [ ] Require fidelity to the supplied method and scientific clarity over decoration.
- [ ] Validate with a generic pipeline brief; ensure missing components are queried or marked rather than invented.

### Task 11: LaTeX Paper Writer Skill

**Files:** Create `skills/latex-paper-writer/SKILL.md`.

- [ ] Cover requested manuscript sections while preserving LaTeX, notation, citations, and technical meaning.
- [ ] Require validated artifacts for related work, experimental results, abstracts, and conclusions; mark missing evidence rather than filling gaps.
- [ ] Validate with a toy outline whose results and references are absent; ensure no numbers, citations, or theorem claims are fabricated.

### Task 12: Claim-Evidence Checker Skill

**Files:** Create `skills/claim-evidence-checker/SKILL.md`.

- [ ] Define the claim-evidence matrix with claim type, required/actual evidence, source location, support status, severity, and suggested revision.
- [ ] Cover significance, state-of-the-art, robustness, generalization, and causal overreach cases.
- [ ] Validate with synthetic overclaimed statements and incomplete evidence; ensure statuses distinguish partial support from unverifiability.

### Task 13: Citation Verifier Skill

**Files:** Create `skills/citation-verifier/SKILL.md`.

- [ ] Separate bibliographic metadata verification from semantic support verification.
- [ ] Cover title, authors, venue, year, identifier, BibTeX, primary sources, published/preprint versions, and unresolved cases.
- [ ] Validate with toy incomplete and mismatched citation records; ensure no plausible-looking substitute reference is fabricated.

### Task 14: Reproducibility Auditor Skill

**Files:** Create `skills/reproducibility-auditor/SKILL.md`.

- [ ] Cover the data, preprocessing, split, model, training, selection, calibration, metric, compute, software, checkpoint, and availability fields in the spec.
- [ ] Use complete, incomplete, ambiguous, and missing statuses with precise evidence locations.
- [ ] Validate with a toy paper excerpt that omits multiple setup details; ensure omissions are reported as unknown, not inferred.

### Task 15: Paper Consistency Checker Skill

**Files:** Create `skills/paper-consistency-checker/SKILL.md`.

- [ ] Cover notation, acronym, dataset size/splits, metrics, numbers, figures, method names, hyperparameters, theorem/algorithm notation, and references.
- [ ] Require precise source locations and distinguish confirmed mismatches from items needing manual verification.
- [ ] Validate with a toy manuscript containing deliberate mismatches; ensure each issue is actionable and located.

### Task 16: Submission Readiness Skill

**Files:** Create `skills/submission-readiness/SKILL.md`.

- [ ] Cover novelty, correctness, evidence, baselines, ablations, statistics, reproducibility, figures, citations, consistency, limitations, anonymization, venue compliance, and supplements.
- [ ] Use PASS, WARNING, FAIL, and NOT CHECKED; require current official venue-source verification before claiming compliance.
- [ ] Validate with a toy checklist including unknown venue rules; ensure unknown requirements remain NOT CHECKED.

### Task 17: Rebuttal Skill

**Files:** Create `skills/rebuttal/SKILL.md`.

- [ ] Define reviewer/issue/severity/validity/experiment/clarification/correction/priority outputs and require clustering overlapping comments.
- [ ] Prioritize correctness, material misunderstandings, evidence, clarification, then presentation; keep responses respectful and evidence-based.
- [ ] Validate with synthetic reviewer comments including an unfinished experiment; ensure the response does not promise completion.

### Task 18: Venue Profiles and Safe Examples

**Files:** Create `venues/README.md`, `venues/iclr.md`, `venues/neurips.md`, `venues/icml.md`, `venues/cvpr.md`, `venues/aaai.md`, `venues/kdd.md`, `venues/ieee-tgrs.md`, `venues/pattern-recognition.md`, `examples/README.md`.

- [ ] Keep each profile lightweight and add the current-official-source verification instruction for calls, formats, page limits, anonymity, supplements, and LaTeX templates.
- [ ] Add no deadline calendar or unsourced permanent venue rules.
- [ ] State that future examples must be synthetic, toy, or fully public benchmark work; add no populated personal research examples.

### Task 19: Root Documentation and License

**Files:** Modify `README.md`, `.gitignore`; create `AGENTS.md`, `LICENSE`.

- [ ] Explain purpose, audience, design philosophy, structure, skill interaction, limitations, contribution rules, and public-safe boundaries in README; include the workflow Mermaid diagram.
- [ ] Define contributor rules in `AGENTS.md`, including modularity, concise instructions, link checking, synthetic examples, citation integrity, and README updates.
- [ ] Add all requested private/local/secret/output/editor exclusions plus common Python cache/build ignores to `.gitignore`.
- [ ] Add standard MIT license text; ensure file dates and copyright owner wording do not invent a person or institution.

### Task 20: Repository-Wide Review

**Files:** All files created or modified above.

- [ ] Compare the generated tree against the approved spec and confirm all 15 skills, seven shared documents, eight venue profiles plus index, six templates, and root files exist.
- [ ] Inspect every skill for consistent sections, valid frontmatter, operational workflows, appropriate integrity rules, and correct upstream/downstream references.
- [ ] Check all relative Markdown links and referenced paths; fix broken references.
- [ ] Search all repository content for personal, institutional, confidential, project-specific, credential, fabricated-reference, temporary venue-rule, and stale-date content; manually inspect every match.
- [ ] Remove duplicate policy prose where shared links are sufficient and ensure the README is understandable to a first-time visitor.
- [ ] Report checks performed and any limitation that prevents a claim of complete verification.
