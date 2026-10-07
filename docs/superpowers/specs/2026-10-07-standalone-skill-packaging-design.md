# Standalone Skill Packaging, Installation, and Discovery Design

## Purpose

Make each research skill independently portable to Codex and other agents that support the `SKILL.md` / Agent Skills directory format. A user should be able to select a skill, obtain a self-contained folder or ZIP, install it into an agent's documented skill directory, and understand how the host discovers it.

This is a packaging and local-install design. It does not publish skills, call hosted APIs, or claim that every agent uses the same discovery path.

## Current State

The repository is the source of truth: each `skills/<name>/SKILL.md` links to reusable materials in sibling `shared/` and `templates/` directories. Copying only a skill folder breaks those relative links. `docs/skill-portability.md` inventories these dependencies and recommends generating optional standalone bundles.

The official Agent Skills format represents a skill as a directory with `SKILL.md` and optional supporting files; OpenAI documentation describes directory and ZIP uploads for its Skills API. Codex plugin packaging is a separate, product-oriented installation/discovery route. This project will target portable skill directories and local discovery first, while treating discovery paths as host-specific. See [Agent Skills specification](https://agentskills.io/specification), [OpenAI Skills documentation](https://developers.openai.com/api/docs/guides/tools-skills), and [Codex plugin architecture](https://developers.openai.com/plugins/concepts/plugins).

## Goals

- Generate a self-contained folder and ZIP for any one of the 15 skills or for all skills.
- Preserve one authoritative copy of shared policies and templates in the source repository; do not duplicate these in source skill folders.
- Include only a skill's transitive local Markdown dependencies in its bundle.
- Include the repository license notice with every generated bundle so redistributed copies retain the license terms.
- Rewrite bundled links so every local reference resolves inside the standalone skill folder.
- Provide a small, dependency-free Python interface for package generation and installation to an explicit destination.
- Document Codex project/user installation and generic Agent Skills-compatible host installation without presenting a universal path as fact.
- Make discovery inspectable through valid `name` and `description` frontmatter and a simple local listing/check command or equivalent documented command.
- Preserve the repository's public-safe, project-agnostic constraints.

## Non-Goals

- Codex plugin or marketplace manifests, plugin publication, or public release automation.
- Uploading skills through OpenAI API or other hosted services; no API keys or credentials are needed.
- Product-specific installers for named third-party agents beyond documenting the generic bundle and directing users to each host's current skill-directory instructions.
- Automatic updates, dependency installation, runtime dependencies, telemetry, or system-wide configuration changes.
- Editing source skill instructions to duplicate shared policy prose solely for packaging.

## Proposed Architecture

Keep the existing source tree unchanged in principle. Add a standard-library Python CLI under `scripts/` that reads the source skills and their local Markdown-link dependency graph and produces output under ignored `dist/` by default.

Per-skill output layout:

```text
dist/skills/<skill-name>/
├── SKILL.md
├── LICENSE
└── references/
    ├── shared/<referenced-policy-files>.md
    └── templates/<referenced-template-files>.md
```

The CLI creates one bundle per selected skill. Bundles contain exactly one `SKILL.md`; `name` and `description` frontmatter remain unchanged so compatible hosts can discover the skill. Supporting resources remain local to the skill under `references/`. A `--zip` option also creates `dist/zips/<skill-name>.zip`, with `<skill-name>/` as its single top-level directory. `--all` generates bundles for all source skills.

The dependency collector follows inline Markdown links, images, and reference definitions recursively from `SKILL.md`, while ignoring inline and fenced code. It includes only repository-local resources in the permitted `skills/`, `shared/`, `templates/`, and `venues/` source areas. The venue overview is included only when transitively referenced (currently through the submission checklist template). It excludes external URLs and anchors. When copied, a link from a skill to a shared policy, template, or venue overview is rewritten to the equivalent `references/shared/...`, `references/templates/...`, or `references/venues/...` path. Links within copied resources are rewritten as needed and remain bundle-local. Rewritten paths are URL-encoded. Unresolved links, path traversal, symlinks escaping the repository, unsupported resource types, invalid skill names, or duplicate bundle paths fail with an actionable error; packaging must not silently produce incomplete bundles.

The CLI supports:

- `list [--path <skills-root>]`, to report source or installed skill names/descriptions without claiming host discovery.
- `package --skill <name>` or `package --all` with optional `--output <directory>` (default `dist/`) and optional `--zip`.
- `validate <bundle>`, to verify one-manifest structure, frontmatter, and internal references.
- `install <bundle-directory-or-zip> --destination <skills-root>`, placing the skill at `<skills-root>/<name>`.
- An explicit overwrite option for an existing same-name destination; default behavior refuses to overwrite. Installation never chooses a destination implicitly.

The default generated folder output is `dist/skills/<name>/`, with optional ZIPs at `dist/zips/<name>.zip`; `dist/` is already ignored. The tool does not delete arbitrary output directories or clean `dist/` wholesale.

## Installation and Discovery

### Codex

Document project-scoped installation to `.agents/skills/<name>/` and user-scoped installation to `~/.agents/skills/<name>/`, using a generated standalone bundle. Link to current official Codex documentation for these locations and recheck it before release. Also document using the repository in place by pointing discovery to its `skills/` directory while keeping sibling resources available. State the distinction between Codex skill discovery and a Codex plugin/marketplace install.

### Other compatible agents

Provide host-neutral steps: read that agent's current official instructions for the skill directory; copy or install the standalone folder beneath that directory; ensure the host indexes `SKILL.md`; and restart/reload only when that host requires it. Do not claim a universal directory path or automatic discovery behavior.

### Discovery inspection

The package's frontmatter is the discovery metadata. A repository command or validation helper should list each available skill's name and description and validate a generated bundle's name, exactly-one-manifest rule, and internal resource links. Discovery output reports what is present on disk; it does not claim that a host has loaded or invoked a skill.

## Interfaces and Error Handling

- Source input: repository root, selected skill name(s), and relative Markdown dependencies.
- Package output: one standalone skill directory per name with one root `SKILL.md`, its linked resources, and the repository `LICENSE`; optionally one ZIP per skill.
- Install input: one validated standalone directory and an explicit destination skills root.
- Install output: `<destination>/<skill-name>` with `SKILL.md` and supporting resources.
- Refuse path escapes and destination collisions by default. A user must explicitly request replacement of a same-name install.
- Report external links as external and leave them unchanged; fail for broken local links rather than rewriting them away.
- Do not copy environment-specific/private files, credentials, test-run artifacts, or repository data beyond declared local skill dependencies.

## Documentation Changes

Update README with package, list/validate, and installation commands; separate Codex project/user locations from generic host instructions; explain that generated files are ignored and reproducible from source. Update `docs/skill-portability.md` from a dependency inventory into instructions for using, generating, inspecting, and installing bundles. Update `.gitignore` only if the chosen generated output is not already ignored. Add CLI help text and examples with no credentials or real user paths.

## Validation Strategy

- Unit tests using Python's standard library for dependency closure, inline/reference/image links, code-region handling, link rewriting and URL encoding, frontmatter constraints, one-manifest output, license inclusion, ZIP layout and safe staging, invalid names, broken links, path traversal, symlink escape, and destination collision/replacement behavior.
- Run package generation in a temporary directory; confirm all 15 skills can be packaged and every generated local link resolves within its bundle.
- Extract generated ZIPs into temporary directories and run the same structural/resource checks.
- Test installation into temporary project- and user-shaped destinations; confirm existing destinations are preserved when overwrite is not requested and replaced only when explicitly requested.
- Validate names/descriptions and discovery listing against source frontmatter. Do not claim host discovery merely because files are installed.
- Check README and portability instructions against current official Codex documentation and the generic Agent Skills specification before release.
- Run existing skill frontmatter/link validation, behavioral tests, `python3 -B -m unittest`, and `git diff --check`; keep packaging checks distinct from behavioral skill evaluations.

## Security and Public-Safety

Treat source links as untrusted paths: resolve them and enforce repository-root containment before reading or copying. Reject symlinks that resolve outside the repository. Do not evaluate links, fetch URLs, execute skill content, or access credentials. The installer writes only under the explicitly supplied destination and refuses collisions unless replacement was requested. Keep generated bundles public-safe and source-derived.

## v0.2 Completion Criteria

A user can generate an individual skill bundle, install it into a chosen skill root, and inspect its discovery metadata without hand-copying shared files. All local Markdown links in generated bundles resolve internally; ZIPs extract to the documented layout; install collisions are handled safely; Codex and generic-host discovery claims are accurate and clearly differentiated.
