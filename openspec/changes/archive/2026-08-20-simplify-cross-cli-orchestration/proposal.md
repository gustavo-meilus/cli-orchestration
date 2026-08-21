## Why

The orchestration protocol has strong logical roles and acceptance gates, but some process, dependency, ownership, and validation rules remain advisory, while its installed runtime artifacts are Codex-specific. A smaller portable core based on each CLI's built-in general-purpose subagent can support Codex, Claude Code, and Copilot CLI without duplicating six role implementations per platform or introducing a scheduler.

## What Changes

- Separate the six logical orchestration roles from the platform-specific subagent type used to execute them.
- Use the built-in generic subagent as the portable baseline: Codex `default`, Claude Code `general-purpose`, and Copilot CLI `general-purpose`.
- Retain fresh-thread Inspector, Planner, Executor, Reviewer, Validator, and Final Auditor contracts, with optional native custom-agent profiles as defense-in-depth rather than required runtime infrastructure.
- **BREAKING**: New installations stop requiring the six Codex custom-agent profiles by default; existing files are preserved during upgrade, and an explicit native-hardening option installs or refreshes them.
- Add one optional repository process contract for direct tasks and non-OpenSpec development frameworks.
- Make TDD evidence, dependency readiness, path ownership, single-writer coordination, role identity, and exact validation commands explicit protocol requirements.
- Allow long-running work to persist the existing compact ledger in one optional repository-local state file for cross-session reconstruction.
- Add thin Codex, Claude Code, and Copilot CLI adapters plus tool-aware installation, verification, manifest declarations, and smoke tests.
- Document safe composition with OpenSpec and Superpowers under a one-orchestration-owner rule.
- Do not add an orchestration service, task database, lock manager, merge queue, automatic worktree lifecycle, or normative dependence on Claude agent teams or Copilot Fleet.

## Capabilities

### New Capabilities

- `portable-agent-runtime`: Defines how platform-generic subagents execute six preserved logical roles with fresh-thread independence and optional native hardening profiles.
- `development-process-contract`: Defines durable direct-task/framework inputs and evidence requirements, including enforceable red-green TDD reporting and single-orchestrator composition.
- `work-coordination-and-acceptance`: Defines dependency readiness, single-writer ownership, role-identity separation, validation commands, and acceptance transitions.
- `multi-cli-distribution`: Defines truthful support declarations and tool-aware installation, verification, and discovery for Codex, Claude Code, and Copilot CLI.

### Modified Capabilities

None. This repository had no canonical OpenSpec capabilities before this change.

## Impact

- Protocol and control-packet references under `templates/skills/orchestrator-work-protocol/`.
- OpenSpec orchestration mapping, project instructions, usage, architecture, compatibility, and source-verification documentation.
- Manifest ownership/support metadata.
- Installer and verifier command-line interfaces and their platform-specific templates.
- Existing Codex custom-agent files, which become optional native hardening profiles rather than the portable execution requirement.
- New tests and temporary-install fixtures for supported CLI layouts and idempotent verification.
- Optional repository-local orchestration process/state files, with no service or database dependency.
