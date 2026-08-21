#!/usr/bin/env python3
"""Verify a selected portable adaptive orchestration installation."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None

from install import BEGIN, END, NORMAL_AGENT_FILES, PACKAGE_ROOT, SKILLS, TOOLS, configured_codex_home, resolve_targets
from manifest import load_manifest


VERSION = (PACKAGE_ROOT / "VERSION").read_text(encoding="utf-8").strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", choices=("user", "project"), required=True)
    parser.add_argument("--tool", action="append", metavar="TOOL")
    parser.add_argument("--project", type=Path)
    parser.add_argument("--native-hardening", action="store_true")
    args = parser.parse_args()
    selected = args.tool or ["codex"]
    invalid = [tool for tool in selected if tool not in TOOLS]
    if invalid:
        parser.error(f"unsupported --tool {invalid[0]!r}")
    args.tools = list(dict.fromkeys(selected))
    if args.native_hardening and "codex" not in args.tools:
        parser.error(f"--native-hardening is not supported for tool {args.tools[0]}")
    return args


def check_skill(path: Path) -> list[str]:
    if not path.is_file():
        return [f"missing skill: {path}"]
    text = path.read_text(encoding="utf-8")
    errors = []
    if not text.startswith("---\n"):
        errors.append(f"missing YAML frontmatter: {path}")
    for field in ("name:", "description:"):
        if field not in text[:2000]:
            errors.append(f"missing {field[:-1]} metadata: {path}")
    return errors


def compare_owned_file(actual: Path, expected: Path, label: str) -> list[str]:
    if not actual.is_file():
        return [f"missing {label}: {actual}"]
    if actual.read_bytes() != expected.read_bytes():
        return [f"installed {label} differs from package template: {actual}"]
    return []


def compare_owned_tree(actual: Path, expected: Path, label: str) -> list[str]:
    errors: list[str] = []
    for source in sorted(path for path in expected.rglob("*") if path.is_file()):
        relative = source.relative_to(expected)
        if "__pycache__" in relative.parts or source.suffix in {".pyc", ".pyo"}:
            continue
        errors.extend(compare_owned_file(actual / relative, source, f"{label}/{relative.as_posix()}"))
    return errors


def main() -> int:
    args = parse_args()
    if args.scope == "user":
        if args.project:
            print("ERROR: --project is only valid with --scope project", file=sys.stderr)
            return 2
        root = Path.home()
    else:
        root = (args.project or Path.cwd()).expanduser().resolve()
        if not root.is_dir():
            print(f"ERROR: project directory does not exist: {root}", file=sys.stderr)
            return 2

    failures: list[str] = []
    warnings: list[str] = []
    manifest = load_manifest(PACKAGE_ROOT / "manifest.json")
    if manifest["version"] != VERSION:
        failures.append(f"manifest version {manifest['version']} differs from VERSION {VERSION}")

    record_path = root / ".orchestration/install.json"
    if not record_path.is_file():
        failures.append(f"missing installation record: {record_path}")
    else:
        try:
            record = json.loads(record_path.read_text(encoding="utf-8"))
            if record.get("version") != VERSION:
                failures.append(f"installation record version differs from {VERSION}")
            if record.get("tools") != args.tools:
                failures.append(f"installation record tools {record.get('tools')!r} differ from selection {args.tools!r}")
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"invalid installation record: {exc}")

    checked_instructions: set[Path] = set()
    for tool in args.tools:
        codex_home = configured_codex_home(root) if tool == "codex" and args.scope == "user" else None
        instruction, skills_root, tool_root, bridge = resolve_targets(tool, args.scope, root, codex_home=codex_home)
        if instruction not in checked_instructions:
            if not instruction.is_file():
                failures.append(f"missing instruction file: {instruction}")
            else:
                text = instruction.read_text(encoding="utf-8")
                if BEGIN not in text or END not in text:
                    failures.append(f"managed orchestration block missing from {instruction}")
            checked_instructions.add(instruction)
        adapter_path = tool_root / "orchestration-adapter.md"
        failures.extend(compare_owned_file(adapter_path, PACKAGE_ROOT / f"templates/adapters/{tool}.md", f"{tool} adapter"))
        if adapter_path.is_file():
            adapter_text = adapter_path.read_text(encoding="utf-8")
            expected_mapping = manifest["adapters"][tool]["generic_agent"]
            expected_entry = manifest["adapters"][tool]["explicit_entry"]
            if expected_mapping not in adapter_text:
                failures.append(f"{tool} adapter missing generic-agent mapping {expected_mapping!r}")
            if expected_entry not in adapter_text:
                failures.append(f"{tool} adapter missing explicit entry {expected_entry!r}")
        if bridge is not None:
            failures.extend(compare_owned_file(bridge, PACKAGE_ROOT / "templates/adapters/claude-bridge.md", "Claude bridge"))
        for skill in SKILLS:
            failures.extend(check_skill(skills_root / skill / "SKILL.md"))
            failures.extend(compare_owned_tree(skills_root / skill, PACKAGE_ROOT / "templates/skills" / skill, f"{skill} skill"))
        if tool == "codex":
            config = tool_root / "config.toml"
            if not config.is_file():
                failures.append(f"missing Codex config: {config}")
            elif tomllib is not None:
                try:
                    data = tomllib.loads(config.read_text(encoding="utf-8"))
                    agents = data.get("agents", {})
                    if agents.get("enabled") is not True:
                        failures.append("Codex agents.enabled must be true")
                    concurrency = agents.get("max_concurrent_threads_per_session")
                    if not isinstance(concurrency, int) or isinstance(concurrency, bool) or concurrency < 1:
                        failures.append("Codex concurrency setting must be a positive integer")
                except Exception as exc:
                    failures.append(f"invalid Codex config: {exc}")
            if args.native_hardening:
                for filename in NORMAL_AGENT_FILES:
                    profile = tool_root / "agents" / filename
                    if not profile.is_file():
                        failures.append(f"missing optional Codex profile: {profile}")
                    elif tomllib is not None:
                        try:
                            tomllib.loads(profile.read_text(encoding="utf-8"))
                        except Exception as exc:
                            failures.append(f"invalid Codex profile {profile}: {exc}")
                    failures.extend(compare_owned_file(profile, PACKAGE_ROOT / "templates/codex/agents" / filename, f"Codex profile {filename}"))

    if args.scope == "project" and (root / "openspec").exists():
        executable = shutil.which("openspec")
        if not executable:
            warnings.append("project contains openspec/ but openspec CLI is unavailable")
        else:
            result = subprocess.run([executable, "--version"], capture_output=True, text=True, check=False)
            if result.returncode not in (0, 1):
                warnings.append("OpenSpec version command failed")
        if not (root / ".agents/skills/openspec-apply-change/SKILL.md").exists():
            warnings.append("OpenSpec exists but canonical Codex OpenSpec skills were not detected")

    print(f"Portable adaptive orchestration {VERSION} installation check")
    print(f"Scope: {args.scope}; tools: {', '.join(args.tools)}")
    for item in failures:
        print(f"FAIL: {item}")
    for item in warnings:
        print(f"WARN: {item}")
    if failures:
        return 1
    print("PASS: selected adapters and portable core are installed and syntactically valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
