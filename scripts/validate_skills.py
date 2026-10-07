#!/usr/bin/env python3
"""Run isolated skill cases and rubric scoring with the Codex CLI."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


CASE_HEADING = re.compile(r"^## ([A-Z]\d)\b.*$", re.MULTILINE)
PROMPT_FIELD = re.compile(
    r"^\*\*Synthetic prompt(?: \(([^)]+)\))?:\*\*(.*?)(?=^\*\*|\Z)",
    re.MULTILINE | re.DOTALL,
)
CRITERIA_FIELD = re.compile(
    r"^\*\*Scoring criteria:\*\*\s*$(.*)", re.MULTILINE | re.DOTALL
)
CRITERION = re.compile(r"^- \[([A-Z]\d\.\d+)\] (.+)$", re.MULTILINE)
LINK = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
SCORE_STATUSES = {"PASS", "FAIL", "INCONCLUSIVE"}


def markdown_files(root: Path, source: Path) -> list[Path]:
    """Return the local Markdown resources linked from a skill, recursively."""
    found: list[Path] = []
    pending = [source]
    seen: set[Path] = set()
    while pending:
        current = pending.pop()
        if current in seen or not current.is_file():
            continue
        seen.add(current)
        found.append(current)
        if current.suffix.lower() != ".md":
            continue
        for _, target in LINK.findall(current.read_text(encoding="utf-8")):
            target = target.split()[0].strip("<>")
            if not target or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("//"):
                continue
            path, _, _ = target.partition("#")
            linked = (current.parent / path).resolve() if path else current
            try:
                linked.relative_to(root.resolve())
            except ValueError:
                continue
            if linked.is_file() and linked.suffix.lower() == ".md":
                pending.append(linked)
    return found


def _materialize_prompt(root: Path, body: str) -> tuple[str, dict[str, str]]:
    artifacts: dict[str, str] = {}

    def replace_link(match: re.Match[str]) -> str:
        label, target = match.groups()
        target = target.split()[0].strip("<>")
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("//"):
            return label
        path, _, _ = target.partition("#")
        if not path:
            return label
        artifact = (root / "docs/validation" / path).resolve()
        try:
            artifact.relative_to(root.resolve())
        except ValueError:
            return label
        if not artifact.is_file():
            raise ValueError(f"Case input is missing: {target}")
        if artifact.suffix.lower() not in {".md", ".tex", ".txt", ".csv", ".json"}:
            raise ValueError(f"Unsupported case input type: {target}")
        content = artifact.read_text(encoding="utf-8")
        artifacts[artifact.relative_to(root).as_posix()] = content
        return label

    task = LINK.sub(replace_link, body).strip()
    blocks = [
        "You are working in a fresh, isolated evaluation context. Apply the supplied repository skill to the user's request. The evaluation rubric is intentionally not included.",
        "## User request",
        task,
    ]
    for name, content in artifacts.items():
        blocks.extend([f"## Supplied input: {name}", "```text", content.rstrip(), "```"])
    return "\n\n".join(blocks) + "\n", artifacts


def load_cases(root: Path) -> list[dict[str, object]]:
    source = root / "docs/validation/research-skills-cases.md"
    text = source.read_text(encoding="utf-8")
    matches = list(CASE_HEADING.finditer(text))
    cases: list[dict[str, object]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section = text[match.end() : end]
        prompt_matches = list(PROMPT_FIELD.finditer(section))
        criteria_match = CRITERIA_FIELD.search(section)
        if not prompt_matches or not criteria_match:
            raise ValueError(f"Case {match.group(1)} needs a prompt and scoring criteria")
        criteria = [
            {"id": criterion_id, "text": criterion_text.strip()}
            for criterion_id, criterion_text in CRITERION.findall(criteria_match.group(1))
        ]
        if not criteria:
            raise ValueError(f"Case {match.group(1)} has no scoring criteria")
        case_id = match.group(1)
        skill_names = {
            "E1": ["experiment-designer"],
            "E2": ["experiment-designer"],
            "R1": ["reproducibility-auditor"],
            "X1": ["experiment-designer", "result-analyzer"],
            "L1": ["latex-paper-writer"],
            "C1": ["citation-verifier", "result-analyzer"],
        }[case_id]
        skill_paths = [root / "skills" / name / "SKILL.md" for name in skill_names]
        resources = []
        for skill_path in skill_paths:
            resources.extend(markdown_files(root, skill_path))
        resources = list(dict.fromkeys(resources))
        context = []
        for resource in resources:
            context.extend(
                [
                    f"## Repository skill/resource: {resource.relative_to(root).as_posix()}",
                    resource.read_text(encoding="utf-8").rstrip(),
                ]
            )
        stages = []
        for stage_index, prompt_match in enumerate(prompt_matches, start=1):
            label, body = prompt_match.groups()
            prompt, artifacts = _materialize_prompt(root, body)
            stages.append(
                {
                    "id": f"{case_id}-{stage_index}" if len(prompt_matches) > 1 else case_id,
                    "label": label or "main",
                    "prompt": prompt,
                    "artifacts": artifacts,
                }
            )
        cases.append(
            {
                "id": case_id,
                "skills": skill_names,
                "skill": ", ".join(skill_names),
                "criteria": criteria,
                "prompt": "\n\n".join(context),
                "stages": [
                    {
                        **stage,
                        "prompt": "\n\n".join(context) + "\n\n" + stage["prompt"],
                    }
                    for stage in stages
                ],
                "source": source.relative_to(root).as_posix(),
                "skill_sha256": {
                    name: hashlib.sha256(path.read_bytes()).hexdigest()
                    for name, path in zip(skill_names, skill_paths)
                },
                "resources": [resource.relative_to(root).as_posix() for resource in resources],
            }
        )
    if [case["id"] for case in cases] != ["E1", "E2", "R1", "X1", "L1", "C1"]:
        raise ValueError("Expected the six existing cases in E1, E2, R1, X1, L1, C1 order")
    return cases


def validate_score_record(case: dict[str, object], record: dict[str, object]) -> None:
    scores = record.get("scores")
    if not isinstance(scores, list):
        raise ValueError("Score record must contain a scores list")
    expected = {criterion["id"] for criterion in case["criteria"]}
    actual: set[str] = set()
    for score in scores:
        if not isinstance(score, dict):
            raise ValueError("Each score must be an object")
        criterion_id = score.get("criterion")
        status = score.get("status")
        evidence = score.get("evidence")
        if criterion_id not in expected:
            raise ValueError(f"Unknown criterion: {criterion_id}")
        if criterion_id in actual:
            raise ValueError(f"Duplicate criterion: {criterion_id}")
        if status not in SCORE_STATUSES:
            raise ValueError(f"Invalid status for {criterion_id}: {status}")
        if not isinstance(evidence, str) or not evidence.strip():
            raise ValueError(f"Evidence is required for {criterion_id}")
        actual.add(criterion_id)
    missing = expected - actual
    if missing:
        raise ValueError(f"Missing criteria: {', '.join(sorted(missing))}")


def run_codex(prompt: str, artifacts: dict[str, str], output_path: Path, timeout: int) -> int:
    executable = shutil.which("codex")
    if not executable:
        return 127
    with tempfile.TemporaryDirectory(prefix="research-skills-eval-") as scratch:
        scratch_path = Path(scratch)
        for relative, content in artifacts.items():
            destination = scratch_path / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding="utf-8")
        command = [
            executable,
            "exec",
            "--ephemeral",
            "--ignore-user-config",
            "--skip-git-repo-check",
            "--sandbox",
            "workspace-write",
            "--color",
            "never",
            "--output-last-message",
            str(output_path),
            "-C",
            scratch,
            "-",
        ]
        completed = subprocess.run(
            command,
            input=prompt,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
    return completed.returncode


def score_prompt(case: dict[str, object], responses: list[tuple[str, str]]) -> str:
    rubric = "\n".join(f"- {c['id']}: {c['text']}" for c in case["criteria"])
    observed = "\n\n".join(
        f"## Response stage: {label}\n<response>\n{response}\n</response>"
        for label, response in responses
    )
    return f"""You are an independent rubric scorer in a fresh context. Score only what the response demonstrates. Do not infer missing behavior. Use PASS only when the response clearly satisfies the criterion, FAIL when it clearly violates or omits it, and INCONCLUSIVE when the response does not provide enough evidence either way. For every score, quote a short exact excerpt from the response; if no excerpt exists, quote `No supporting excerpt.` and explain in the evidence field. Return only the required JSON object.

