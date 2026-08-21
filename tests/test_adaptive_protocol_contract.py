"""Behavior contracts for the lean portable orchestration release."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "templates/skills/orchestrator-work-protocol/references/protocol.md"
PACKETS = ROOT / "templates/skills/orchestrator-work-protocol/references/control-packets.md"
POLICY = ROOT / "templates/project/AGENTS.block.md"
OPEN_SPEC = ROOT / "templates/skills/openspec-orchestrated-apply/SKILL.md"
STATE_SCHEMA = ROOT / "templates/skills/orchestrator-work-protocol/references/state.schema.json"
WORKFLOW = ROOT / "templates/skills/openspec-orchestrated-apply/references/workflow.md"


class AdaptiveProtocolContractTests(unittest.TestCase):
    def test_protocol_has_ordered_cumulative_route_precedence(self) -> None:
        text = PROTOCOL.read_text(encoding="utf-8")
        ordered = [
            "Explicit orchestration",
            "High risk",
            "Material uncertainty",
            "Material implementation",
            "Useful read-only parallelism",
            "Direct execution",
        ]
        positions = [text.index(label) for label in ordered]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("cumulative", text.lower())
        self.assertIn("does not manufacture an Implementer", text)

    def test_pure_boundary_starts_only_after_orchestration_is_selected(self) -> None:
        protocol = PROTOCOL.read_text(encoding="utf-8")
        policy = POLICY.read_text(encoding="utf-8")
        for text in (protocol, policy):
            self.assertIn("direct execution", text.lower())
            self.assertIn("pure control plane", text.lower())
            self.assertIn("Scout", text)

    def test_normal_roles_and_fresh_verifier_are_cli_neutral(self) -> None:
        protocol = PROTOCOL.read_text(encoding="utf-8")
        headings = [line for line in protocol.splitlines() if line.startswith("### Role: ")]
        self.assertEqual(headings, ["### Role: Scout", "### Role: Implementer", "### Role: Verifier"])
        self.assertIn("new context", protocol)
        self.assertIn("did not implement, edit, or own", protocol)
        self.assertIn("does not require a different model", protocol)
        self.assertNotIn("gpt-", protocol.lower())

    def test_packets_encode_affinity_dependencies_one_writer_and_compact_results(self) -> None:
        text = PACKETS.read_text(encoding="utf-8")
        for phrase in (
            "context-affinity",
            "dependencies",
            "owned paths",
            "one active writer",
            "Compact result packet",
            "same Implementer",
            "different fresh Verifier",
            "cause diagnosis",
        ):
            self.assertIn(phrase, text)

    def test_open_spec_bridge_is_thin_and_canonical(self) -> None:
        text = OPEN_SPEC.read_text(encoding="utf-8")
        self.assertIn("canonical `$openspec-apply-change`", text)
        self.assertIn("canonical `$openspec-verify-change`", text)
        self.assertIn("conformance evidence", text)
        self.assertIn("does not copy, replace, or shadow", text)
        self.assertNotIn("Validator PASS +", text)

    def test_acceptance_and_worker_unavailability_are_route_specific(self) -> None:
        text = PROTOCOL.read_text(encoding="utf-8")
        self.assertIn("Direct acceptance", text)
        self.assertIn("Orchestrated acceptance", text)
        self.assertIn("BLOCKED", text)
        self.assertIn("never silently falls back", text)

    def test_framework_authority_and_acceptance_ownership_are_distinct(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        order = [
            "latest explicit user requirement",
            "governing repository instructions",
            "approved OpenSpec change artifacts",
            "canonical specifications",
        ]
        positions = [text.index(item) for item in order]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("acceptance criteria", text)
        self.assertIn("acceptance decision", text)
        self.assertIn("same-level", text)

    def test_public_logical_entries_remain_stable(self) -> None:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        resources = set(manifest["canonical_resources"])
        self.assertIn("templates/skills/orchestrator-work-protocol", resources)
        self.assertIn("templates/skills/openspec-orchestrated-apply", resources)
        self.assertTrue((ROOT / "templates/skills/orchestrator-work-protocol/SKILL.md").exists())
        self.assertTrue((ROOT / "templates/skills/openspec-orchestrated-apply/SKILL.md").exists())

    def test_legacy_state_requires_preservation_and_reconciliation(self) -> None:
        state_doc = (ROOT / "templates/skills/orchestrator-work-protocol/references/state.md").read_text(encoding="utf-8")
        self.assertIn("preserve", state_doc.lower())
        self.assertIn("unambiguous", state_doc.lower())
        self.assertIn("fresh reconciliation", state_doc.lower())
        self.assertIn("BLOCKED", state_doc)

    def test_state_v2_is_optional_and_minimal(self) -> None:
        schema = json.loads(STATE_SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["schema_version"]["const"], 2)
        self.assertEqual(
            schema["required"],
            ["schema_version", "workflow_id", "route", "owner", "next_gate", "batches"],
        )
        item = schema["$defs"]["batch"]
        self.assertEqual(
            item["required"],
            ["id", "objective", "status", "dependencies", "owned_paths", "assigned_context", "evidence_refs", "rework_count"],
        )
        forbidden = {"transcript", "raw_logs", "specification_body", "planner_verdict", "auditor"}
        self.assertTrue(forbidden.isdisjoint(item["properties"]))

    def test_public_version_surface_is_aligned(self) -> None:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual((ROOT / "VERSION").read_text(encoding="utf-8").strip(), "2.0.0")
        self.assertEqual(manifest["version"], "2.0.0")
        self.assertIn("Release-Version: 2.0.0", PROTOCOL.read_text(encoding="utf-8"))

    def test_manifest_uses_exact_support_vocabulary(self) -> None:
        source = (ROOT / "scripts/manifest.py").read_text(encoding="utf-8")
        self.assertIn('STATUSES = frozenset({"experimental", "supported"})', source)
        self.assertNotIn('"unsupported"', source)


if __name__ == "__main__":
    unittest.main()
