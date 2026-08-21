# Troubleshooting

## Skill or adapter is not discovered

Run `scripts/verify_install.py` with the same scope and repeated `--tool` selection used for installation. Restart the CLI after a new user-level install. Confirm native discovery roots against `docs/SOURCE-VERIFICATION.md`.

## Orchestration cannot create a worker

Return `BLOCKED` with the missing Scout/Implementer/Verifier capability. Check CLI version, agent enablement, permissions, non-interactive approval constraints, and native account feature availability. Do not silently complete the role in the primary.

## Work unexpectedly uses six routine stages

The release 2.0 normal route is Implementer → fresh Verifier, with Scout only for material uncertainty. Legacy profiles are optional high-assurance/migration resources. Reinstall or migrate if the managed block still describes the old default.

## Verification changed files

Treat the mutation as implementation. Assign ownership and send the changed output to a fresh Verifier.

## Repeat install fails on Windows read-only files

Release 2.0 uses attribute-safe atomic replacement. If failure remains, use `--dry-run`, inspect the exact package-owned destination, preserve its backup, and check filesystem/OneDrive policy. Never broaden removal to the repository root.

## Legacy state is blocked

Keep the v1 original. `migrate_legacy.py` converts only unambiguous claims to `RECONCILE`; repair invalid JSON/claims or start a fresh state v2 file. Old review/audit identities never imply new acceptance.

## OpenSpec resources changed

Stop and restore the canonical resources through OpenSpec's own installation/update path. The package installer and migration do not own those files; preservation test failure is release-blocking.
