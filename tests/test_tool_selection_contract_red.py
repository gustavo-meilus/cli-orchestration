"""Installer selection contracts for the adaptive portable distribution."""

from __future__ import annotations

import unittest

from tests.helpers import isolated_roots, managed_files, run_script


class ToolSelectionContractTests(unittest.TestCase):
    destination_roots = {"codex": ".codex", "claude": ".claude", "copilot": ".github"}

    def managed_file_snapshots(self, home, project) -> tuple[dict[str, bytes], dict[str, bytes]]:
        return managed_files(home), managed_files(project)

    def assert_rejected_before_writes(self, result, home, project, snapshots, diagnostic: str) -> None:
        """Require argument failures to leave both isolated targets untouched."""
        self.assertEqual(result.returncode, 2)
        self.assertIn(diagnostic, result.stderr)
        home_snapshot, project_snapshot = snapshots
        self.assertEqual(managed_files(home), home_snapshot)
        self.assertEqual(managed_files(project), project_snapshot)

    def test_default_is_codex_and_explicit_tool_selects_one_adapter(self) -> None:
        with isolated_roots() as (home, project):
            untouched = {}
            for other_tool in ("claude", "copilot"):
                other_root = project / self.destination_roots[other_tool]
                sentinel = other_root / "preexisting.txt"
                sentinel.parent.mkdir(parents=True)
                sentinel.write_text(f"{other_tool} sentinel", encoding="utf-8")
                untouched[other_tool] = managed_files(other_root)
            result = run_script("install.py", "--scope", "project", "--project", str(project), home=home)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("tool: codex", result.stdout.lower())
            self.assertTrue((project / ".codex").exists())
            for other_tool, snapshot in untouched.items():
                self.assertEqual(managed_files(project / self.destination_roots[other_tool]), snapshot)

    def test_rejects_invalid_tool_before_writes(self) -> None:
        with isolated_roots() as (home, project):
            snapshots = self.managed_file_snapshots(home, project)
            result = run_script(
                "install.py", "--scope", "project", "--project", str(project), "--tool", "all", home=home,
            )
            self.assert_rejected_before_writes(
                result, home, project, snapshots, "unsupported --tool 'all'",
            )

    def test_repeated_tool_option_installs_a_deduplicated_multi_cli_selection(self) -> None:
        with isolated_roots() as (home, project):
            result = run_script(
                "install.py", "--scope", "project", "--project", str(project),
                "--tool", "codex", "--tool", "claude", home=home,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("tools: codex, claude", result.stdout.lower())
            self.assertTrue((project / ".codex").exists())
            self.assertTrue((project / ".claude").exists())
            self.assertFalse((project / ".github" / "skills").exists())

            repeated = run_script(
                "install.py", "--scope", "project", "--project", str(project),
                "--tool", "codex", "--tool", "claude", "--tool", "codex", home=home,
            )
            self.assertEqual(repeated.returncode, 0, repeated.stderr)
            self.assertIn("tools: codex, claude", repeated.stdout.lower())

    def test_rejects_unsupported_claude_native_hardening_before_writes(self) -> None:
        with isolated_roots() as (home, project):
            snapshots = self.managed_file_snapshots(home, project)
            result = run_script(
                "install.py", "--scope", "project", "--project", str(project),
                "--tool", "claude", "--native-hardening", home=home,
            )
            self.assert_rejected_before_writes(
                result, home, project, snapshots, "--native-hardening is not supported for tool claude",
            )

    def test_rejects_unsupported_copilot_native_hardening_before_writes(self) -> None:
        with isolated_roots() as (home, project):
            snapshots = self.managed_file_snapshots(home, project)
            result = run_script(
                "install.py", "--scope", "project", "--project", str(project),
                "--tool", "copilot", "--native-hardening", home=home,
            )
            self.assert_rejected_before_writes(
                result, home, project, snapshots, "--native-hardening is not supported for tool copilot",
            )

    def test_resolves_each_adapter_destination_without_cross_tool_writes(self) -> None:
        for tool, expected in self.destination_roots.items():
            with self.subTest(tool=tool), isolated_roots() as (home, project):
                untouched = {}
                for other_tool, other_root in self.destination_roots.items():
                    if other_tool == tool:
                        continue
                    sentinel = project / other_root / "preexisting.txt"
                    sentinel.parent.mkdir(parents=True)
                    sentinel.write_text(f"{other_tool} sentinel", encoding="utf-8")
                    untouched[other_tool] = managed_files(project / other_root)
                result = run_script("install.py", "--scope", "project", "--project", str(project), "--tool", tool, home=home)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue((project / expected).exists())
                for other_tool, snapshot in untouched.items():
                    self.assertEqual(
                        managed_files(project / self.destination_roots[other_tool]),
                        snapshot,
                        f"{tool} installation modified {other_tool}'s destination",
                    )
