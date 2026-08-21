"""Clean install, repeat, migration, attributes, and preservation fixtures."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import unittest

from tests.helpers import isolated_roots, managed_files, run_script


def hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*")) if path.is_file()
    }


class DistributionWorkflowTests(unittest.TestCase):
    def _canonical_sentinel(self, root: Path) -> tuple[Path, str]:
        sentinel = root / ".agents/skills/openspec-preservation-sentinel/SKILL.md"
        sentinel.parent.mkdir(parents=True, exist_ok=True)
        sentinel.write_text("canonical openspec bytes\n", encoding="utf-8")
        return sentinel, hashlib.sha256(sentinel.read_bytes()).hexdigest()

    def _assert_sentinel(self, sentinel: Path, expected: str) -> None:
        self.assertTrue(sentinel.is_file())
        self.assertEqual(hashlib.sha256(sentinel.read_bytes()).hexdigest(), expected)

    def test_fresh_user_multi_cli_install_and_verify(self) -> None:
        with isolated_roots() as (home, project):
            args = ("--scope", "user", "--tool", "codex", "--tool", "claude", "--tool", "copilot")
            installed = run_script("install.py", *args, home=home)
            self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
            self.assertTrue((home / ".codex/orchestration-adapter.md").is_file())
            self.assertTrue((home / ".claude/orchestration-adapter.md").is_file())
            self.assertTrue((home / ".copilot/orchestration-adapter.md").is_file())
            verified = run_script("verify_install.py", *args, home=home)
            self.assertEqual(verified.returncode, 0, verified.stdout + verified.stderr)

    def test_clean_mixed_install_repeat_and_verify_are_deterministic(self) -> None:
        with isolated_roots() as (home, project):
            args = ("--scope", "project", "--project", str(project), "--tool", "codex", "--tool", "claude", "--tool", "copilot")
            first = run_script("install.py", *args, home=home)
            self.assertEqual(first.returncode, 0, first.stderr)
            snapshot = managed_files(project)
            second = run_script("install.py", *args, home=home)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(managed_files(project), snapshot)
            verify = run_script("verify_install.py", *args, home=home)
            self.assertEqual(verify.returncode, 0, verify.stdout + verify.stderr)

    def test_optional_codex_hardening_installs_only_normal_roles(self) -> None:
        with isolated_roots() as (home, project):
            args = ("--scope", "project", "--project", str(project), "--tool", "codex", "--native-hardening")
            self.assertEqual(run_script("install.py", *args, home=home).returncode, 0)
            names = sorted(path.name for path in (project / ".codex/agents").glob("*.toml"))
            self.assertEqual(names, ["implementer.toml", "scout.toml", "verifier.toml"])
            verified = run_script("verify_install.py", *args, home=home)
            self.assertEqual(verified.returncode, 0, verified.stdout + verified.stderr)

    def test_restrictive_destination_attributes_do_not_break_repeat_install(self) -> None:
        with isolated_roots() as (home, project):
            args = ("--scope", "project", "--project", str(project))
            self.assertEqual(run_script("install.py", *args, home=home).returncode, 0)
            protocol = project / ".agents/skills/orchestrator-work-protocol/references/protocol.md"
            protocol.write_text("stale", encoding="utf-8")
            protocol.chmod(stat.S_IREAD)
            result = run_script("install.py", *args, home=home)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Release-Version: 2.0.0", protocol.read_text(encoding="utf-8"))

    def test_invalid_selection_fails_before_install_record_publication(self) -> None:
        with isolated_roots() as (home, project):
            result = run_script("install.py", "--scope", "project", "--project", str(project), "--tool", "invalid", home=home)
            self.assertEqual(result.returncode, 2)
            self.assertFalse((project / ".orchestration/install.json").exists())

    def test_install_and_migration_preserve_canonical_openspec_bytes(self) -> None:
        with isolated_roots() as (home, project):
            canonical = project / ".agents/skills/openspec-apply-change"
            canonical.mkdir(parents=True)
            (canonical / "SKILL.md").write_text("canonical sentinel\n", encoding="utf-8")
            before = hashes(project / ".agents/skills")
            args = ("--scope", "project", "--project", str(project), "--tool", "codex")
            self.assertEqual(run_script("install.py", *args, home=home).returncode, 0)
            self.assertEqual(before, {key: value for key, value in hashes(project / ".agents/skills").items() if key.startswith("openspec-apply-change/")})
            migrate = run_script("migrate_legacy.py", "--scope", "project", "--project", str(project), "--tool", "codex", "--apply", home=home)
            self.assertEqual(migrate.returncode, 0, migrate.stdout + migrate.stderr)
            after = {key: value for key, value in hashes(project / ".agents/skills").items() if key.startswith("openspec-apply-change/")}
            self.assertEqual(before, after)

    def test_legacy_profiles_and_state_are_recoverable(self) -> None:
        with isolated_roots() as (home, project):
            profile = project / ".codex/agents/inspector.toml"
            profile.parent.mkdir(parents=True)
            profile.write_text('name = "inspector"\n# orchestrator-work-protocol\n', encoding="utf-8")
            state = project / ".orchestration/state.json"
            state.parent.mkdir(parents=True)
            state.write_text(json.dumps({
                "schema_version": 1,
                "owner": {"role": "Primary Orchestrator", "thread": "old"},
                "items": [{"id": "one", "objective": "One", "state": "DONE", "dependencies": [], "owned_paths": ["src"], "evidence_refs": [], "rework_count": 0}],
            }), encoding="utf-8")
            preview = run_script("migrate_legacy.py", "--project", str(project), home=home)
            self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
            self.assertTrue(profile.exists())
            self.assertFalse((state.parent / "state.v2.json").exists())
            applied = run_script("migrate_legacy.py", "--project", str(project), "--apply", home=home)
            self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
            self.assertFalse(profile.exists())
            self.assertTrue(list((project / ".orchestration").glob("legacy-backup-*/codex-agents/inspector.toml")))
            self.assertTrue(list(state.parent.glob("state.json.v1.bak-*")))
            migrated = json.loads((state.parent / "state.v2.json").read_text(encoding="utf-8"))
            self.assertEqual(migrated["batches"][0]["status"], "RECONCILE")

    def test_unrelated_legacy_named_profile_is_preserved(self) -> None:
        with isolated_roots() as (home, project):
            profile = project / ".codex/agents/planner.toml"
            profile.parent.mkdir(parents=True)
            profile.write_text('name = "my-unrelated-planner"\n', encoding="utf-8")
            result = run_script("migrate_legacy.py", "--project", str(project), "--apply", home=home)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(profile.read_text(encoding="utf-8"), 'name = "my-unrelated-planner"\n')

    def test_every_installer_option_preserves_canonical_openspec_bytes(self) -> None:
        scenarios = [
            ("project-default", ("--scope", "project")),
            ("project-dry", ("--scope", "project", "--dry-run")),
            ("project-codex-hardening", ("--scope", "project", "--tool", "codex", "--native-hardening")),
            ("project-claude", ("--scope", "project", "--tool", "claude")),
            ("project-copilot", ("--scope", "project", "--tool", "copilot")),
            ("project-mixed", ("--scope", "project", "--tool", "codex", "--tool", "claude", "--tool", "copilot")),
            ("user-default", ("--scope", "user")),
            ("user-dry", ("--scope", "user", "--dry-run")),
            ("user-mixed", ("--scope", "user", "--tool", "codex", "--tool", "claude", "--tool", "copilot")),
        ]
        for name, arguments in scenarios:
            with self.subTest(name=name), isolated_roots() as (home, project):
                root = project if "project" in arguments else home
                sentinel, digest = self._canonical_sentinel(root)
                args = list(arguments)
                if "project" in arguments:
                    args.extend(("--project", str(project)))
                result = run_script("install.py", *args, home=home)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self._assert_sentinel(sentinel, digest)

    def test_every_migration_option_preserves_canonical_openspec_bytes(self) -> None:
        scenarios = [
            ("project-dry", ("--scope", "project")),
            ("project-apply", ("--scope", "project", "--apply")),
            ("project-tools", ("--scope", "project", "--tool", "codex", "--tool", "claude", "--tool", "copilot", "--apply")),
            ("user-dry", ("--scope", "user")),
            ("user-apply", ("--scope", "user", "--tool", "codex", "--tool", "claude", "--apply")),
        ]
        for name, arguments in scenarios:
            with self.subTest(name=name), isolated_roots() as (home, project):
                root = project if "project" in arguments else home
                sentinel, digest = self._canonical_sentinel(root)
                args = list(arguments)
                if "project" in arguments:
                    args.extend(("--project", str(project)))
                custom_state = root / ".orchestration/custom-legacy.json"
                args.extend(("--state", str(custom_state)))
                result = run_script("migrate_legacy.py", *args, home=home)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self._assert_sentinel(sentinel, digest)

    def test_removed_openspec_init_option_is_rejected_without_writes(self) -> None:
        with isolated_roots() as (home, project):
            sentinel, digest = self._canonical_sentinel(project)
            before = managed_files(project)
            result = run_script("install.py", "--scope", "project", "--project", str(project), "--init-openspec", home=home)
            self.assertEqual(result.returncode, 2)
            self.assertIn("unrecognized arguments: --init-openspec", result.stderr)
            self.assertEqual(managed_files(project), before)
            self._assert_sentinel(sentinel, digest)

    def test_verifier_rejects_corrupt_installed_adapter_mapping_and_entry(self) -> None:
        for tool, destination, mapping, entry in (
            ("codex", ".codex", "default", "$orchestrator-work-protocol"),
            ("claude", ".claude", "general-purpose", "/orchestrator-work-protocol"),
            ("copilot", ".github", "general-purpose", "orchestrator-work-protocol"),
        ):
            for defect, needle in (("mapping", mapping), ("entry", entry)):
                with self.subTest(tool=tool, defect=defect), isolated_roots() as (home, project):
                    args = ("--scope", "project", "--project", str(project), "--tool", tool)
                    self.assertEqual(run_script("install.py", *args, home=home).returncode, 0)
                    adapter = project / destination / "orchestration-adapter.md"
                    adapter.write_text(adapter.read_text(encoding="utf-8").replace(needle, "CORRUPTED", 1), encoding="utf-8")
                    result = run_script("verify_install.py", *args, home=home)
                    self.assertEqual(result.returncode, 1)
                    self.assertIn("differs from package template", result.stdout)

    def test_verifier_rejects_corrupt_native_config_and_claude_bridge(self) -> None:
        with isolated_roots() as (home, project):
            args = ("--scope", "project", "--project", str(project), "--tool", "codex")
            self.assertEqual(run_script("install.py", *args, home=home).returncode, 0)
            config = project / ".codex/config.toml"
            config.write_text(config.read_text(encoding="utf-8").replace("enabled = true", "enabled = false"), encoding="utf-8")
            result = run_script("verify_install.py", *args, home=home)
            self.assertEqual(result.returncode, 1)
            self.assertIn("agents.enabled must be true", result.stdout)
        with isolated_roots() as (home, project):
            args = ("--scope", "project", "--project", str(project), "--tool", "claude")
            self.assertEqual(run_script("install.py", *args, home=home).returncode, 0)
            (project / "CLAUDE.md").write_text("corrupt bridge\n", encoding="utf-8")
            result = run_script("verify_install.py", *args, home=home)
            self.assertEqual(result.returncode, 1)
            self.assertIn("Claude bridge differs from package template", result.stdout)


if __name__ == "__main__":
    unittest.main()
