# Claude Code adapter

## Native mapping

- Instructions: project `CLAUDE.md` bridge plus `AGENTS.md`; user `~/.claude/CLAUDE.md` bridge plus `~/.claude/AGENTS.md`.
- Skills: `.claude/skills/<name>/SKILL.md` in the selected project or user scope.
- Generic worker: Claude Code `general-purpose` subagent; dispatch it with exactly one logical `Scout`, `Implementer`, or `Verifier` contract.
- Explicit entry: `/orchestrator-work-protocol`; OpenSpec material orchestration may use `/openspec-orchestrated-apply`.

## Fail closed and limitations

Confirm the active Claude Code process can create a separate general-purpose context before assigning a required role. If worker creation or fresh-Verifier isolation is unavailable, return actionable `BLOCKED`; never collapse the route into primary implementation or self-review.

Claude-native permissions, hooks, model selection, and custom-agent metadata are adapter/runtime features, not portable protocol requirements. This package installs no Claude-specific hardening profile.
