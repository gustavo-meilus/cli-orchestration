"""Aligned version, support, and checksum release contracts."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]


class ReleaseSurfaceTests(unittest.TestCase):
    def test_version_appears_on_every_public_surface(self) -> None:
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(version, "2.0.0")
        for relative in ("README.md", "CHANGELOG.md", "manifest.json", "templates/skills/orchestrator-work-protocol/references/protocol.md"):
            self.assertIn(version, (ROOT / relative).read_text(encoding="utf-8"), relative)

    def test_release_checksums_are_current(self) -> None:
        result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/checksums.py"), "--verify"], cwd=ROOT, text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_public_launch_surface_is_present_and_vector_assets_parse(self) -> None:
        for relative in (
            ".gitattributes", "LICENSE", "CONTRIBUTING.md", "SECURITY.md", "CODE_OF_CONDUCT.md",
            ".github/ISSUE_TEMPLATE/bug.yml", ".github/ISSUE_TEMPLATE/feature.yml",
            ".github/PULL_REQUEST_TEMPLATE.md", "docs/BRAND.md", "docs/LAUNCH.md",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)
        for svg in sorted((ROOT / "assets" / "brand").glob("*.svg")):
            root = ET.parse(svg).getroot()
            self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg", svg.name)
            self.assertIn("viewBox", root.attrib, svg.name)

    def test_public_identity_is_tacticswitch(self) -> None:
        manifest = (ROOT / "manifest.json").read_text(encoding="utf-8")
        self.assertIn('"name": "tacticswitch"', manifest)
        for relative in ("README.md", "CONTRIBUTING.md", "docs/BRAND.md", "docs/LAUNCH.md"):
            surface = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("TacticSwitch", surface, relative)
            self.assertNotIn("CLI Orchestration", surface, relative)
        self.assertIn("github.com/gustavo-meilus/tacticswitch", (ROOT / "SECURITY.md").read_text(encoding="utf-8"))

    def test_readme_keeps_claim_limits_adjacent(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("# TacticSwitch", readme)
        self.assertIn("Use the right formation for the work.", readme)
        self.assertIn("all three adapters are **experimental**", readme)
        self.assertIn("does **not** compare completed route quality", readme)
        self.assertIn("Licensed under the [MIT License](LICENSE)", readme)


if __name__ == "__main__":
    unittest.main()
