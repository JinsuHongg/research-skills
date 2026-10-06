# Research Skills v0.1 Design

## Purpose

Create a public, reusable collection of AI skills for computer science, machine learning, data science, computer vision, uncertainty quantification, and adjacent research workflows. The repository provides operational guidance and structured artifacts from literature review through rebuttal. It does not contain project-specific research context or attempt to automate research judgment without evidence.

## Audience and success criteria

The intended users are researchers and AI agents supporting conference and journal publication work. A first-time reader should be able to understand the repository, select an appropriate skill, use its expected inputs and outputs, and follow evidence and research-integrity safeguards. The v0.1 collection should be complete enough to support the workflow while avoiding software infrastructure and time-sensitive venue claims.

## Public-safety and research-integrity constraints

- Keep all content project-agnostic and suitable for a public repository.
- Exclude personal, institutional, credential, unpublished-project, user-specific, proprietary, and confidential reviewer information.
- Keep private project context outside this repository; examples must be synthetic, toy, or based on fully public benchmark tasks.
- Never fabricate citations, metadata, experimental results, statistical significance, theorem statements, or venue requirements.
- Mark unverified facts, interpretations, unresolved citations, and unsupported claims explicitly.
- Require verification against current official venue sources before relying on venue rules.

## Repository architecture

The repository has five content areas:

- `skills/`: 15 focused `SKILL.md` files for literature review, review, gap finding, question design, experiment design, result analysis, publication figures, method diagrams, LaTeX writing, claim-evidence checking, citation verification, reproducibility auditing, manuscript consistency, submission readiness, and rebuttal.
- `shared/`: seven common policy and checklist documents for research principles, academic writing, citation, evidence, experiments, reproducibility, and review.
- `venues/`: a README and eight lightweight profiles (ICLR, NeurIPS, ICML, CVPR, AAAI, KDD, IEEE TGRS, Pattern Recognition). Profiles emphasize stable scope/context and direct users to verify all current requirements from official sources.
- `templates/`: six reusable markdown artifacts for literature matrices, experiment plans, claim-evidence matrices, paper reviews, reproducibility reports, and submission checklists.
- `examples/`: a README defining safe example boundaries; no personal research examples are included in v0.1.

Root documentation includes `README.md`, `AGENTS.md`, `.gitignore`, and a permissive MIT `LICENSE` for reusable prompt and supporting content.

Each skill has one primary responsibility and shares a consistent operational structure: purpose and scope, triggers, inputs, ordered workflow, outputs, validation, failure modes, research-integrity rules, and interaction with related skills. Shared policies hold reusable cross-skill rules; skill files link to those policies rather than copying long passages. Skill frontmatter uses a searchable name and a concise trigger-focused description.

## Research workflow and artifact flow

The README presents this sequence:

`Idea → Literature Review → Research Gap → Research Question / Hypothesis → Experiment Design → Experiment Execution → Result Analysis → Figures / Tables → Paper Writing → Internal Review → Validation → Submission → Rebuttal`

Skills can be used independently. Where evidence should flow between stages, structured artifacts are the interface: literature matrix to related-work outline; experiment plan and verified results to results writing; claim-evidence matrix to abstract and conclusion; review and audit templates to internal validation. Writing consumes validated artifacts and does not fill evidence gaps by invention.

## Skill responsibilities

