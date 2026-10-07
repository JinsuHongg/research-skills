#!/usr/bin/env python3
"""Create and install portable bundles for repository skills."""

from __future__ import annotations

import argparse
import json
import re
import os
import posixpath
import shutil
import stat
import sys
import tempfile
from pathlib import Path
from pathlib import PurePosixPath
from urllib.parse import quote, unquote, urlsplit
import zipfile


FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---(?:\s*\n|\Z)", re.DOTALL)
FRONTMATTER_FIELD = re.compile(r"^(name|description):\s*(.*?)\s*$")
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK = re.compile(r"(!?)\[([^\]]+)\]\(\s*(<[^>]+>|[^)\s]+)([^)]*)\)")
REFERENCE_DEFINITION = re.compile(
    r"(?m)^([ \t]{0,3}\[[^\]\n]+\]:[ \t]*)(<[^>\n]+>|[^ \t\n]+)([^\n]*)"
)
FENCE_OPEN = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})")
INLINE_CODE = re.compile(r"(?<!`)(`+)(?!`)(.*?)(?<!`)\1(?!`)", re.DOTALL)
SOURCE_AREAS = ("shared", "templates", "venues")


def _frontmatter(skill_file: Path) -> dict[str, str]:
    text = skill_file.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        raise ValueError(f"Missing YAML frontmatter: {skill_file}")
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        field = FRONTMATTER_FIELD.match(line)
        if field:
            key, value = field.groups()
            if key in fields:
                raise ValueError(f"Duplicate frontmatter field {key!r}: {skill_file}")
            fields[key] = _yaml_string(value, key, skill_file)
    if not fields.get("name") or not fields.get("description"):
        raise ValueError(f"Frontmatter requires non-empty name and description: {skill_file}")
    length_errors = []
    if len(fields["name"]) > 64:
        length_errors.append("Skill name exceeds 64 characters")
    if len(fields["description"]) > 1024:
        length_errors.append("Skill description exceeds 1024 characters")
    if length_errors:
        raise ValueError(f"{' and '.join(length_errors)}: {skill_file}")
    return fields


def _yaml_string(value: str, key: str, skill_file: Path) -> str:
    value = value.strip()
    if not value:
        return ""
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as error:
            raise ValueError(f"Malformed double-quoted YAML {key} in {skill_file}") from error
        if not isinstance(parsed, str):
            raise ValueError(f"YAML {key} must be a string scalar in {skill_file}")
        return parsed
    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            raise ValueError(f"Malformed single-quoted YAML {key} in {skill_file}")
        inner = value[1:-1]
        if re.search(r"(?<!')'(?!')", inner):
            raise ValueError(f"Malformed single-quoted YAML {key} in {skill_file}")
        return inner.replace("''", "'")

    # This parser intentionally supports plain string scalars, not YAML collections,
    # aliases, tags, block strings, or implicitly typed values.
    scalar = re.sub(r"\s+#.*$", "", value).rstrip()
    if not scalar:
        return ""
    if scalar[0] in "[{&*!|>" or re.search(r":\s", scalar):
        raise ValueError(f"Unsupported YAML {key}; use a string scalar in {skill_file}")
    if scalar.lower() in {"null", "~", "true", "false"} or re.fullmatch(r"[-+]?\d+(?:\.\d+)?", scalar):
        raise ValueError(f"YAML {key} must be a string scalar in {skill_file}")
    return scalar


def _assert_manifest_within(manifest: Path, directory: Path, label: str) -> Path:
    resolved = manifest.resolve()
    try:
        resolved.relative_to(directory.resolve())
    except ValueError as error:
        raise ValueError(f"{label} resolves outside its skill directory: {manifest}") from error
    return resolved


def _mask_code(text: str) -> str:
    characters = list(text)
    fence: tuple[str, int] | None = None
    offset = 0
    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        opening = FENCE_OPEN.match(content)
        if fence is not None:
            marker, minimum = fence
            closing = re.match(rf"^[ \t]{{0,3}}{re.escape(marker)}{{{minimum},}}[ \t]*$", content)
            if closing:
                fence = None
            for index in range(offset, offset + len(line)):
                if characters[index] not in "\r\n":
                    characters[index] = " "
        elif opening:
            run = opening.group(1)
            fence = (run[0], len(run))
            for index in range(offset, offset + len(line)):
                if characters[index] not in "\r\n":
                    characters[index] = " "
        offset += len(line)
    masked = "".join(characters)
    characters = list(masked)
    for match in INLINE_CODE.finditer(masked):
        for index in range(match.start(), match.end()):
            if characters[index] not in "\r\n":
                characters[index] = " "
    return "".join(characters)


