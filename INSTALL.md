# Installation

Requires Python 3.10+; OpenSpec is optional unless its workflow is used. Installation modifies only selected adapter destinations, the two package-owned skills, the marked policy block, and `.orchestration/install.json`. Existing replaced files receive timestamped backups.

## Project scope

Codex-only compatibility default:

```bash
python scripts/install.py --scope project --project /repo
python scripts/verify_install.py --scope project --project /repo
```

Explicit selection; repeat `--tool` for multiple CLIs:

```bash
python scripts/install.py --scope project --project /repo --tool claude --tool copilot
python scripts/verify_install.py --scope project --project /repo --tool claude --tool copilot
```

## User scope

```bash
python scripts/install.py --scope user --tool codex
python scripts/verify_install.py --scope user --tool codex
```

Codex honors `CODEX_HOME` for its native root while shared Codex skills remain under the selected user home. Claude and Copilot use their documented native roots. Windows and WSL are separate environments and need separate installs.

## Dry run and optional hardening

```bash
python scripts/install.py --scope project --project /repo --tool codex --dry-run
python scripts/install.py --scope project --project /repo --tool codex --native-hardening
```

Native hardening installs only Codex Scout/Implementer/Verifier profiles. It is not required for portable behavior or base compatibility.

## OpenSpec initialization

The package installer never initializes or updates OpenSpec. If OpenSpec is wanted, run its current canonical initialization/update command separately after consulting authoritative OpenSpec documentation. That explicit framework operation owns any resulting `.agents/skills/openspec-*` changes.

## Upgrade and rollback

Preview legacy reconciliation with `scripts/migrate_legacy.py`; see [docs/MIGRATION.md](docs/MIGRATION.md). Restore a replaced package-owned file from its `.bak-<timestamp>` sibling or `.orchestration/legacy-backup-*`. Canonical OpenSpec and unrelated files are never rollback targets.
