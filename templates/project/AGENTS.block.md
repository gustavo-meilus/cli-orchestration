<!-- BEGIN ORCHESTRATOR-STANDARD -->
## Portable adaptive orchestration

KISS: use direct execution for clear, local, low-risk, cheaply verifiable work. Invoke `orchestrator-work-protocol` when the user/repository requires orchestration, independent review materially reduces behavior or regression risk, substantive discovery uncertainty exists, independent read-heavy branches materially help, or work crosses a high-risk boundary.

When orchestration is selected, the primary is a pure control plane. Use the minimum topology: `Implementer -> fresh Verifier`, or `Scout -> Implementer -> fresh Verifier` for material uncertainty. Read-only work uses only useful read-only contexts. Keep one active writer per overlapping boundary and batch by context affinity.

A fresh Verifier is a new non-implementer context; model diversity is not required. Route one concrete defect to the same Implementer when safely available, then use a different fresh Verifier. A second failure returns cause diagnosis and `BLOCKED`.

Planner, Validator, Final Auditor, and specialists are optional high-assurance additions for a documented distinct risk, not routine stages. If a required worker is unavailable, fail closed instead of silently performing its role in the primary.

OpenSpec owns its proposal/spec/design/tasks/apply/verify/sync/archive lifecycle and `.agents/skills/openspec-*`. Use canonical OpenSpec skills and preserve them byte-for-byte. `openspec-orchestrated-apply` is only a thin route-aware bridge.
<!-- END ORCHESTRATOR-STANDARD -->