def _markdown_targets(text: str) -> list[str]:
    visible = _mask_code(text)
    targets = [match.group(3).strip("<>") for match in MARKDOWN_LINK.finditer(visible)]
    targets.extend(
        match.group(2).strip("<>") for match in REFERENCE_DEFINITION.finditer(visible)
    )
    return targets


def _ensure_output_subdirectory(output_root: Path, name: str) -> Path:
    output_root = output_root.resolve()
    candidate = output_root / name
    if candidate.exists() or candidate.is_symlink():
        resolved = candidate.resolve()
        try:
            resolved.relative_to(output_root)
        except ValueError as error:
            raise ValueError(f"Output directory resolves outside output root: {candidate}") from error
        if not resolved.is_dir():
            raise ValueError(f"Output path is not a directory: {candidate}")
        return resolved
    candidate.mkdir(parents=True, exist_ok=True)
    resolved = candidate.resolve()
    try:
        resolved.relative_to(output_root)
    except ValueError as error:
        raise ValueError(f"Output directory resolves outside output root: {candidate}") from error
    return resolved


def discover_skills(root: Path) -> list[dict[str, str]]:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"Skills directory does not exist: {root}")
    results: list[dict[str, str]] = []
    names: set[str] = set()
    for directory in sorted(root.iterdir()):
        manifest = directory / "SKILL.md"
        if not directory.is_dir() or not manifest.is_file():
            continue
        try:
            directory.resolve().relative_to(root)
        except ValueError as error:
            raise ValueError(f"Skill directory resolves outside skills root: {directory}") from error
        _assert_manifest_within(manifest, directory, "Skill manifest")
        fields = _frontmatter(manifest)
        name = fields["name"]
        if not SKILL_NAME.fullmatch(name) or name != directory.name:
            raise ValueError(
                f"Invalid skill name {name!r}; it must match directory {directory.name!r} "
                "and use lowercase letters, digits, and single hyphens"
            )
        if name in names:
            raise ValueError(f"Duplicate skill name: {name}")
        names.add(name)
        results.append({"name": name, "description": fields["description"]})
    return results


def collect_dependencies(root: Path, skill_dir: Path) -> list[Path]:
    root = root.resolve()
    skill_dir = skill_dir.resolve()
    try:
        skill_relative = skill_dir.relative_to(root / "skills")
    except ValueError as error:
        raise ValueError(f"Skill directory must be beneath {root / 'skills'}") from error
    if len(skill_relative.parts) != 1 or not SKILL_NAME.fullmatch(skill_relative.name):
        raise ValueError(f"Invalid skill directory: {skill_dir}")
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        raise ValueError(f"Skill manifest is missing: {skill_file}")

    allowed_roots = [skill_dir] + [root / area for area in SOURCE_AREAS]
    pending = [skill_file.resolve()]
    found: list[Path] = []
    seen: set[Path] = set()
    while pending:
        current = pending.pop()
        try:
            current.relative_to(root)
        except ValueError as error:
            raise ValueError(f"Local resource resolves outside repository: {current}") from error
        if current in seen:
            continue
        if not current.is_file():
            raise ValueError(f"Local Markdown resource does not exist: {current}")
        if current.suffix.lower() != ".md":
            raise ValueError(f"Unsupported local resource type: {current}")
        try:
            current.relative_to(skill_dir)
            allowed = True
        except ValueError:
            allowed = False
        if not allowed:
            for allowed_root in allowed_roots[1:]:
                try:
                    current.relative_to(allowed_root.resolve())
                    allowed = True
                    break
                except ValueError:
                    continue
        if not allowed:
            raise ValueError(f"Local resource is outside permitted source areas: {current}")
        seen.add(current)
        found.append(current)

        content = current.read_text(encoding="utf-8")
        for target in _markdown_targets(content):
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("//") or not parsed.path:
                continue
            relative_path = Path(unquote(parsed.path))
            if relative_path.is_absolute():
                raise ValueError(f"Absolute local Markdown link is not allowed: {target}")
            if relative_path.suffix.lower() != ".md":
                raise ValueError(f"Unsupported local resource type: {target}")
            linked = (current.parent / relative_path).resolve()
            try:
                linked.relative_to(root)
            except ValueError as error:
                raise ValueError(f"Local resource link escapes repository: {target}") from error
            if not linked.is_file():
                raise ValueError(f"Broken local Markdown link {target!r} in {current}")
            pending.append(linked)
    return found


