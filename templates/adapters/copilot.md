# GitHub Copilot CLI adapter

## Native mapping

- Instructions: applicable `AGENTS.md` plus Copilot CLI's native repository/user instruction discovery.
- Skills: project `.github/skills/<name>/SKILL.md`; user `.copilot/skills/<name>/SKILL.md`.
- Generic worker: Copilot CLI `general-purpose`/custom-agent prompt path; assign exactly one logical `Scout`, `Implementer`, or `Verifier` contract.
- Explicit entry: invoke `orchestrator-work-protocol` using the active Copilot CLI skill/agent syntax; preserve the logical name even when native punctuation differs.

## Fail closed and limitations

Confirm the active CLI can create and isolate every required generic worker. If it cannot, return actionable `BLOCKED`; never silently execute or self-verify in the primary.

The portable adapter does not use `/fleet` as its orchestration owner: fleet plans and delegates independently and would create competing ownership. Copilot-native model catalogs, permissions, and parallelism are runtime details. This package installs no Copilot-specific hardening profile. Native support remains experimental until a tested CLI version passes fresh-process discovery, invocation, worker-creation, and unavailable-worker smoke checks.
