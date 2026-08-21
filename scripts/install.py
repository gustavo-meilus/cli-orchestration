#!/usr/bin/env python3
"""Install the portable adaptive orchestration release safely."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile
from dataclasses import dataclass


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = PACKAGE_ROOT / "templates"
VERSION = (PACKAGE_ROOT / "VERSION").read_text(encoding="utf-8").strip()
BEGIN = "<!-- BEGIN ORCHESTRATOR-STANDARD -->"
END = "<!-- END ORCHESTRATOR-STANDARD -->"
TOOLS = ("codex", "claude", "copilot")
NORMAL_AGENT_FILES = ("scout.toml", "implementer.toml", "verifier.toml")
SKILLS = ("orchestrator-work-protocol", "openspec-orchestrated-apply")


@dataclass(frozen=True)
class InstallTargets:
    instruction: Path
    skills: Path
    tool_root: Path
    bridge: Path | None = None


TARGETS: dict[str, dict[str, InstallTargets]] = {
    "codex": {
        "user": InstallTargets(Path(".codex/AGENTS.md"), Path(".agents/skills"), Path(".codex")),
        "project": InstallTargets(Path("AGENTS.md"), Path(".agents/skills"), Path(".codex")),
    },
    "claude": {
        "user": InstallTargets(Path(".claude/AGENTS.md"), Path(".claude/skills"), Path(".claude"), Path(".claude/CLAUDE.md")),
        "project": InstallTargets(Path("AGENTS.md"), Path(".claude/skills"), Path(".claude"), Path("CLAUDE.md")),
    },
    "copilot": {
        "user": InstallTargets(Path(".copilot/AGENTS.md"), Path(".copilot/skills"), Path(".copilot")),
        "project": InstallTargets(Path("AGENTS.md"), Path(".github/skills"), Path(".github")),
    },
}


def resolve_targets(tool: str, scope: str, root: Path, *, codex_home: Path | None = None) -> tuple[Path, Path, Path, Path | None]:
    targets = TARGETS[tool][scope]
    if tool == "codex" and scope == "user":
        tool_root = codex_home if codex_home is not None else root / targets.tool_root
        instruction_relative = targets.instruction.relative_to(targets.tool_root)
        return tool_root / instruction_relative, root / targets.skills, tool_root, None
    bridge = root / targets.bridge if targets.bridge is not None else None
    return root / targets.instruction, root / targets.skills, root / targets.tool_root, bridge


def configured_codex_home(home: Path) -> Path:
    configured = os.environ.get("CODEX_HOME")
    return Path(configured).expanduser() if configured else home / ".codex"


def stamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f")


def _make_writable(path: Path) -> None:
    if path.exists():
        path.chmod(path.stat().st_mode | stat.S_IWRITE | stat.S_IREAD)


def backup(path: Path, dry_run: bool) -> Path | None:
    if not path.exists():
        return None
    target = path.with_name(path.name + f".bak-{stamp()}")
    print(f"BACKUP {path} -> {target}")
    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    return target


def _atomic_write(dst: Path, data: bytes) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{dst.name}.", suffix=".tmp", dir=dst.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        _make_writable(dst)
        os.replace(temporary, dst)
        _make_writable(dst)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def write_owned_file(src: Path, dst: Path, dry_run: bool) -> None:
    data = src.read_bytes()
    if dst.exists() and dst.read_bytes() == data:
        print(f"OK     {dst}")
        return
    if dst.exists():
        backup(dst, dry_run)
    print(f"WRITE  {dst}")
    if not dry_run:
        _atomic_write(dst, data)


def write_owned_bytes(data: bytes, dst: Path, dry_run: bool) -> None:
    if dst.exists() and dst.read_bytes() == data:
        print(f"OK     {dst}")
        return
    if dst.exists():
        backup(dst, dry_run)
    print(f"WRITE  {dst}")
    if not dry_run:
        _atomic_write(dst, data)


def copy_owned_tree(src: Path, dst: Path, dry_run: bool) -> None:
    for source in sorted(path for path in src.rglob("*") if path.is_file()):
        relative = source.relative_to(src)
        if "__pycache__" in relative.parts or source.suffix in {".pyc", ".pyo"}:
            continue
        write_owned_file(source, dst / relative, dry_run)


def update_managed_block(path: Path, block_source: Path, dry_run: bool) -> None:
    block = block_source.read_text(encoding="utf-8").strip()
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if BEGIN in existing and END in existing:
        start = existing.index(BEGIN)
        end = existing.index(END, start) + len(END)
        updated = existing[:start] + block + existing[end:]
    else:
        prefix = existing.rstrip()
        updated = (prefix + "\n\n" if prefix else "") + block + "\n"
    if updated == existing:
        print(f"OK     {path}")
        return
    if path.exists():
        backup(path, dry_run)
    print(f"UPDATE {path} (managed block)")
    if not dry_run:
        _atomic_write(path, updated.encode("utf-8"))


def update_codex_config(path: Path, dry_run: bool) -> None:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    lines = text.splitlines()
    if "[agents]" not in text:
        if lines and lines[-1].strip():
            lines.append("")
        lines.extend(["# Added by portable adaptive orchestration", "[agents]", "enabled = true", "max_concurrent_threads_per_session = 3"])
    else:
        if "enabled" not in text:
            index = lines.index("[agents]") + 1
            lines.insert(index, "enabled = true  # portable adaptive orchestration")
        if "max_concurrent_threads_per_session" not in text:
            index = lines.index("[agents]") + 1
            lines.insert(index, "max_concurrent_threads_per_session = 3  # portable adaptive orchestration")
    updated = "\n".join(lines).rstrip() + "\n"
    if updated == text:
        print(f"OK     {path}")
        return
    if path.exists():
        backup(path, dry_run)
    print(f"UPDATE {path} ([agents] adaptive defaults)")
    if not dry_run:
        _atomic_write(path, updated.encode("utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", choices=("user", "project"), required=True)
    parser.add_argument("--tool", action="append", metavar="TOOL", help="Target CLI; repeat for multiple: codex, claude, copilot")
    parser.add_argument("--project", type=Path)
    parser.add_argument("--dry-run", action="store_true")
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

    tools_label = ", ".join(args.tools)
    selection_label = f"tool: {tools_label}" if len(args.tools) == 1 else f"tools: {tools_label}"
    print(f"Installing portable adaptive orchestration ({selection_label}; scope: {args.scope}){' [DRY RUN]' if args.dry_run else ''}")
    updated_instruction_paths: set[Path] = set()
    for tool in args.tools:
        codex_home = configured_codex_home(root) if tool == "codex" and args.scope == "user" else None
        instruction, skills_root, tool_root, bridge = resolve_targets(tool, args.scope, root, codex_home=codex_home)
        print(f"DESTINATION tool={tool} scope={args.scope} root={tool_root}")
        if instruction not in updated_instruction_paths:
            update_managed_block(instruction, TEMPLATES / "project/AGENTS.block.md", args.dry_run)
            updated_instruction_paths.add(instruction)
        if bridge is not None:
            write_owned_file(TEMPLATES / "adapters/claude-bridge.md", bridge, args.dry_run)
        write_owned_file(TEMPLATES / f"adapters/{tool}.md", tool_root / "orchestration-adapter.md", args.dry_run)
        for skill in SKILLS:
            copy_owned_tree(TEMPLATES / "skills" / skill, skills_root / skill, args.dry_run)
        if tool == "codex":
            update_codex_config(tool_root / "config.toml", args.dry_run)
            if args.native_hardening:
                for filename in NORMAL_AGENT_FILES:
                    write_owned_file(TEMPLATES / "codex/agents" / filename, tool_root / "agents" / filename, args.dry_run)

    install_record = {"package": "tacticswitch", "version": VERSION, "scope": args.scope, "tools": args.tools}
    write_owned_bytes((json.dumps(install_record, indent=2) + "\n").encode(), root / ".orchestration/install.json", args.dry_run)
    print("Installation complete. Run scripts/verify_install.py with the same --scope/--tool selection.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
