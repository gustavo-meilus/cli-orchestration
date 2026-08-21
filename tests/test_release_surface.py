"""Aligned version, support, and checksum release contracts."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import unittest


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


if __name__ == "__main__":
    unittest.main()
