"""Regression coverage for package-owned Python cache hygiene."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tests.helpers import REPOSITORY_ROOT


class RepositoryCacheHygieneTests(unittest.TestCase):
    """Package inputs and dry-run output exclude interpreter cache artifacts."""

    def test_ignore_rules_cover_python_cache_artifacts_exactly(self) -> None:
        lines = (REPOSITORY_ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines, ["__pycache__/", "*.pyc", "*.pyo"])

    def test_templates_contain_no_python_cache_artifacts(self) -> None:
        artifacts = [
            path.relative_to(REPOSITORY_ROOT / "templates").as_posix()
            for path in (REPOSITORY_ROOT / "templates").rglob("*")
            if "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}
        ]
        self.assertEqual(artifacts, [])

    def test_project_codex_dry_run_is_repeatable_cache_free_and_side_effect_free(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            home = root / "home"
            project = root / "project"
            home.mkdir()
            project.mkdir()
            environment = os.environ.copy()
            environment.update(
                {
                    "HOME": str(home),
                    "USERPROFILE": str(home),
                    "PYTHONDONTWRITEBYTECODE": "1",
                }
            )
            environment.pop("CODEX_HOME", None)

            results = []
            for _ in range(2):
                result = subprocess.run(
                    [
                        sys.executable,
                        "-B",
                        str(REPOSITORY_ROOT / "scripts" / "install.py"),
                        "--scope",
                        "project",
                        "--project",
                        str(project),
                        "--dry-run",
                    ],
                    cwd=REPOSITORY_ROOT,
                    env=environment,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(list(home.rglob("*")), [])
                self.assertEqual(list(project.rglob("*")), [])
                results.append(result)

            first, second = results
            self.assertEqual(first.stdout, second.stdout)
            self.assertEqual(first.stderr, second.stderr)
            self.assertIn(
                f"DESTINATION tool=codex scope=project root={project / '.codex'}",
                first.stdout.splitlines(),
            )
            for stream in (first.stdout, first.stderr, second.stdout, second.stderr):
                self.assertNotIn("__pycache__", stream)
                self.assertNotIn(".pyc", stream)
                self.assertNotIn(".pyo", stream)


if __name__ == "__main__":
    unittest.main()
