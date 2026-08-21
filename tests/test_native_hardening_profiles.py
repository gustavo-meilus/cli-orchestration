"""Optional Codex-native profile contracts."""

from __future__ import annotations

from pathlib import Path
import unittest

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None


ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / "templates/codex/agents"


@unittest.skipIf(tomllib is None, "tomllib unavailable")
class NativeHardeningProfileTests(unittest.TestCase):
    def test_normal_profiles_are_parseable_role_pointers(self) -> None:
        for filename, role in (("scout.toml", "Scout"), ("implementer.toml", "Implementer"), ("verifier.toml", "Verifier")):
            with self.subTest(filename=filename):
                data = tomllib.loads((PROFILES / filename).read_text(encoding="utf-8"))
                self.assertEqual(data["name"], role.casefold())
                self.assertIn(f"Role: {role}", data["developer_instructions"])
                self.assertIn("orchestrator-work-protocol", data["developer_instructions"])

    def test_legacy_profiles_are_labeled_optional_and_not_normal_defaults(self) -> None:
        for path in PROFILES.glob("*.toml"):
            if path.name in {"scout.toml", "implementer.toml", "verifier.toml"}:
                continue
            data = tomllib.loads(path.read_text(encoding="utf-8"))
            self.assertIn("optional high-assurance", data["description"].lower())

    def test_profiles_do_not_duplicate_packet_bodies(self) -> None:
        for path in PROFILES.glob("*.toml"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("## Work packet", text)
            self.assertNotIn("## Verifier result", text)


if __name__ == "__main__":
    unittest.main()
