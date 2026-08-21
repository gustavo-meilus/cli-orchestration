"""Thin-adapter and canonical-core contracts."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class AdapterResourceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))

    def test_adapters_map_native_mechanisms_to_three_logical_roles(self) -> None:
        expected = {"codex": "default", "claude": "general-purpose", "copilot": "general-purpose"}
        for tool, generic in expected.items():
            with self.subTest(tool=tool):
                adapter = self.manifest["adapters"][tool]
                self.assertEqual(adapter["generic_agent"], generic)
                text = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in adapter["resources"])
                for role in ("Scout", "Implementer", "Verifier"):
                    self.assertIn(role, text)
                self.assertIn("BLOCKED", text)
                self.assertIn("orchestrator-work-protocol", text)

    def test_adapter_files_do_not_fork_normative_packet_bodies(self) -> None:
        forbidden = ("## Work packet", "## Implementer result", "## Verifier result", "Release-Version:")
        for adapter in self.manifest["adapters"].values():
            for resource in adapter["resources"]:
                text = (ROOT / resource).read_text(encoding="utf-8")
                self.assertFalse(any(item in text for item in forbidden), resource)

    def test_adapter_resources_are_isolated_and_exist(self) -> None:
        claimed = []
        for tool, adapter in self.manifest["adapters"].items():
            for resource in adapter["resources"]:
                self.assertTrue((ROOT / resource).is_file(), resource)
                self.assertNotIn(resource.casefold(), claimed)
                claimed.append(resource.casefold())

    def test_discovery_claims_match_source_verification(self) -> None:
        source = (ROOT / "docs/SOURCE-VERIFICATION.md").read_text(encoding="utf-8")
        for tool, adapter in self.manifest["adapters"].items():
            for url in adapter["verification"]["source_urls"]:
                self.assertIn(url, source, f"{tool}: {url}")

    def test_copilot_fleet_is_not_the_portable_orchestration_owner(self) -> None:
        text = (ROOT / "templates/adapters/copilot.md").read_text(encoding="utf-8")
        self.assertIn("`/fleet`", text)
        self.assertIn("does not use", text)


if __name__ == "__main__":
    unittest.main()
