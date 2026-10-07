# Standalone Skill Packaging Implementation Plan

**Required sub-skill:** `superpowers:executing-plans` (native execution in the current repository)

## Goal

Implement the approved standalone packaging design so a user can list research skills, package one or all into self-contained directories and ZIPs, validate a bundle, and install it under an explicitly selected skills root. Keep the repository source tree as the single source of truth.

## Architecture

Add one standard-library CLI module at `scripts/package_skills.py`, with importable functions for skill discovery, dependency collection, bundle generation, validation, ZIP creation, installation, and command dispatch. Resolve only repository-local Markdown dependencies under `skills/`, `shared/`, `templates/`, and `venues/`; `venues/` resources are included only when transitively linked (currently by the submission checklist template). Preserve external links and rewrite copied local links to paths inside each bundle. Include the repository license notice with each bundle. Write default outputs beneath ignored `dist/`. Test the functions through `unittest` in a new `tests/test_package_skills.py` module. Update the portability guide and README with commands and host-specific discovery guidance.

## Tech Stack

- Python 3 standard library only (`argparse`, `pathlib`, `re`, `shutil`, `tempfile`, `zipfile`, and `unittest`)
- Markdown with relative links
- Existing repository validation harness and `git diff --check`

## Spec

`docs/superpowers/specs/2026-10-07-standalone-skill-packaging-design.md`

## Global Constraints

- Keep source skills, shared policies, and templates authoritative; generate copies only under output directories.
- Preserve the repository's public-safe and research-integrity rules. Do not add user paths, private context, credentials, or illustrative research findings.
- Do not add runtime dependencies, product-specific third-party installers, Codex plugin manifests, hosted publishing, or automatic updates.
- Never infer that a host discovered a skill from the presence of files. Use explicit install destinations and refuse collisions unless replacement is requested.
- Reject broken local references, unsupported linked resources, invalid skill names, and paths or ZIP members that escape their allowed roots.
- Parse only a documented frontmatter YAML scalar subset, reject malformed or unsupported forms, and enforce Agent Skills name/description length limits.
- Do not commit changes as part of this implementation without a separate user request.

## Review Focus

1. Does packaging recursively include each referenced local Markdown file exactly once and omit unreferenced shared resources and venue files?
2. Do rewritten links—including links between copied shared files—resolve within the generated bundle while anchors and external URLs remain intact?
3. Do broken links, path traversal, symlink escapes, invalid names, and unsafe ZIP members fail before writing outside the selected roots?
4. Does installation preserve an existing skill on default collision and replace it only when explicitly requested?
5. Do docs distinguish Codex discovery/install locations from host-specific generic Agent Skills guidance and avoid claims of automatic host loading?

## Implementation Tasks

### Task 1: Add source discovery and dependency-closure tests

**Files:** `tests/test_package_skills.py` (new), `scripts/package_skills.py` (new, initially absent or test-only skeleton).

1. Write failing `unittest` cases for:
   - listing source skills with frontmatter `name` and `description`;
   - rejecting missing or invalid skill names and metadata that does not match its source directory;
   - collecting a transitive closure of relative Markdown links from `SKILL.md`;
   - omitting unreferenced resources and preserving external URLs and anchor-only links;
   - failing on broken local links, unsupported linked file types, repository path traversal, and a symlink resolving outside the repository.
2. Run `python3 -B -m unittest tests.test_package_skills -v` and confirm the new tests fail because the module/API is not implemented.
3. Implement importable functions with stable interfaces:
   - `discover_skills(root: Path) -> list[dict[str, str]]` returns sorted skill names and descriptions from immediate skill directories;
   - `collect_dependencies(root: Path, skill_dir: Path) -> list[Path]` returns the `SKILL.md` and each reachable local Markdown resource once;
   - `main(argv: list[str] | None = None) -> int` will be completed in Task 3.
4. Re-run the focused tests and confirm the discovery and dependency-closure cases pass.

### Task 2: Generate and validate self-contained bundle directories and ZIPs

**Files:** `tests/test_package_skills.py`, `scripts/package_skills.py`.

