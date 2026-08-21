## 1. Establish Test and Metadata Baselines

- [x] 1.1 Add standard-library test helpers that install into temporary user/project roots and capture managed-file changes without invoking a model.
- [x] 1.2 Add failing tests for `--tool codex|claude|copilot`, Codex default selection, invalid tool/native-hardening combinations, adapter destination resolution, and one-tool-per-invocation behavior.
- [x] 1.3 Replace Codex-only manifest ownership fields with a versioned per-tool adapter map covering status, generic-agent name, scopes, resources, native hardening, and verification evidence; retain explicit legacy Codex profile ownership metadata for safe migration.
- [x] 1.4 Add manifest/schema tests that reject unsupported status promotion, missing generic-agent mappings, overlapping owned resources, and malformed verification metadata.

## 2. Canonical Portable Protocol

- [x] 2.1 Make the canonical orchestration skill and protocol CLI-neutral while preserving the pure control-plane boundary and six logical roles.
- [x] 2.2 Add generic-agent dispatch rules for Codex `default`, Claude Code `general-purpose`, and Copilot CLI `general-purpose`, including fresh-thread requirements for Reviewer and Final Auditor.
- [x] 2.3 Extend control packets and the primary ledger with process mode, owned paths, shared resources, exact validation commands, TDD red/green evidence, changed paths, and role/thread identities.
- [x] 2.4 Add and test the hard routing invariants that all dependencies are `DONE` before `READY` and at most one source-writing Executor is active.
- [x] 2.5 Update the OpenSpec orchestration skill to use the same canonical generic-agent dispatch and packet contracts without weakening OpenSpec authority, drift reconciliation, or acceptance mapping.
- [x] 2.6 Convert the existing Codex custom-agent templates into optional native-hardening profiles that reference and preserve the canonical role contracts.

## 3. Process and Resumption Contracts

- [x] 3.1 Add an optional `ORCHESTRATION.md` template with objective, authority, `STANDARD|TDD|CUSTOM` process mode, work derivation, dependencies, acceptance criteria, and exact validation commands.
- [x] 3.2 Add TDD protocol tests proving review cannot pass without reliable red and green evidence references.
- [x] 3.3 Add the one-orchestration-owner rule and explicit OpenSpec/Superpowers composition behavior to the canonical protocol and compatibility guidance.
- [x] 3.4 Define a versioned `.orchestration/state.json` schema containing only compact ledger state and add validation/reconciliation guidance for cross-session resumption, including strict role/string/version parity, safe item lifecycle, cycle detection, and truthful no-change completion.
- [x] 3.5 Add tests that reject invalid state transitions, dependency-ready violations, concurrent source writers, cycle/removal/write-bypass cases, unsafe role identities, and recursive transcript/raw-log fields in persisted state.

## 4. Thin CLI Adapters

- [x] 4.1 Verify current official discovery paths, invocation syntax, generic-agent names, and ordinary-subagent limitations for Codex, Claude Code, and Copilot CLI; update source-verification records with URLs, versions, and dates.
- [x] 4.2 Add a Codex adapter resource containing only Codex discovery paths, `default` dispatch syntax, invocation spelling, and optional native-hardening behavior.
- [x] 4.3 Add a Claude Code adapter resource and minimal `CLAUDE.md` bridge using ordinary `general-purpose` subagents without depending on agent teams.
- [x] 4.4 Add a Copilot CLI adapter resource using its supported instruction/skill discovery and `general-purpose` subagent without assigning normative scheduling or acceptance to Fleet.
- [x] 4.5 Add static tests that each adapter can locate every canonical role and packet while canonical resources remain free of conflicting platform-specific invocation syntax.

## 5. Tool-Aware Installation

- [x] 5.1 Refactor installer target resolution into one declarative adapter table shared by user/project scope logic.
- [ ] 5.2 Add `--tool codex|claude|copilot` with a backward-compatible Codex default and copy only the selected adapter's owned resources plus canonical skills.
- [ ] 5.3 Add `--native-hardening`, install supported native profiles only when explicitly requested, and fail clearly for adapters without native profiles.
- [ ] 5.4 Preserve pre-existing Codex profile files during default upgrades, avoid refreshing them without native-hardening opt-in, and report their retained legacy/native status without deleting them.
- [ ] 5.5 Make `--init-openspec` select the OpenSpec tool integration matching the chosen CLI and preserve current init/update and dry-run behavior.
- [ ] 5.6 Update PowerShell and shell wrappers to forward tool and native-hardening options consistently.
- [ ] 5.7 Add installation tests for backup behavior, dry runs, repeated-install idempotence, scope validation, legacy-profile preservation, and non-overlapping cross-tool writes.

## 6. Tool-Aware Verification

- [ ] 6.1 Add `--tool codex|claude|copilot` to the verifier and validate only the selected adapter's managed resources and discovery layout.
- [ ] 6.2 Validate adapter metadata, canonical skill frontmatter, managed instruction blocks/bridges, generic-agent mapping, and optional native profiles with actionable failures.
- [ ] 6.3 Report retained legacy Codex profiles and unavailable optional CLI binaries as warnings rather than silently accepting or deleting them.
- [ ] 6.4 Add verifier tests for valid temporary installations and for every required missing, malformed, mismatched, or stale adapter resource.

## 7. Documentation and Migration

- [ ] 7.1 Update README, installation, usage, architecture, workflow, governance, troubleshooting, and adoption documentation for portable generic agents, logical roles, one writer, exact evidence, and optional state persistence.
- [ ] 7.2 Add a concise compatibility guide for OpenSpec, direct tasks, custom frameworks, TDD, and safe Superpowers composition under one orchestration owner.
- [ ] 7.3 Document Codex, Claude Code, and Copilot CLI installation/verification commands, adapter status, limitations, and the prohibition on treating Claude agent teams or Copilot Fleet as normative schedulers.
- [ ] 7.4 Add release and rollback guidance for the breaking default-profile change, including preserved legacy profiles and explicit native-hardening opt-in.

## 8. Validation and Support Promotion

- [ ] 8.1 Run the complete Python test suite, syntax/compile checks, OpenSpec strict validation, and temporary user/project install-verify-idempotence matrices for every adapter.
- [ ] 8.2 Run the documented fresh-process Codex smoke test and record the discovered skill, generic-agent dispatch, role packet, CLI version, and verification date.
- [ ] 8.3 Run equivalent fresh-process Claude Code and Copilot CLI smoke tests where the CLIs are available; keep any adapter without passing discovery evidence marked `experimental`.
- [ ] 8.4 Reconcile manifest support statuses and documentation strictly from smoke-test evidence, then run a final clean verification of package-owned resources and unrelated-file preservation.
