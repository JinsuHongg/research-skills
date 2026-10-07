# Skill Portability Guide

The repository keeps skills modular and shared guidance in one place. The packaging CLI creates self-contained folders and ZIPs by following each skill's transitive local Markdown links. It copies only linked files from `skills/`, `shared/`, `templates/`, and `venues/`; venue material is included only when a linked template needs it. Source files remain authoritative, and generated output under `dist/` is ignored by Git.

See the [README](../README.md) for the research workflow and repository principles.

## List and package skills

Run these commands from the repository root:

```bash
python3 scripts/package_skills.py list
python3 scripts/package_skills.py package --skill citation-verifier --zip
python3 scripts/package_skills.py package --all
python3 scripts/package_skills.py validate dist/skills/citation-verifier
```

`list` reports names and descriptions found on disk; it does not confirm that an agent host loaded a skill. `package` writes folders to `dist/skills/<name>/`; `--zip` also writes `dist/zips/<name>.zip`. The generated folder has one `SKILL.md`, linked resources beneath `references/`, and the repository `LICENSE` notice. Existing output paths are preserved: choose an empty `--output` directory or remove the specific generated bundle before rebuilding it.

## Install for Codex

Codex checks project skill folders under `.agents/skills/` (including ancestor directories) and user skills under `~/.agents/skills/`. Install a generated bundle to either scope with an explicit destination:

```bash
python3 scripts/package_skills.py install dist/skills/citation-verifier --destination .agents/skills
python3 scripts/package_skills.py install dist/zips/citation-verifier.zip --destination "$HOME/.agents/skills"
```

The command refuses to replace an existing same-name skill unless `--replace` is supplied. Codex detects skill changes automatically; if a new skill does not appear, restart Codex. Check current [Codex skills documentation](https://developers.openai.com/codex/skills) before relying on locations or behavior that may change.

To use source skills in place during repository development, keep `shared/`, `templates/`, and `venues/` alongside `skills/`, and create a symlink under `.agents/skills/` for each skill you want Codex to discover. Codex documents support for symlinked skill folders. For example, from the repository root:

```bash
mkdir -p .agents/skills
ln -s ../../skills/citation-verifier .agents/skills/citation-verifier
```

The packaging CLI's `list --path` inspects skill folders contained in the selected directory and does not follow skill-directory symlinks whose targets are outside that directory. Use it on the repository's `skills/` directory to list source skills.

## Install for other agents

Read the selected host's current official skill-directory and reload instructions. Copy the standalone folder under the location that host documents, or use its supported ZIP import. The Agent Skills format standardizes the skill folder and `SKILL.md` metadata, but it does not make every host use the same discovery path or installation behavior. See the [Agent Skills specification](https://agentskills.io/specification).

Codex plugins are a separate distribution format. This CLI packages and installs standalone folders; it does not create plugins or publish them.

## Resource inventory

The table lists relative resources linked from each skill. Copying only a skill directory by itself breaks those links when resources are listed. Skills with no linked repository resources are self-contained with respect to the repository's shared documents and templates; they still need the user-provided research materials and tools named in their instructions.

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
| submission-readiness | — | `submission-checklist.md` | `README.md` (transitive through the template) | Breaks linked template and venue guide |

Venue overview files are orientation only. Venue-specific workflows still require current official sources; packaging the overview does not verify changing venue rules.
