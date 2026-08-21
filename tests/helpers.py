"""Isolated standard-library helpers for installer/verifier contract tests."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Iterator
from contextlib import contextmanager


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


@contextmanager
def isolated_roots() -> Iterator[tuple[Path, Path]]:
    """Yield temporary user and project roots without touching real CLI homes."""
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        user_root = root / "user"
        project_root = root / "project"
        user_root.mkdir()
        project_root.mkdir()
        yield user_root, project_root


def run_script(script: str, *arguments: str, home: Path, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    """Run a package script with an isolated home and captured managed changes."""
    environment = os.environ.copy()
    environment.update({"HOME": str(home), "USERPROFILE": str(home)})
    return subprocess.run(
        [sys.executable, str(REPOSITORY_ROOT / "scripts" / script), *arguments],
        cwd=cwd or REPOSITORY_ROOT,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )


def managed_files(root: Path) -> dict[str, bytes]:
    """Return a deterministic snapshot for idempotence and write-scope assertions."""
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file() and ".bak-" not in path.name
    }
