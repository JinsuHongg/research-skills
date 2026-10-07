# Skill Portability Assessment

The source repository keeps skills modular and shared guidance in one place. To use the collection in place, configure skill discovery for the repository's `skills/` directory and keep `shared/` and `templates/` at their current sibling paths. Tool-specific discovery setup varies; see the [README](../README.md).

The table lists relative resources linked from each skill. Copying a skill directory by itself breaks those links when resources are listed. Skills with no linked repository resources are self-contained with respect to this repository's shared documents and templates; they still need the user-provided research materials and tools named in their instructions.

| Skill | `shared/` resources | `templates/` resources | `venues/` resources | Copying only the skill directory |
|---|---|---|---|---|
| citation-verifier | `citation-policy.md` | — | — | Breaks linked policy |
| claim-evidence-checker | `evidence-policy.md` | `claim-evidence-matrix.md` | — | Breaks linked policy and template |
| experiment-designer | `experiment-checklist.md`, `evidence-policy.md`, `research-principles.md` | `experiment-plan.md` | — | Breaks linked policy and template |
| latex-paper-writer | `academic-writing-guidelines.md`, `citation-policy.md` | `claim-evidence-matrix.md` | — | Breaks linked policy and template |
| literature-review | `citation-policy.md`, `evidence-policy.md` | `literature-matrix.md` | — | Breaks linked policy and template |
| method-diagram | — | — | — | Keeps its repository references |
| paper-consistency-checker | — | — | — | Keeps its repository references |
| paper-reviewer | `evidence-policy.md`, `review-rubric.md` | `paper-review.md` | — | Breaks linked policy and template |
| publication-figure | `evidence-policy.md` | — | — | Breaks linked policy |
| rebuttal | — | — | — | Keeps its repository references |
| reproducibility-auditor | `reproducibility-checklist.md` | `reproducibility-report.md` | — | Breaks linked policy and template |
| research-gap-finder | `evidence-policy.md` | — | — | Breaks linked policy |
| research-question-designer | `evidence-policy.md` | — | — | Breaks linked policy |
| result-analyzer | `evidence-policy.md` | `claim-evidence-matrix.md` | — | Breaks linked policy and template |
| submission-readiness | — | `submission-checklist.md` | — | Breaks linked template |

No skill links directly to a file under `venues/`. Venue-specific workflows rely on current official sources supplied or accessed during the task; the submission-readiness skill explicitly requires those current sources.

## Packaging direction

Keep this repository as the single source of truth. If users need individually installable bundles later, generate optional self-contained copies under a future packaging or `dist/` step by including the referenced shared files and templates. Do not duplicate shared policy text in the source skill files. No bundles or packaging system are created by this assessment.