def _bundle_path_for_source(root: Path, skill_dir: Path, source: Path) -> Path:
    if source == skill_dir / "SKILL.md":
        return Path("SKILL.md")
    relative = source.relative_to(root)
    if relative.parts[0] == "skills":
        return Path("references") / "skills" / relative.parts[1] / Path(*relative.parts[2:])
    return Path("references") / relative.parts[0] / Path(*relative.parts[1:])


def _rewrite_markdown(
    content: str,
    source_file: Path,
    bundle_file: Path,
    source_to_bundle: dict[Path, Path],
) -> str:
    visible = _mask_code(content)
    edits: list[tuple[int, int, str]] = []

    def rewrite_target(raw_target: str) -> str:
        target = raw_target.strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or target.startswith("//") or not parsed.path:
            return raw_target
        source_target = (source_file.parent / unquote(parsed.path)).resolve()
        if source_target not in source_to_bundle:
            raise ValueError(f"Local Markdown dependency was not collected: {target}")
        bundle_target = source_to_bundle[source_target]
        relative = posixpath.relpath(
            bundle_target.as_posix(), start=bundle_file.parent.as_posix()
        )
        rewritten = quote(relative, safe="/.-_~")
        if parsed.query:
            rewritten += f"?{parsed.query}"
        if parsed.fragment:
            rewritten += f"#{parsed.fragment}"
        if raw_target.startswith("<") and raw_target.endswith(">"):
            rewritten = f"<{rewritten}>"
        return rewritten

    for match in MARKDOWN_LINK.finditer(visible):
        replacement = (
            f"{match.group(1)}[{match.group(2)}]("
            f"{rewrite_target(match.group(3))}{match.group(4)})"
        )
        edits.append((match.start(), match.end(), replacement))
    for match in REFERENCE_DEFINITION.finditer(visible):
        replacement = f"{match.group(1)}{rewrite_target(match.group(2))}{match.group(3)}"
        edits.append((match.start(), match.end(), replacement))
    for start, end, replacement in sorted(edits, reverse=True):
        content = content[:start] + replacement + content[end:]
    return content