Case: {case['id']}
Target skills: {case['skill']}

Criteria:
{rubric}

Observed response(s):
{observed}
"""


def score_schema(case: dict[str, object]) -> dict[str, object]:
    ids = [criterion["id"] for criterion in case["criteria"]]
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["scores"],
        "properties": {
            "scores": {
                "type": "array",
                "minItems": len(ids),
                "maxItems": len(ids),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["criterion", "status", "evidence"],
                    "properties": {
                        "criterion": {"type": "string", "enum": ids},
                        "status": {"type": "string", "enum": sorted(SCORE_STATUSES)},
                        "evidence": {"type": "string", "minLength": 1},
                    },
                },
            }
        },
    }


def invoke_coder(prompt: str, output_path: Path, schema_path: Path, timeout: int) -> int:
    executable = shutil.which("codex")
    if not executable:
        return 127
    with tempfile.TemporaryDirectory(prefix="research-skills-score-") as scratch:
        command = [
            executable,
            "exec",
            "--ephemeral",
            "--ignore-user-config",
            "--skip-git-repo-check",
            "--sandbox",
            "read-only",
            "--color",
            "never",
            "--output-schema",
            str(schema_path),
            "--output-last-message",
            str(output_path),
            "-C",
            scratch,
            "-",
        ]
        completed = subprocess.run(
            command,
            input=prompt,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
    return completed.returncode


def run_cases(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    cases = load_cases(root)
    selected = [case for case in cases if not args.case or case["id"] in args.case]
    if args.case and {case["id"] for case in selected} != set(args.case):
        raise ValueError("Unknown case ID supplied")
    run_dir = Path(args.output).resolve()
    run_dir.mkdir(parents=True, exist_ok=False)
    record: dict[str, object] = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "runner": "codex exec --ephemeral",
        "scorer": "codex exec --ephemeral (separate process per case)",
        "cases": [],
    }
    failures = 0
    for case in selected:
        case_id = case["id"]
        print(f"Running {case_id} with {case['skill']}…", flush=True)
        response_stages: list[tuple[str, str]] = []
        stage_items = []
        run_codes = []
        for stage in case["stages"]:
            stage_id = stage["id"]
            response_path = run_dir / f"{stage_id}.response.md"
            run_code = run_codex(
                stage["prompt"], stage["artifacts"], response_path, args.timeout
            )
            run_codes.append(run_code)
            stage_item = {
                "id": stage_id,
                "label": stage["label"],
                "runner_exit_code": run_code,
                "response_file": response_path.name if response_path.exists() else None,
            }
            stage_items.append(stage_item)
            if run_code == 0 and response_path.is_file() and response_path.read_text(encoding="utf-8").strip():
                response_stages.append((stage["label"], response_path.read_text(encoding="utf-8")))
        run_code = next((code for code in run_codes if code != 0), 0)
        item: dict[str, object] = {
            "id": case_id,
            "skills": case["skills"],
            "skill_sha256": case["skill_sha256"],
            "resources": case["resources"],
            "runner_exit_code": run_code,
            "stages": stage_items,
        }
        if run_code != 0 or len(response_stages) != len(case["stages"]):
            item["status"] = "NOT RUN" if run_code == 127 else "RUNNER ERROR"
            failures += 1
            record["cases"].append(item)
            print(f"  {item['status']}", flush=True)
            continue
        schema_path = run_dir / f"{case_id}.score-schema.json"
        schema_path.write_text(json.dumps(score_schema(case), indent=2), encoding="utf-8")
        score_path = run_dir / f"{case_id}.scores.json"
        print(f"Scoring {case_id} in a separate context…", flush=True)
        score_code = invoke_coder(
            score_prompt(case, response_stages),
            score_path,
            schema_path,
            args.timeout,
        )
        schema_path.unlink(missing_ok=True)
        item["scorer_exit_code"] = score_code
        item["score_file"] = score_path.name if score_path.exists() else None
        if score_code == 0 and score_path.is_file():
            try:
                score_record = json.loads(score_path.read_text(encoding="utf-8"))
                validate_score_record(case, score_record)
                item["scores"] = score_record["scores"]
                item["status"] = "SCORED"
            except (ValueError, json.JSONDecodeError) as error:
                item["status"] = "SCORING ERROR"
                item["scoring_error"] = str(error)
                failures += 1
        else:
            item["status"] = "SCORING ERROR"
            failures += 1
        record["cases"].append(item)
        print(f"  {item['status']}", flush=True)
    record["finished_at"] = datetime.now(timezone.utc).isoformat()
    (run_dir / "run.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Run record: {run_dir / 'run.json'}")
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=Path(__file__).resolve().parents[1], type=Path)
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run", help="run fresh skill and scoring contexts for the cases")
    run_parser.add_argument("--case", action="append", choices=["E1", "E2", "R1", "X1", "L1", "C1"])
    run_parser.add_argument("--output", required=True, help="new output directory for captured responses and scores")
    run_parser.add_argument("--timeout", type=int, default=300, help="timeout per runner or scorer process in seconds")
    run_parser.set_defaults(handler=run_cases)
    args = parser.parse_args(argv)
    try:
        return args.handler(args)
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
