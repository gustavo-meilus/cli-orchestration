# Release 2.0 Reconciliation Map

Status: historical implementation evidence for the completed and archived `align-portable-lean-orchestration` change. Current runtime authority is the shipped release surface and canonical specs under `openspec/specs/`.

## Baselines

| Input | Identity | Role in this change |
|---|---|---|
| Current repository | release 2.0.0 source; Git initialized after implementation | Portable multi-CLI runtime authority, subject to executable tests and manifests |
| Archived change | `openspec/changes/archive/2026-08-20-simplify-cross-cli-orchestration/` | Historical planning input only; never runtime authority |
| Lean v2 package | `codex-openspec-lean-orchestration-v2.0.0.zip`, SHA-256 `d2285c8c9bd71b5e323f4eb42281794bd25fa9b5fd517eb8a9d6b53b2feb756d`, rechecked 2026-08-20 | Lean Codex-first implementation input, not an overlay or authority |
| Archived change | `openspec/changes/archive/2026-08-20-align-portable-lean-orchestration/` | Completed planning and verification record; no longer an active change |

The expanded v2 directory has the Windows `ReadOnly` attribute. Its repeat-install behavior is therefore a required regression fixture, not a source attribute to propagate into installed files.

## File ownership and disposition

| File or asset | Owner/classification | Decision | Release 2.0 treatment |
|---|---|---|---|
| `AGENTS.md` | repository contributor policy | retain | Keep repository-local execution policy distinct from the installed runtime block. |
| `.agents/skills/openspec-*` | canonical OpenSpec | retain byte-for-byte | Excluded from package ownership, installation, migration, and shadow copies. |
| `openspec/changes/archive/2026-08-20-align-portable-lean-orchestration/**` | completed planning record | retain | Historical evidence only; canonical specs and shipped behavior govern current use. |
| `openspec/changes/archive/**` | historical planning input | retain | Never installed or treated as current behavior. |
| `templates/skills/orchestrator-work-protocol/**` | package portable core | adapt | Replace six-role default with ordered adaptive routing, three normal roles, compact packets, and optional state v2. |
| `templates/skills/openspec-orchestrated-apply/**` | package integration bridge | adapt | Preserve the public name while delegating apply/verify semantics to canonical OpenSpec skills. |
| `templates/project/AGENTS.block.md` | installed runtime policy | adapt | Publish adaptive routing and pure-control-plane behavior only after orchestration is selected. |
| `templates/project/ORCHESTRATION.md` | optional repository process input | adapt | Keep TDD/custom process inputs without making a second planner or task graph. |
| `templates/adapters/*.md` | package CLI adapters | adapt | Limit each file to native discovery, invocation, generic-agent mapping, fail-closed behavior, and limitations. |
| `templates/codex/agents/{scout,implementer,verifier}.toml` | optional Codex hardening | migrate/add | Map normal logical roles without placing model names in the portable core. |
| `templates/codex/agents/{inspector,planner,executor,reviewer,validator,final-auditor}.toml` | legacy package profiles | retire from default / preserve on upgrade | Do not install as normal roles; migration backs up package-owned copies and does not delete unrelated user profiles. |
| `scripts/install.py`, wrappers | package distribution | adapt | Support explicit one-or-more tools, Codex default, selected-adapter deployment, atomic attribute-safe writes, and recoverable backups. |
| `scripts/verify_install.py`, wrappers | package verification | adapt | Verify selected tools, version consistency, logical entries, native syntax, and OpenSpec preservation boundaries. |
| `scripts/migrate_legacy.py` | package migration | add | Dry-run by default; apply only package-owned reconciliation with backups and conservative state conversion. |
| `scripts/manifest.py`, `manifest.json` | package evidence authority | adapt | Enforce exactly `experimental|supported`, aligned version, source dates, smoke evidence, and ownership separation. |
| `tests/**` | repository validation | adapt | Replace six-role assumptions with route, role, state, adapter, migration, and preservation contracts. |
| `README.md`, `USAGE.md`, `INSTALL.md`, `CHANGELOG.md`, `docs/**` | shipped-current documentation | adapt | Describe release 2.0 behavior and field limitations; no document may present the legacy pipeline as the default. |
| `VERSION`, `MANIFEST.sha256` | public release surface | adapt/regenerate | Align to `2.0.0` after the managed file set stabilizes. |
| `graphify-out/**`, `__pycache__`, `*.pyc` | derived cache | retire | Never package or treat as authority. |

## Reconciliation rules

- Package-owned replacements are backed up; unrelated files are preserved.
- Existing public skill names remain available, but their default behavior becomes adaptive.
- A legacy state file is preserved before any conversion. Only unambiguous claims enter state v2, and every migrated claim requires fresh reconciliation.
- Legacy custom-agent filenames are preserved when they are not demonstrably package-owned. The installer never claims them as current normal-role evidence.
- Canonical OpenSpec paths are sentinel-hashed before distribution tests and must be byte-identical afterward.
