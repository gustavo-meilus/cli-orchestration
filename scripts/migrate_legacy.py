#!/usr/bin/env python3
"""Preview or apply conservative migration from the six-role release."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

from install import PACKAGE_ROOT, TARGETS, configured_codex_home, resolve_targets, stamp


LEGACY_PROFILES = ("inspector.toml", "planner.toml", "executor.toml", "reviewer.toml", "validator.toml", "final-auditor.toml")
OWNERSHIP_MARKERS = ("orchestrator-work-protocol", "canonical Inspector role", "canonical Planner role", "canonical Executor role", "canonical Reviewer role", "canonical Validator role", "canonical Final Auditor role", "Legacy optional high-assurance")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", choices=("project", "user"), default="project")
    parser.add_argument("--project", type=Path)
    parser.add_argument("--tool", action="append", choices=tuple(TARGETS), default=None)
    parser.add_argument("--state", type=Path, help="Legacy v1 state path; defaults to <root>/.orchestration/state.json")
    parser.add_argument("--apply", action="store_true", help="Apply; default is dry-run")
    args = parser.parse_args()
    args.tools = list(dict.fromkeys(args.tool or ["codex"]))
    return args


def _load_state_module():
    path = PACKAGE_ROOT / "templates/skills/orchestrator-work-protocol/scripts/state.py"
    spec = importlib.util.spec_from_file_location("portable_state", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load state migration module")
    module = importlib.util.module_from_spec(spec)
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module


def _is_package_owned_profile(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return any(marker in text for marker in OWNERSHIP_MARKERS)


def _migrate_profiles(root: Path, scope: str, apply: bool) -> list[str]:
    codex_home = configured_codex_home(root) if scope == "user" else None
    _, _, tool_root, _ = resolve_targets("codex", scope, root, codex_home=codex_home)
    backup_root = root / ".orchestration" / f"legacy-backup-{stamp()}" / "codex-agents"
    actions = []
    for filename in LEGACY_PROFILES:
        source = tool_root / "agents" / filename
        if not source.exists():
            continue
        if not _is_package_owned_profile(source):
            actions.append(f"PRESERVE unrelated profile {source}")
            continue
        target = backup_root / filename
        actions.append(f"RELOCATE package-owned {source} -> {target}")
        if apply:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(target))
    return actions


def _migrate_state(path: Path, root: Path, apply: bool) -> list[str]:
    if not path.exists():
        return []
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"BLOCKED invalid legacy state {path}: {exc}; preserve it and repair or move it manually"]
    if raw.get("schema_version") == 2:
        return [f"PRESERVE current state v2 {path}"]
    module = _load_state_module()
    try:
        migrated = module.migrate_legacy_state(raw, path.parent.parent.name or "legacy-workflow")
    except module.StateError as exc:
        return [str(exc) + f"; original preserved at {path}"]
    destination = path.with_name("state.v2.json")
    backup = path.with_name(path.name + f".v1.bak-{stamp()}")
    actions = [f"BACKUP legacy state {path} -> {backup}", f"WRITE reconciliable state v2 -> {destination}"]
    if apply:
        shutil.copyfile(path, backup)
        module.write_state(destination, migrated)
    return actions


def main() -> int:
    args = parse_args()
    if args.scope == "user":
        if args.project:
            print("ERROR: --project is only valid for project scope", file=sys.stderr)
            return 2
        root = Path.home()
    else:
        root = (args.project or Path.cwd()).expanduser().resolve()
        if not root.is_dir():
            print(f"ERROR: project directory does not exist: {root}", file=sys.stderr)
            return 2
    state_path = args.state or root / ".orchestration/state.json"
    mode = "APPLY" if args.apply else "DRY RUN"
    print(f"Legacy migration {mode}: root={root}; tools={', '.join(args.tools)}")
    actions = []
    if "codex" in args.tools:
        actions.extend(_migrate_profiles(root, args.scope, args.apply))
    state_actions = _migrate_state(state_path, root, args.apply)
    actions.extend(state_actions)
    for action in actions:
        print(action)
    if any(action.startswith("BLOCKED") for action in actions):
        return 1
    command = [sys.executable, str(PACKAGE_ROOT / "scripts/install.py"), "--scope", args.scope]
    if args.scope == "project":
        command.extend(["--project", str(root)])
    for tool in args.tools:
        command.extend(["--tool", tool])
    if not args.apply:
        command.append("--dry-run")
    result = subprocess.run(command, text=True, check=False)
    if result.returncode:
        print("BLOCKED: adaptive installation failed; legacy files and backups remain recoverable", file=sys.stderr)
        return result.returncode
    print("Migration complete; fresh reconciliation is required before resuming migrated state.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
