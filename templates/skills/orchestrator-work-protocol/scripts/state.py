#!/usr/bin/env python3
"""Validate, atomically write, and conservatively migrate optional state v2."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path, PurePosixPath
import tempfile
from typing import Any


SCHEMA_VERSION = 2
ROUTES = {"READ_ONLY", "IMPLEMENTER_VERIFIER", "SCOUT_IMPLEMENTER_VERIFIER", "HIGH_ASSURANCE"}
STATUSES = {"PENDING", "RECONCILE", "READY", "IMPLEMENTING", "IMPLEMENTED", "VERIFYING", "REWORK", "ACCEPTED", "BLOCKED", "SUPERSEDED"}
ACTIVE_WRITES = {"IMPLEMENTING", "REWORK"}


class StateError(ValueError):
    """State violates the compact resumability contract."""


def validate_state(state: Any) -> dict[str, Any]:
    _object(state, "state", {"schema_version", "workflow_id", "route", "owner", "next_gate", "batches"})
    if state["schema_version"] != SCHEMA_VERSION or isinstance(state["schema_version"], bool):
        raise StateError("schema_version must be 2")
    for key in ("workflow_id", "owner", "next_gate"):
        _string(state[key], key, 512)
    if state["route"] not in ROUTES:
        raise StateError("route is invalid")
    if not isinstance(state["batches"], list):
        raise StateError("batches must be a list")
    ids: set[str] = set()
    for item in state["batches"]:
        _batch(item)
        if item["id"] in ids:
            raise StateError(f"duplicate batch id: {item['id']}")
        ids.add(item["id"])
    by_id = {item["id"]: item for item in state["batches"]}
    for item in state["batches"]:
        if item["id"] in item["dependencies"]:
            raise StateError(f"batch {item['id']} cannot depend on itself")
        missing = sorted(set(item["dependencies"]) - ids)
        if missing:
            raise StateError(f"batch {item['id']} has unknown dependencies: {missing}")
        if item["status"] == "READY":
            incomplete = [name for name in item["dependencies"] if by_id[name]["status"] != "ACCEPTED"]
            if incomplete:
                raise StateError(f"READY batch {item['id']} has non-ACCEPTED dependencies: {incomplete}")
        _freshness(item)
    _cycles(by_id)
    active = [item for item in state["batches"] if item["status"] in ACTIVE_WRITES]
    for index, first in enumerate(active):
        for second in active[index + 1:]:
            if _path_sets_overlap(first["owned_paths"], second["owned_paths"]):
                raise StateError(f"overlapping active writers: {first['id']} and {second['id']}")
    return state


def load_state(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise StateError(f"cannot load state {path}: {exc}") from exc
    return validate_state(data)


def write_state(path: Path, state: Any, previous: Any | None = None) -> None:
    validated = validate_state(state)
    if path.exists():
        actual = load_state(path)
        if previous is not None and previous != actual:
            raise StateError("provided previous state does not match persisted state")
    elif previous is not None:
        raise StateError("initial state creation cannot use previous state")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(validated, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def migrate_legacy_state(legacy: Any, workflow_id: str) -> dict[str, Any]:
    """Convert readable v1 claims to RECONCILE batches; never inherit acceptance."""
    try:
        if not isinstance(legacy, dict) or legacy.get("schema_version") != 1 or not isinstance(legacy.get("items"), list):
            raise StateError("legacy state has no valid v1 item list")
        batches = []
        for old in legacy["items"]:
            if not isinstance(old, dict):
                raise StateError("legacy item is not an object")
            identifier = old.get("id")
            objective = old.get("objective")
            dependencies = old.get("dependencies", [])
            owned_paths = old.get("owned_paths", [])
            evidence = old.get("evidence_refs", [])
            rework = old.get("rework_count", 0)
            _string(identifier, "legacy id", 128)
            _string(objective, "legacy objective", 1024)
            _strings(dependencies, "legacy dependencies", 128)
            _strings(owned_paths, "legacy owned_paths", 512)
            _strings(evidence, "legacy evidence_refs", 512)
            if isinstance(rework, bool) or not isinstance(rework, int) or rework < 0:
                raise StateError("legacy rework_count is invalid")
            batches.append({
                "id": identifier,
                "objective": objective,
                "status": "RECONCILE",
                "dependencies": dependencies,
                "owned_paths": owned_paths,
                "assigned_context": None,
                "evidence_refs": [*evidence, "legacy:preserved-claim"],
                "rework_count": min(rework, 1),
            })
        return validate_state({
            "schema_version": 2,
            "workflow_id": workflow_id,
            "route": "SCOUT_IMPLEMENTER_VERIFIER",
            "owner": "primary-orchestrator",
            "next_gate": "FRESH_RECONCILIATION",
            "batches": batches,
        })
    except StateError as exc:
        raise StateError(f"BLOCKED: legacy state cannot be migrated safely: {exc}") from exc


def _batch(item: Any) -> None:
    fields = {"id", "objective", "status", "dependencies", "owned_paths", "assigned_context", "evidence_refs", "rework_count"}
    _object(item, "batch", fields)
    _string(item["id"], "batch id", 128)
    _string(item["objective"], "batch objective", 1024)
    if item["status"] not in STATUSES:
        raise StateError("batch status is invalid")
    _strings(item["dependencies"], "dependencies", 128)
    _strings(item["owned_paths"], "owned_paths", 512)
    _strings(item["evidence_refs"], "evidence_refs", 512)
    if item["assigned_context"] is not None:
        _string(item["assigned_context"], "assigned_context", 512)
    if isinstance(item["rework_count"], bool) or not isinstance(item["rework_count"], int) or not 0 <= item["rework_count"] <= 1:
        raise StateError("only one automatic rework is permitted")


def _freshness(item: dict[str, Any]) -> None:
    if item["status"] != "VERIFYING":
        return
    implementers = {ref.split(":", 1)[1] for ref in item["evidence_refs"] if ref.startswith("implementer:")}
    verifiers = {ref.split(":", 1)[1] for ref in item["evidence_refs"] if ref.startswith("verifier:")}
    if implementers & verifiers:
        raise StateError(f"batch {item['id']} does not use a fresh Verifier")


def _cycles(by_id: dict[str, dict[str, Any]]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(identifier: str) -> None:
        if identifier in visiting:
            raise StateError(f"dependency cycle includes {identifier}")
        if identifier in visited:
            return
        visiting.add(identifier)
        for dependency in by_id[identifier]["dependencies"]:
            visit(dependency)
        visiting.remove(identifier)
        visited.add(identifier)
    for identifier in sorted(by_id):
        visit(identifier)


def _path_sets_overlap(first: list[str], second: list[str]) -> bool:
    normalized_first = [_parts(value) for value in first]
    normalized_second = [_parts(value) for value in second]
    return any(a == b or a[:len(b)] == b or b[:len(a)] == a for a in normalized_first for b in normalized_second)


def _parts(value: str) -> tuple[str, ...]:
    return tuple(part.casefold() for part in PurePosixPath(value.replace("\\", "/")).parts if part not in ("", "."))


def _object(value: Any, label: str, fields: set[str]) -> None:
    if not isinstance(value, dict) or set(value) != fields:
        raise StateError(f"{label} must contain exactly {sorted(fields)}")


def _string(value: Any, label: str, limit: int) -> None:
    if not isinstance(value, str) or not value or len(value) > limit:
        raise StateError(f"{label} must be a non-empty string of at most {limit} characters")


def _strings(value: Any, label: str, limit: int) -> None:
    if not isinstance(value, list):
        raise StateError(f"{label} must be a unique list")
    for item in value:
        _string(item, label, limit)
    if len(value) != len(set(value)):
        raise StateError(f"{label} must be a unique list")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path)
    parser.add_argument("--migrate-legacy", type=Path)
    parser.add_argument("--workflow-id")
    args = parser.parse_args()
    if args.migrate_legacy:
        if not args.workflow_id:
            parser.error("--workflow-id is required with --migrate-legacy")
        legacy = json.loads(args.state.read_text(encoding="utf-8"))
        migrated = migrate_legacy_state(legacy, args.workflow_id)
        write_state(args.migrate_legacy, migrated)
        print(f"PASS: migrated legacy claim for fresh reconciliation: {args.migrate_legacy}")
    else:
        load_state(args.state)
        print(f"PASS: valid optional v2 orchestration state: {args.state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
