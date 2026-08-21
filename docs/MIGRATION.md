# Migration from 1.x

Release 2.0 changes the normal route and state schema but preserves the two public logical skill names.

## Preview

```bash
python scripts/migrate_legacy.py --scope project --project /repo --tool codex
```

Dry-run is the default. It reports package-owned legacy profiles eligible for relocation, unrelated files it will preserve, legacy state conversion, and the resulting adaptive install.

## Apply

```bash
python scripts/migrate_legacy.py --scope project --project /repo --tool codex --apply
python scripts/verify_install.py --scope project --project /repo --tool codex
```

Repeat `--tool` for a multi-CLI destination. Migration:

- relocates only legacy Codex profiles carrying a recognized package marker to `.orchestration/legacy-backup-*`;
- preserves unrelated same-named profiles;
- backs up v1 state and writes `state.v2.json` with every readable claim at `RECONCILE`;
- blocks invalid or ambiguous state without overwriting the original;
- installs the selected release 2.0 adapters/core using recoverable file backups;
- never touches canonical `.agents/skills/openspec-*`.

## Rollback

Restore package-owned files from `.bak-<timestamp>` siblings and legacy profiles from `.orchestration/legacy-backup-*`. Keep the v1 state backup; remove or set aside the generated v2 claim only after confirming its exact path. Reinstall the prior release if needed. Unrelated and canonical OpenSpec files require no rollback because migration does not own them.
