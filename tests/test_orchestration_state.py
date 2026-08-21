"""Tests for optional compact state v2 and conservative v1 migration."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "templates/skills/orchestrator-work-protocol/scripts/state.py"
SCHEMA_PATH = ROOT / "templates/skills/orchestrator-work-protocol/references/state.schema.json"
SPEC = importlib.util.spec_from_file_location("orchestration_state", MODULE_PATH)
assert SPEC and SPEC.loader
state_module = importlib.util.module_from_spec(SPEC)
_previous_dont_write_bytecode = sys.dont_write_bytecode
sys.dont_write_bytecode = True
try:
    SPEC.loader.exec_module(state_module)
finally:
    sys.dont_write_bytecode = _previous_dont_write_bytecode


def batch(identifier: str = "core", **overrides):
    value = {
        "id": identifier,
        "objective": "Implement one coherent batch",
        "status": "PENDING",
        "dependencies": [],
        "owned_paths": ["src/core"],
        "assigned_context": None,
        "evidence_refs": [],
        "rework_count": 0,
    }
    value.update(overrides)
    return value


def ledger(*batches):
    return {
        "schema_version": 2,
        "workflow_id": "change-1",
        "route": "IMPLEMENTER_VERIFIER",
        "owner": "primary-thread",
        "next_gate": "DISPATCH_IMPLEMENTER",
        "batches": list(batches or (batch(),)),
    }


class OrchestrationStateTests(unittest.TestCase):
    def test_schema_is_strict_minimal_v2(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["schema_version"]["const"], 2)
        self.assertFalse(schema["additionalProperties"])
        self.assertFalse(schema["$defs"]["batch"]["additionalProperties"])

    def test_valid_state_and_dependency_readiness(self) -> None:
        first = batch("first", status="ACCEPTED")
        second = batch("second", status="READY", dependencies=["first"], owned_paths=["src/other"])
        self.assertEqual(state_module.validate_state(ledger(first, second))["schema_version"], 2)
        first["status"] = "IMPLEMENTED"
        with self.assertRaisesRegex(state_module.StateError, "non-ACCEPTED"):
            state_module.validate_state(ledger(first, second))

    def test_only_one_overlapping_writer_can_be_active(self) -> None:
        one = batch("one", status="IMPLEMENTING", assigned_context="agent-a")
        two = batch("two", status="IMPLEMENTING", assigned_context="agent-b", owned_paths=["src/core/file.py"])
        with self.assertRaisesRegex(state_module.StateError, "overlapping active writers"):
            state_module.validate_state(ledger(one, two))
        two["owned_paths"] = ["docs"]
        state_module.validate_state(ledger(one, two))

    def test_verifier_must_be_fresh_and_rework_is_bounded(self) -> None:
        item = batch(
            status="VERIFYING",
            assigned_context="implementer-a",
            evidence_refs=["implementer:implementer-a", "verifier:implementer-a"],
        )
        with self.assertRaisesRegex(state_module.StateError, "fresh Verifier"):
            state_module.validate_state(ledger(item))
        item["evidence_refs"][-1] = "verifier:verifier-b"
        state_module.validate_state(ledger(item))
        item["rework_count"] = 2
        with self.assertRaisesRegex(state_module.StateError, "one automatic rework"):
            state_module.validate_state(ledger(item))

    def test_atomic_write_checks_actual_previous(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "state.json"
            initial = ledger()
            state_module.write_state(path, initial)
            changed = copy.deepcopy(initial)
            changed["batches"][0]["status"] = "READY"
            state_module.write_state(path, changed, previous=initial)
            fabricated = copy.deepcopy(initial)
            with self.assertRaisesRegex(state_module.StateError, "does not match"):
                state_module.write_state(path, initial, previous=fabricated)

    def test_legacy_migration_preserves_only_unambiguous_claims(self) -> None:
        legacy = {
            "schema_version": 1,
            "owner": {"role": "Primary Orchestrator", "thread": "primary"},
            "items": [{
                "id": "done-item", "objective": "Done", "state": "DONE",
                "dependencies": [], "owned_paths": ["src"], "evidence_refs": ["tests:pass"],
                "rework_count": 0,
            }],
        }
        migrated = state_module.migrate_legacy_state(legacy, "legacy-change")
        self.assertEqual(migrated["schema_version"], 2)
        self.assertEqual(migrated["batches"][0]["status"], "RECONCILE")
        self.assertIn("legacy:preserved-claim", migrated["batches"][0]["evidence_refs"])

    def test_ambiguous_legacy_migration_blocks(self) -> None:
        with self.assertRaisesRegex(state_module.StateError, "BLOCKED"):
            state_module.migrate_legacy_state({"schema_version": 1, "items": "invalid"}, "legacy")


if __name__ == "__main__":
    unittest.main()
