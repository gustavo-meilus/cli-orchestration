"""Enabled, side-effect-free coverage for installer target selection."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tests.helpers import REPOSITORY_ROOT


def _load_installer():
    specification = importlib.util.spec_from_file_location(
        "install_target_resolution", REPOSITORY_ROOT / "scripts" / "install.py"
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


INSTALLER = _load_installer()


class InstallTargetResolutionTests(unittest.TestCase):
    """Every adapter/scope pair resolves only its declared discovery paths."""

    ROOT = Path("installation-root")

    EXPECTED = {
        ("codex", "user"): (
            ".codex/AGENTS.md", ".agents/skills", ".codex", None,
        ),
        ("codex", "project"): (
            "AGENTS.md", ".agents/skills", ".codex", None,
        ),
        ("claude", "user"): (
            ".claude/AGENTS.md", ".claude/skills", ".claude", ".claude/CLAUDE.md",
        ),
        ("claude", "project"): (
            "AGENTS.md", ".claude/skills", ".claude", "CLAUDE.md",
        ),
        ("copilot", "user"): (
            ".copilot/AGENTS.md", ".copilot/skills", ".copilot", None,
        ),
        ("copilot", "project"): (
            "AGENTS.md", ".github/skills", ".github", None,
        ),
    }

    def test_every_tool_scope_resolves_exact_declared_paths(self) -> None:
        for (tool, scope), expected in self.EXPECTED.items():
            with self.subTest(tool=tool, scope=scope):
                instruction, skills, tool_root, bridge = INSTALLER.resolve_targets(
                    tool, scope, self.ROOT
                )
                self.assertEqual(
                    (instruction, skills, tool_root, bridge),
                    tuple(
                        None if path is None else self.ROOT / path
                        for path in expected
                    ),
                )

    def test_codex_user_targets_use_default_or_configured_codex_home(self) -> None:
        home = Path("user-home")
        configured = Path("configured-codex-home")

        self.assertEqual(
            INSTALLER.resolve_targets("codex", "user", home),
            (home / ".codex" / "AGENTS.md", home / ".agents/skills", home / ".codex", None),
        )
        self.assertEqual(
            INSTALLER.resolve_targets("codex", "user", home, codex_home=configured),
            (configured / "AGENTS.md", home / ".agents/skills", configured, None),
        )

    def test_configured_codex_home_expands_user_directory(self) -> None:
        with patch.dict(os.environ, {"HOME": "user-home", "USERPROFILE": "user-home", "CODEX_HOME": "~/.custom-codex"}, clear=False):
            self.assertEqual(INSTALLER.configured_codex_home(Path("user-home")), Path("user-home/.custom-codex"))

    def test_codex_user_dry_run_resolves_default_and_custom_homes_without_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            home = root / "home"
            custom = root / "custom-codex"
            home.mkdir()
            environment = os.environ.copy()
            environment.update({"HOME": str(home), "USERPROFILE": str(home)})

            default_environment = environment.copy()
            default_environment.pop("CODEX_HOME", None)
            default = subprocess.run(
                [sys.executable, str(REPOSITORY_ROOT / "scripts" / "install.py"), "--scope", "user", "--dry-run"],
                cwd=REPOSITORY_ROOT,
                env=default_environment,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(default.returncode, 0, default.stderr)
            self.assertIn(f"root={home / '.codex'}", default.stdout)
            self.assertFalse((home / ".codex").exists())
            self.assertFalse((home / ".agents").exists())

            custom_environment = environment.copy()
            custom_environment["CODEX_HOME"] = str(custom)
            configured = subprocess.run(
                [sys.executable, str(REPOSITORY_ROOT / "scripts" / "install.py"), "--scope", "user", "--dry-run"],
                cwd=REPOSITORY_ROOT,
                env=custom_environment,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(configured.returncode, 0, configured.stderr)
            self.assertIn(f"root={custom}", configured.stdout)
            self.assertIn(f"UPDATE {custom / 'AGENTS.md'}", configured.stdout)
            self.assertIn(f"WRITE  {home / '.agents/skills'}", configured.stdout)
            self.assertFalse(custom.exists())
            self.assertFalse((home / ".agents").exists())

    def test_copy_owned_tree_excludes_interpreter_cache_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            destination = root / "destination"
            (source / "nested").mkdir(parents=True)
            (source / "nested" / "kept.py").write_text("pass\n", encoding="utf-8")
            (source / "nested" / "compiled.pyc").write_bytes(b"bytecode")
            (source / "nested" / "optimized.pyo").write_bytes(b"bytecode")
            (source / "__pycache__").mkdir()
            (source / "__pycache__" / "state.cpython-311.pyc").write_bytes(b"bytecode")

            INSTALLER.copy_owned_tree(source, destination, dry_run=False)

            self.assertEqual((destination / "nested" / "kept.py").read_text(encoding="utf-8"), "pass\n")
            self.assertFalse((destination / "nested" / "compiled.pyc").exists())
            self.assertFalse((destination / "nested" / "optimized.pyo").exists())
            self.assertFalse((destination / "__pycache__").exists())