1. Add failing cases for bundle layout, exactly one `SKILL.md`, preserved frontmatter, rewritten inline and reference links, ignored code examples, encoded filenames, license inclusion, recursive shared-resource links, bundle validation, and ZIP top-level layout/extraction.
2. Add negative cases for invalid bundle metadata, unresolved links after rewriting, and invalid YAML/Agent Skills field constraints.
3. Run the focused test module and confirm these cases fail before implementation.
4. Implement:
   - `build_bundle(root: Path, skill_name: str, output_root: Path) -> Path`, writing `output_root/skills/<name>/SKILL.md` and reachable dependencies beneath `references/<source-area>/`, including `shared/`, `templates/`, and transitively linked `venues/` resources;
   - `validate_bundle(bundle: Path) -> list[str]`, returning an empty list when valid and actionable validation errors otherwise;
   - `create_zip(bundle: Path, zip_path: Path) -> Path`, writing a ZIP whose sole top-level directory is the skill name.
5. Rewrite only local links to copied resources; retain fragments, external links, and unrelated valid syntax. Preserve selected-skill local resources beneath `references/skills/<name>/` if any occur. Ensure no resource is copied twice and no link points back to the source repository.
6. Re-run focused tests and confirm generated directory and ZIP bundles validate.

### Task 3: Add safe explicit-destination installation and CLI commands

**Files:** `tests/test_package_skills.py`, `scripts/package_skills.py`.

1. Add failing cases for installing a directory bundle and ZIP into a temporary destination, refusing an existing destination by default, explicit replacement, malformed bundle rejection, and ZIP traversal/symlink rejection.
2. Run the focused tests and confirm these cases fail before implementation.
3. Implement `install_bundle(bundle: Path, destination: Path, replace: bool = False) -> Path`. Validate before installation, stage files under the destination filesystem, and avoid changing an existing installation unless `replace=True`. For ZIP input, inspect member paths and file types before extraction and extract only the expected skill directory into a temporary staging area.
4. Complete `main(argv)` with `list [--path <skills-root>]`, `package --skill <name>` / `package --all`, optional `--output` / `--zip`, `validate <bundle>`, and `install <bundle> --destination <skills-root> [--replace]`. Default source root is derived from the script location; all writes are scoped to explicit or documented output roots.
5. Add CLI-level tests for command output, exit codes, and actionable errors without asserting exact cosmetic formatting.
6. Re-run focused tests and confirm install behavior and command dispatch.

### Task 4: Document packaging, installation, and discovery

**Files:** `README.md`, `docs/skill-portability.md`, `scripts/package_skills.py` (CLI help).

1. Add concise command examples for listing, packaging one skill or all skills, creating ZIPs, validating bundles, and installing to an explicit directory.
2. Explain the generated layout, ignored/reproducible `dist/` output, and how to use source skills in place while retaining sibling resource directories.
3. Document Codex project and user skill directories separately from generic host instructions. Verify the Codex paths and Agent Skills claims against current official documentation before presenting them; describe host-specific reload/discovery behavior as host-dependent.
4. Preserve the existing resource inventory while changing `docs/skill-portability.md` into a usage guide. Check every new relative Markdown link.

### Task 5: Run integrated packaging and repository checks

**Files:** no planned source changes; repair only issues found in earlier tasks.

1. Run packaging in a temporary output root for every source skill and confirm all 15 generated bundles pass `validate_bundle` and every local Markdown link resolves within its own bundle.
2. Create ZIPs for all skills, extract them into a temporary directory, and validate the extracted bundles.
3. Run installation cases against temporary project-shaped and user-shaped destination roots, confirming the installed directory matches the validated bundle.
4. Run `python3 -B -m unittest discover -s tests -v`, verify that all 15 source skills appear with valid names and descriptions, check that every local Markdown link in generated bundles resolves within its bundle, and run `git diff --check`.
5. Review the final diff against the design spec, especially ZIP path handling, destination collision behavior, docs accuracy, and generated-output ignore rules. Report any official-source facts that could not be reverified instead of implying they were checked.