def build_bundle(root: Path, skill_name: str, output_root: Path) -> Path:
    root = root.resolve()
    if not SKILL_NAME.fullmatch(skill_name):
        raise ValueError(f"Invalid skill name: {skill_name!r}")
    skills = discover_skills(root / "skills")
    if skill_name not in {skill["name"] for skill in skills}:
        raise ValueError(f"Unknown skill: {skill_name}")
    skill_dir = root / "skills" / skill_name
    dependencies = collect_dependencies(root, skill_dir)
    source_to_bundle = {
        source: _bundle_path_for_source(root, skill_dir, source) for source in dependencies
    }
    license_file = root / "LICENSE"
    if not license_file.is_file():
        raise ValueError(f"Repository LICENSE is missing: {license_file}")
    source_to_bundle[license_file.resolve()] = Path("LICENSE")
    output_root = output_root.resolve()
    skills_root = _ensure_output_subdirectory(output_root, "skills")
    destination = skills_root / skill_name
    if destination.exists() or destination.is_symlink():
        raise ValueError(f"Bundle destination already exists: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging_parent = Path(tempfile.mkdtemp(prefix=f".{skill_name}-", dir=destination.parent))
    staging = staging_parent / skill_name
    staging.mkdir()
    try:
        for source, relative in source_to_bundle.items():
            target = staging / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if relative == Path("LICENSE"):
                shutil.copyfile(source, target)
                continue
            content = source.read_text(encoding="utf-8")
            target.write_text(
                _rewrite_markdown(content, source, relative, source_to_bundle), encoding="utf-8"
            )
        errors = validate_bundle(staging)
        if errors:
            raise ValueError("Generated bundle is invalid: " + "; ".join(errors))
        os.replace(staging, destination)
    except Exception:
        shutil.rmtree(staging_parent, ignore_errors=True)
        raise
    shutil.rmtree(staging_parent, ignore_errors=True)
    return destination


def validate_bundle(bundle: Path) -> list[str]:
    bundle = bundle.resolve()
    errors: list[str] = []
    if not bundle.is_dir():
        return [f"Bundle directory does not exist: {bundle}"]
    manifests = [path for path in bundle.rglob("SKILL.md") if path.is_file()]
    if len(manifests) != 1 or manifests[0] != bundle / "SKILL.md":
        errors.append("Bundle must contain exactly one root SKILL.md manifest")
    for path in bundle.rglob("*"):
        if path.is_symlink():
            errors.append(f"Bundle must not contain symlinks: {path.relative_to(bundle)}")
    manifest = bundle / "SKILL.md"
    if not manifest.is_symlink() and manifest.is_file():
        try:
            fields = _frontmatter(manifest)
            name = fields["name"]
            if not SKILL_NAME.fullmatch(name) or name != bundle.name:
                errors.append(
                    f"Bundle name {name!r} must be valid and match directory {bundle.name!r}"
                )
        except (OSError, UnicodeError, ValueError) as error:
            errors.append(str(error))
    for markdown in sorted(path for path in bundle.rglob("*") if path.suffix.lower() == ".md"):
        if markdown.is_symlink():
            continue
        try:
            text = markdown.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            errors.append(f"Cannot read bundle resource {markdown.relative_to(bundle)}: {error}")
            continue
        for target in _markdown_targets(text):
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("//") or not parsed.path:
                continue
            relative = Path(unquote(parsed.path))
            if relative.is_absolute() or relative.suffix.lower() != ".md":
                errors.append(f"Unsupported or absolute bundle link {target!r} in {markdown.relative_to(bundle)}")
                continue
            resolved = (markdown.parent / relative).resolve()
            try:
                resolved.relative_to(bundle)
            except ValueError:
                errors.append(f"Bundle link escapes skill directory: {target!r}")
                continue
            if not resolved.is_file():
                errors.append(f"Broken bundle link {target!r} in {markdown.relative_to(bundle)}")
    return errors


def create_zip(bundle: Path, zip_path: Path) -> Path:
    bundle = bundle.resolve()
    errors = validate_bundle(bundle)
    if errors:
        raise ValueError("Cannot zip invalid bundle: " + "; ".join(errors))
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists() or zip_path.is_symlink():
        raise ValueError(f"ZIP destination already exists: {zip_path}")
    zip_path = zip_path.absolute()
    with tempfile.TemporaryDirectory(prefix=f".{zip_path.name}-", dir=zip_path.parent) as temporary:
        temporary_zip = Path(temporary) / zip_path.name
        with zipfile.ZipFile(temporary_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for source in sorted(bundle.rglob("*")):
                if source.is_file():
                    relative = source.relative_to(bundle).as_posix()
                    archive.write(source, f"{bundle.name}/{relative}")
        os.replace(temporary_zip, zip_path)
    return zip_path


def _extract_zip_bundle(archive_path: Path, extraction_root: Path) -> Path:
    try:
        with zipfile.ZipFile(archive_path) as archive:
            infos = archive.infolist()
            roots: set[str] = set()
            seen: set[str] = set()
            members: list[tuple[zipfile.ZipInfo, tuple[str, ...]]] = []
            for info in infos:
                raw_name = info.filename
                if "\\" in raw_name or "\x00" in raw_name or ":" in raw_name:
                    raise ValueError(f"Unsafe ZIP member path: {raw_name!r}")
                raw_parts = raw_name.split("/")
                if raw_parts and raw_parts[-1] == "":
                    raw_parts.pop()
                if not raw_parts or any(part in {"", ".", ".."} for part in raw_parts):
                    raise ValueError(f"Unsafe ZIP member path: {raw_name!r}")
                pure_path = PurePosixPath(raw_name)
                if pure_path.is_absolute():
                    raise ValueError(f"Unsafe absolute ZIP member path: {raw_name!r}")
                mode = info.external_attr >> 16
                kind = stat.S_IFMT(mode)
                if kind == stat.S_IFLNK:
                    raise ValueError(f"ZIP symlink members are not allowed: {raw_name!r}")
                if kind not in {0, stat.S_IFREG, stat.S_IFDIR}:
                    raise ValueError(f"Unsupported ZIP member type: {raw_name!r}")
                normalized = "/".join(raw_parts)
                if normalized in seen:
                    raise ValueError(f"Duplicate ZIP member path: {raw_name!r}")
                seen.add(normalized)
                roots.add(raw_parts[0])
                members.append((info, tuple(raw_parts)))
            if len(roots) != 1:
                raise ValueError("ZIP must contain exactly one top-level skill directory")
            skill_name = next(iter(roots))
            if not SKILL_NAME.fullmatch(skill_name):
                raise ValueError(f"Invalid skill name in ZIP: {skill_name!r}")
            for info, parts in members:
                if parts[0] != skill_name:
                    raise ValueError("ZIP members must remain beneath one skill directory")
                target = extraction_root.joinpath(*parts)
                try:
                    target.resolve().relative_to(extraction_root.resolve())
                except ValueError as error:
                    raise ValueError(f"ZIP member escapes extraction directory: {info.filename!r}") from error
                if info.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with archive.open(info) as source, target.open("wb") as output:
                        shutil.copyfileobj(source, output)
    except zipfile.BadZipFile as error:
        raise ValueError(f"Invalid ZIP bundle: {archive_path}") from error
    return extraction_root / skill_name


def _install_directory(bundle: Path, destination: Path, replace: bool) -> Path:
    errors = validate_bundle(bundle)
    if errors:
        raise ValueError("Cannot install invalid bundle: " + "; ".join(errors))
    destination = destination.resolve()
    final = destination / bundle.name
    exists = final.exists() or final.is_symlink()
    if exists and not replace:
        raise ValueError(f"Skill already exists at destination: {final}")
    destination.mkdir(parents=True, exist_ok=True)
    staging_parent = Path(tempfile.mkdtemp(prefix=f".{bundle.name}-install-", dir=destination))
    staged = staging_parent / bundle.name
    backup = staging_parent / f"{bundle.name}.backup"
    try:
        shutil.copytree(bundle, staged)
        staged_errors = validate_bundle(staged)
        if staged_errors:
            raise ValueError("Staged installation is invalid: " + "; ".join(staged_errors))
        if exists:
            os.replace(final, backup)
        try:
            os.replace(staged, final)
        except Exception:
            if exists and (backup.exists() or backup.is_symlink()):
                os.replace(backup, final)
            raise
        if backup.exists() or backup.is_symlink():
            if backup.is_dir() and not backup.is_symlink():
                shutil.rmtree(backup)
            else:
                backup.unlink()
    finally:
        shutil.rmtree(staging_parent, ignore_errors=True)
    return final


def install_bundle(bundle: Path, destination: Path, replace: bool = False) -> Path:
    bundle = bundle.resolve()
    if bundle.is_dir():
        return _install_directory(bundle, destination, replace)
    if not bundle.is_file() or bundle.suffix.lower() != ".zip":
        raise ValueError(f"Bundle must be a directory or ZIP file: {bundle}")
    with tempfile.TemporaryDirectory(prefix="skill-install-") as temporary:
        extracted = _extract_zip_bundle(bundle, Path(temporary))
        errors = validate_bundle(extracted)
        if errors:
            raise ValueError("Cannot install invalid ZIP bundle: " + "; ".join(errors))
        return _install_directory(extracted, destination, replace)


def main(argv: list[str] | None = None) -> int:
    repository = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Package, inspect, and install research skills.")
    commands = parser.add_subparsers(dest="command", required=True)

    list_parser = commands.add_parser("list", help="List skill metadata present on disk")
    list_parser.add_argument("--path", type=Path, default=repository / "skills")

    package_parser = commands.add_parser("package", help="Generate standalone skill bundles")
    selection = package_parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--skill", metavar="NAME")
    selection.add_argument("--all", action="store_true")
    package_parser.add_argument("--output", type=Path, default=repository / "dist")
    package_parser.add_argument("--zip", action="store_true", help="Also create one ZIP per bundle")

    validate_parser = commands.add_parser("validate", help="Validate a standalone skill directory")
    validate_parser.add_argument("bundle", type=Path)

    install_parser = commands.add_parser("install", help="Install a bundle under an explicit skill root")
    install_parser.add_argument("bundle", type=Path)
    install_parser.add_argument("--destination", type=Path, required=True)
    install_parser.add_argument("--replace", action="store_true", help="Replace an existing same-name skill")

    args = parser.parse_args(argv)
    try:
        if args.command == "list":
            for skill in discover_skills(args.path):
                print(f"{skill['name']}\t{skill['description']}")
            return 0
        if args.command == "package":
            skills = discover_skills(repository / "skills")
            names = [skill["name"] for skill in skills] if args.all else [args.skill]
            available = {skill["name"] for skill in skills}
            if any(name not in available for name in names):
                raise ValueError(f"Unknown skill: {next(name for name in names if name not in available)}")
            output_root = args.output.resolve()
            zip_root = _ensure_output_subdirectory(output_root, "zips") if args.zip else None
            for name in names:
                bundle = build_bundle(repository, name, output_root)
                print(bundle)
                if args.zip:
                    archive = create_zip(bundle, zip_root / f"{name}.zip")
                    print(archive)
            return 0
        if args.command == "validate":
            errors = validate_bundle(args.bundle)
            if errors:
                for error in errors:
                    print(error, file=sys.stderr)
                return 1
            print(f"Valid bundle: {args.bundle}")
            return 0
        if args.command == "install":
            installed = install_bundle(args.bundle, args.destination, replace=args.replace)
            print(installed)
            return 0
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
