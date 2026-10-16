---
name: research-repo-maintainer
description: Use when saving, organizing, updating, or versioning research documents in a local Git repository or GitHub repository.
---

# Research Repo Maintainer

## Purpose

Store research records safely and keep their repository history understandable. This skill manages document location and versioning; it does not design experiments, edit academic prose, audit reproducibility, or verify citations. Use `experiment-designer`, `academic-editing`, `reproducibility-auditor`, or `citation-verifier` for those content tasks. Follow the shared [evidence policy](../../shared/evidence-policy.md) when recording research claims and results.

## Inputs

Identify the document or record, intended repository and path, whether the remote is public, private, or intended for double-blind peer review, and the requested GitHub actions. If the destination, anonymity requirement, or visibility is unknown, ask before placing research material there.

## Workflow

1. Inspect repository instructions, current branch, working-tree status, `.gitignore` rules, and nearby documentation. Preserve existing user changes and follow the repository's structure; do not overwrite unrelated work.
2. Check that the destination is appropriate for the material:
   - Keep personal research goals and identifying details out of project records by default, including thesis plans, target-venue ambitions, names, and institutional details. For double-blind review repositories, also verify that Git author metadata (`user.name`, `user.email`) and file headers are anonymized.
   - Never store credentials, tokens, private keys, `.env` files, private or restricted data, or confidential review material.
   - Strip or sanitize local system paths (e.g., home directory usernames in logs or error traces) and sensitive cell outputs in interactive notebooks (`.ipynb`) before staging.
   - Do not copy unpublished or otherwise sensitive research into a public repository. If content sensitivity or repository visibility is uncertain, pause and ask.
3. Prevent repository bloat by checking file sizes and types before staging. Keep large artifacts—including raw datasets (e.g., `.csv`, `.parquet`, `.zarr`), archives, and model checkpoints (e.g., `.pt`, `.ckpt`)—out of standard Git tracking. Ignore them or use Git LFS where appropriate, and record their storage paths or provenance. Small public or synthetic datasets may be tracked when useful and permitted by repository policy and license.
4. Organize records so readers can distinguish proposals, ongoing work, completed procedures, and verified results. Preserve source, data, and configuration provenance when available. When recording verified experimental results or metrics, link them to the exact code commit hash, Git tag, or experiment run ID that produced them. Do not present planned work as completed or undocumented results as verified. Record public-source provenance and applicable terms when adding external material.
5. When research direction changes, preserve superseded plans or decisions as clearly marked legacy material when useful, and link the current direction to that history. Ask before deleting records, rewriting Git history, or removing remote content.
6. Make only the requested repository changes. Review the diff and affected links before staging or committing. Follow repository-specific commit conventions; otherwise use clear, structured messages that make the research timeline readable from the Git log. If a merge or rebase conflict occurs, do not resolve ambiguities in research records or metrics automatically; pause and ask the user. Push, create a pull request, change repository visibility, or otherwise modify GitHub only when the user explicitly requests that action and the target repository and branch are clear.
7. Report the paths changed, commit hashes created, branch and remote actions taken, and any content or large files that were left out or need a safer destination.

## Validation

- Check that new files are in the intended repository, large binaries/datasets are excluded or handled through Git LFS, and no unrelated working-tree changes or OS/IDE artifacts (`.DS_Store`, `.idea/`, `.vscode/`) were included.
- Review the diff for personal or sensitive information, local system paths, notebook outputs, credentials, unsupported research claims, and accidental deletion of prior records.
- Verify that newly recorded experimental results reference the corresponding code commit hash, tag, or configuration file.
- For double-blind review targets, confirm that neither file contents nor Git commit metadata leak author identity.
- Check links and references affected by document moves or renames.
- If a credential or sensitive dataset appears to have been committed, stop further publication, avoid reproducing the secret, and tell the user. Deleting the visible file does not remove it from Git history; credential revocation and any history cleanup require an authorized remediation plan.

## Failure Modes

- Assuming a GitHub repository is private or safe for unpublished material.
- Committing personal goals, identifying details, local file paths with usernames, uncleaned notebook outputs, credentials, private data, or confidential reviews.
- Leaking author identity via Git commit metadata or file headers in a repository meant for double-blind peer review.
- Committing large datasets, archives, or model weights directly into standard Git history without Git LFS or proper exclusion.
- Recording verified findings without linking the code version (commit hash/tag) or configuration that generated them, or recording unverified values as completed findings.
- Replacing an earlier research direction or resolving merge conflicts in research records without preserving useful history or obtaining user approval.
- Staging, committing, pushing, or changing remote settings beyond the user's requested scope.
