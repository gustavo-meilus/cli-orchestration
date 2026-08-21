---
name: openspec-orchestrated-apply
description: Apply an approved OpenSpec change through the portable adaptive orchestrator while preserving canonical OpenSpec ownership. Use when an OpenSpec implementation needs independent worker contexts or the user explicitly requests orchestration.
---

# OpenSpec Orchestrated Apply

Read `references/workflow.md` and the active `orchestrator-work-protocol` before dispatch.

This is a thin route-aware integration. It does not copy, replace, or shadow canonical `.agents/skills/openspec-*`, and it does not recreate proposal, specs, design, tasks, lifecycle, or acceptance criteria.

1. Receive the change name and select the adaptive route from visible governing information. Material route-selection uncertainty prepends Scout.
2. Give the Implementer the change name and instruct it to use canonical `$openspec-apply-change` with the CLI-returned context files and tasks.
3. After implementation, create a fresh Verifier and instruct it to use canonical `$openspec-verify-change` when available and materially useful.
4. Treat canonical verification as conformance evidence. The fresh Verifier independently judges artifacts, actual state, regressions, and native checks before returning `PASS`, `REWORK`, or `BLOCKED`.
5. Apply the protocol's one-writer, context-affinity, bounded-rework, and fail-closed rules. Report readiness for canonical sync/archive only after acceptance.

For a clear low-risk OpenSpec change that qualifies for direct mode, use canonical `$openspec-apply-change` directly; this bridge is unnecessary.
