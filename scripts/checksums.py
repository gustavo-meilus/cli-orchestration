#!/usr/bin/env python3
"""Write or verify deterministic release-asset SHA-256 metadata."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.sha256"
TOP_LEVEL = (
    "README.md", "USAGE.md", "INSTALL.md", "CHANGELOG.md",
    "CONTRIBUTING.md", "SECURITY.md", "CODE_OF_CONDUCT.md",
    ".gitattributes", "LICENSE", "VERSION", "manifest.json",
)


def release_files() -> list[Path]:
    files = [ROOT / name for name in TOP_LEVEL]
    for directory in (
        ROOT / ".github", ROOT / "assets", ROOT / "benchmarks",
        ROOT / "docs", ROOT / "scripts", ROOT / "templates",
    ):
        files.extend(path for path in directory.rglob("*") if path.is_file())
    return sorted(
        path for path in files
        if "__pycache__" not in path.parts and path.suffix not in {".pyc", ".pyo"} and path != MANIFEST
    )


def rendered() -> str:
    return "".join(
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(ROOT).as_posix()}\n"
        for path in release_files()
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    expected = rendered()
    if args.write:
        MANIFEST.write_text(expected, encoding="utf-8", newline="\n")
        print(f"WROTE {MANIFEST} ({len(release_files())} assets)")
        return 0
    if not MANIFEST.is_file() or MANIFEST.read_text(encoding="utf-8") != expected:
        print("FAIL: MANIFEST.sha256 is stale")
        return 1
    print(f"PASS: {len(release_files())} release asset checksums match")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