- **literature-review**: collect and classify verified sources, extract comparable details, distinguish source facts from interpretation, and draft a related-work outline only after evidence capture.
- **paper-reviewer**: support conference, journal, methodological, statistical, reproducibility, and adversarial/internal modes; separate fatal, major, minor, and optional issues without penalizing methodological preference alone.
- **research-gap-finder**: categorize candidate gaps and distinguish an apparent absence of prior work from a meaningful contribution; attach evidence, importance, novelty uncertainty, likely objections, and substantiation needs.
- **research-question-designer**: derive testable questions, hypotheses, claims, falsification criteria, evidence needs, baselines, and confounders.
- **experiment-designer**: map each experiment to a paper claim and specify data/splits, leakage controls, baselines, ablations, metrics, seeds, statistical reporting, selection policy, robustness, compute budget, and failure analysis.
- **result-analyzer**: report observations, interpretations, justified claims, and unsupported claims separately; include effect sizes and uncertainty only when available and never infer unperformed tests.
- **publication-figure**: choose a visualization for the scientific claim and provide guidance for readable, accessible, honest quantitative figures, including uncertainty, scale, and output format.
- **method-diagram**: create scientifically clear conceptual and pipeline diagrams whose components and relationships match the described method.
- **latex-paper-writer**: draft or revise LaTeX sections from validated literature, plans, results, and claim-evidence artifacts; preserve technical meaning and avoid invented content or filler.
- **claim-evidence-checker**: map important claims to required and actual evidence, locations, support status, severity, and revisions; flag unsupported strength, causal overreach, and limited generality.
- **citation-verifier**: separately verify bibliographic metadata and whether a source supports its associated statement; leave unresolved citations explicitly unresolved.
- **reproducibility-auditor**: inspect data, preprocessing, splits, training, selection, calibration, metrics, compute, software, artifacts, and availability; classify each as complete, incomplete, ambiguous, or missing.
- **paper-consistency-checker**: find manuscript-wide naming, notation, numeric, method, hyperparameter, and cross-reference mismatches with precise locations.
- **submission-readiness**: audit research, evidence, presentation, reproducibility, anonymization, venue compliance, and supplements using PASS, WARNING, FAIL, or NOT CHECKED; verify current official requirements.
- **rebuttal**: cluster and prioritize reviewer feedback, separate valid issues from misunderstandings, and draft concise evidence-based responses without promising unfinished work.

## Shared policies and templates

Shared policy files define citation verification and source hierarchy; evidence types and claim support; direct academic writing; experiment design checks; reproducibility checks; and a general CS/ML/data-science review rubric. Templates provide consistent fields for literature, experiment, claim-evidence, review, reproducibility, and submission artifacts. Templates are blank reusable structures, not filled with project-specific or fabricated content.

## Venue guidance

Venue profiles are lightweight orientation, not authoritative or permanent specifications. Every profile and the venue index instruct users to check the current official call for papers, formatting and page limits, anonymity policy, supplementary-material rules, and official LaTeX template before submission. No current-year dates or unverified policy claims are stored as facts.

## Documentation and contribution guidance

The README explains purpose, audience, philosophy, layout, skill interactions, the workflow diagram, public-safe boundaries, contributions, limitations, and how to add a skill. `AGENTS.md` applies the same public-safety rules to contributors, asks them to keep skills modular and operational, avoid unnecessary duplication, validate internal links, use synthetic examples, avoid invented references, and update the README when the collection changes materially. `.gitignore` excludes the requested local/private/secrets/output/cache paths, common credential files, editor artifacts, and Python caches/build output.

## Out of scope for v0.1

- Automated literature search or citation APIs.
- Code, scripts, workflow engines, CI, or elaborate validation infrastructure.
- Venue deadline calendars or guarantees of venue compliance.
- Personal research examples or populated experiment-result examples.
- Project-specific methods, datasets, private data, or institutional context.
- Exhaustive venue coverage or detailed venue-specific interpretations.

## Validation approach

Review all generated files for coverage of this design and consistency with the public-safe constraints. Check skill structure and metadata consistency, internal links and directory references, duplicated policy text, placeholder or fabricated references, example provenance, and claims about changing venue rules. The repository should remain understandable without prior knowledge of its owner or a particular project.

## v0.2 direction

After v0.1 is used on public or synthetic workflows, consider adding opt-in examples, lightweight link/structure checks, additional stable venue profiles, and refinements based on user feedback. Any automation should remain small and should not replace source, evidence, or venue verification.
