# Codex CLI adapter

## Native mapping

- Instructions: project `AGENTS.md`; user `$CODEX_HOME/AGENTS.md` (normally `~/.codex/AGENTS.md`).
- Skills: project/user `.agents/skills/<name>/SKILL.md` under the applicable discovery root.
- Generic worker: built-in `default` subagent; name the logical `Scout`, `Implementer`, or `Verifier` contract in the dispatch.
- Explicit entry: `$orchestrator-work-protocol`; OpenSpec material orchestration may use `$openspec-orchestrated-apply`.

The portable core owns routing, packets, and acceptance. Codex configuration contains only native agent enablement/concurrency and optional custom-agent hardening.

## Fail closed

Before an orchestrated route performs a responsibility, confirm Codex can create the required independent context. If creation fails or a fresh Verifier cannot be isolated, return actionable `BLOCKED`; never perform that role in the primary.

## Optional hardening

`templates/codex/agents/{scout,implementer,verifier}.toml` are optional native profiles. They point back to the canonical role contracts. Their absence does not change portable behavior. Legacy six-role profile names are optional high-assurance migration resources and are not installed by default.
