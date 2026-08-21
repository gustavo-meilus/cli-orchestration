---
name: orchestrator-work-protocol
description: Route development, analysis, or review through direct execution or the smallest useful CLI-neutral orchestration topology. Use when a user requests orchestration, independent verification materially reduces risk, discovery uncertainty needs isolation, independent read-heavy branches help, or work crosses a high-risk boundary.
---

# Orchestrator Work Protocol

Read `references/protocol.md` before routing. When dispatching a worker, also read `references/control-packets.md`. Read `references/state.md` only for explicitly cross-session or multiple dependent batches.

## Execute

1. Apply the ordered cumulative predicates in the protocol. Route-selection completes when the smallest sufficient direct, read-only, Implementer → Verifier, Scout → Implementer → Verifier, or recorded high-assurance route is named.
2. In direct mode, perform the work and native validation.
3. In orchestration mode, become a pure control plane. Dispatch self-contained packets, respect dependencies, and keep one active writer per overlapping boundary.
4. Accept direct work from native checks; accept orchestrated implementation only from a fresh Verifier `PASS` plus any recorded distinct-risk gate.
5. Route one concrete defect through bounded rework; a second failed verification returns cause diagnosis and `BLOCKED`.

If a required independent worker is unavailable, return actionable `BLOCKED`. Preserve framework ownership and canonical OpenSpec skills throughout.
