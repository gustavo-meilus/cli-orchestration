#!/usr/bin/env python3
"""Run the matched release-2.0 A/B/C Codex field fixture."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "benchmarks/simple-add"
DEFAULT_OUTPUT = ROOT / "benchmarks/results/codex-0.148.0-2026-08-20.json"
ROUTES = {
    "A_DIRECT": (
        "Benchmark route A is explicitly selected as Direct execution for this isolated fixture. "
        "Do not create subagents. Inspect the fixture, make the smallest correction required by AGENTS.md, "
        "run python -m unittest -v, and return BENCH_A_DONE on success or BENCH_A_BLOCKED with the exact reason."
    ),
    "B_IMPLEMENTER_VERIFIER": (
        "Invoke $orchestrator-work-protocol. Benchmark route B explicitly requires Implementer followed by a fresh Verifier. "
        "The primary must remain a pure control plane and use built-in default subagents. Implement the smallest correction required "
        "by AGENTS.md and run its tests. Return BENCH_B_DONE only after fresh Verifier PASS; if any required worker is unavailable, "
        "fail closed and return BENCH_B_BLOCKED with the exact reason."
    ),
    "C_SCOUT_IMPLEMENTER_VERIFIER": (
        "Invoke $orchestrator-work-protocol. Benchmark route C explicitly requires Scout followed by Implementer and a fresh Verifier. "
        "The primary must remain a pure control plane and use built-in default subagents. The Scout must inspect scope/dependencies before "
        "implementation. Implement the smallest correction required by AGENTS.md and run its tests. Return BENCH_C_DONE only after fresh "
        "Verifier PASS; if any required worker is unavailable, fail closed and return BENCH_C_BLOCKED with the exact reason."
    ),
}


def file_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix not in {".pyc", ".pyo"}
        and not any(part.startswith(".") for part in path.relative_to(root).parts)
    }


def parse_events(output: str) -> tuple[list[dict[str, Any]], list[str]]:
    events, invalid = [], []
    for line in output.splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            if line.strip():
                invalid.append(line.strip())
            continue
        if isinstance(value, dict):
            events.append(value)
    return events, invalid


def command_text(event: dict[str, Any]) -> str:
    item = event.get("item")
    if not isinstance(item, dict):
        return ""
    for key in ("command", "cmd", "text"):
        value = item.get(key)
        if isinstance(value, str):
            return value
    return ""


def last_message(events: list[dict[str, Any]], fallback: str) -> str:
    candidates = []
    for event in events:
        item = event.get("item")
        if isinstance(item, dict) and item.get("type") in {"agent_message", "message"}:
            text = item.get("text")
            if isinstance(text, str):
                candidates.append(text)
    return (candidates[-1] if candidates else fallback[-1000:]).strip()[:1000]


def usage(events: list[dict[str, Any]]) -> dict[str, Any]:
    found = None
    for event in events:
        candidate = event.get("usage")
        if isinstance(candidate, dict):
            found = candidate
        result = event.get("result")
        if isinstance(result, dict) and isinstance(result.get("usage"), dict):
            found = result["usage"]
    if not found:
        return {"input_tokens": "unavailable", "output_tokens": "unavailable", "cached_input_tokens": "unavailable", "cost": "unavailable"}
    return {
        "input_tokens": found.get("input_tokens", "unavailable"),
        "output_tokens": found.get("output_tokens", "unavailable"),
        "cached_input_tokens": found.get("cached_input_tokens", "unavailable"),
        "cost": "unavailable",
    }


def run_route(codex: str, route: str, prompt: str, parent: Path) -> dict[str, Any]:
    work = parent / route.lower()
    shutil.copytree(FIXTURE, work)
    python = shutil.which("python") or "python"
    install = subprocess.run(
        [python, "-B", str(ROOT / "scripts/install.py"), "--scope", "project", "--project", str(work), "--tool", "codex"],
        text=True, capture_output=True, check=False,
    )
    if install.returncode:
        return {"route": route, "status": "BLOCKED", "blocker": "fixture installation failed", "install_stderr": install.stderr[-500:]}
    initial = file_hashes(work)
    started = time.perf_counter()
    try:
        run = subprocess.run(
            [codex, "exec", "--json", "--cd", str(work), "--skip-git-repo-check", "--ephemeral", "--sandbox", "danger-full-access", "--color", "never", prompt],
            stdin=subprocess.DEVNULL, text=True, capture_output=True, check=False, timeout=240,
            encoding="utf-8", errors="replace",
        )
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        run = subprocess.CompletedProcess(exc.cmd, 124, exc.stdout or "", exc.stderr or "timeout")
        timed_out = True
    elapsed = round(time.perf_counter() - started, 3)
    events, invalid = parse_events(run.stdout)
    started_items = [event for event in events if event.get("type") == "item.started" and isinstance(event.get("item"), dict)]
    commands = [text for event in started_items if (text := command_text(event))]
    assessment = subprocess.run(
        [python, "-B", "-m", "unittest", "-v"],
        cwd=work, text=True, capture_output=True, check=False,
    )
    final = file_hashes(work)
    changed = sorted(set(initial) | set(final))
    changed = [path for path in changed if initial.get(path) != final.get(path)]
    message = last_message(events, run.stdout + "\n" + run.stderr)
    blocked = "BLOCKED" in message.upper() or run.returncode not in (0,)
    read_commands = [command for command in commands if any(marker in command.lower() for marker in ("get-content", "type ", "cat ", "read"))]
    normalized_reads = [" ".join(command.split()) for command in read_commands]
    repeated_reads = len(normalized_reads) - len(set(normalized_reads))
    tool_events = [event for event in started_items if event["item"].get("type") not in {"agent_message", "message"}]
    agent_messages = [
        event["item"].get("text", "")
        for event in events
        if isinstance(event.get("item"), dict) and event["item"].get("type") in {"agent_message", "message"}
    ]
    rework_cycles = sum("VERDICT: REWORK" in message.upper() for message in agent_messages)
    return {
        "route": route,
        "status": "BLOCKED" if blocked else ("COMPLETED" if assessment.returncode == 0 else "FAILED"),
        "correctness_test_passed": assessment.returncode == 0,
        "elapsed_seconds": elapsed,
        "turns": sum(event.get("type") == "turn.completed" for event in events),
        "tool_calls": len(tool_events),
        "observable_test_runs": sum("unittest" in command.lower() for command in commands) + 1,
        "observable_repeated_file_reads": repeated_reads,
        "rework_cycles": rework_cycles,
        "changed_files": changed,
        "diff_churn_file_count": len(changed),
        "user_interventions": 0,
        "verifier_caught_defects": rework_cycles,
        "telemetry": usage(events),
        "process_exit_code": run.returncode,
        "timed_out": timed_out,
        "final_message_or_blocker": message,
        "unparsed_output_lines": invalid[:10],
        "assessment_excerpt": (assessment.stdout + assessment.stderr)[-1000:],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    codex = shutil.which("codex")
    if not codex:
        raise SystemExit("BLOCKED: codex CLI is unavailable")
    version = subprocess.run([codex, "--version"], text=True, capture_output=True, check=False).stdout.strip()
    with tempfile.TemporaryDirectory(prefix="cli-orchestration-routes-") as temporary:
        parent = Path(temporary)
        results = [run_route(codex, route, prompt, parent) for route, prompt in ROUTES.items()]
    payload = {
        "date": "2026-08-20",
        "fixture": "benchmarks/simple-add",
        "cli": version,
        "matched_initial_behavior": "add(2, 3) incorrectly returns -1; one unittest expects 5",
        "sandbox": "danger-full-access limited to automatically removed temporary fixture copies",
        "routes": results,
        "limitations": [
            "Cost telemetry is unavailable from codex exec JSONL.",
            "Repeated reads, test runs, tool calls, and verifier defects count only observable JSONL events.",
            "A BLOCKED orchestrated route is field evidence for worker availability, not correctness evidence for a completed topology.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
