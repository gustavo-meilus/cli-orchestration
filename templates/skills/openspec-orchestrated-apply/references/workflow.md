# OpenSpec Composition Boundary

Status: Normative integration reference

## Authority

Use this order: latest explicit user requirement; governing repository instructions; approved OpenSpec change artifacts; canonical specifications; approved design/tasks; validated implementation; authoritative external sources; historical or speculative material. A material same-level conflict returns `BLOCKED`. Reconcile a higher-priority change through the canonical OpenSpec update workflow before affected implementation continues.

OpenSpec owns proposal, specifications, design, tasks, apply, verification, sync, archive, and generated `.agents/skills/openspec-*`. The package owns route selection, context assignment, dependency/ownership coordination, and the selected route's acceptance decision.

## Routes

- Clear, low-risk change: invoke canonical `$openspec-apply-change`; native checks own direct acceptance.
- Material, well-specified change: Implementer invokes canonical `$openspec-apply-change`; fresh Verifier evaluates actual state and may invoke canonical `$openspec-verify-change` for conformance evidence.
- Material discovery uncertainty: Scout resolves scope/ownership/dependencies, then use the material route.
- Read-only OpenSpec analysis: use only the minimum read-only contexts; no implementation cycle.

Canonical verification supplies conformance evidence, not automatic orchestration `PASS`. OpenSpec task checkboxes record implementation progress, not independent acceptance.

## TDD and other frameworks

TDD, repository task systems, Superpowers, and other frameworks provide process order, dependencies, artifacts, and acceptance criteria. The selected portable route assigns contexts and owns its acceptance decision. One active orchestration owner coordinates implementation. If two same-level orchestration owners are active for the same scope, return `BLOCKED` until ownership is resolved.

Normal OpenSpec work does not automatically stack Reviewer, Validator, Final Auditor, and canonical verification. Add one distinct read-only gate only for a recorded risk not covered by the fresh Verifier.

## Drift and preservation

When implementation exposes material specification drift, stop the affected scope and use the canonical OpenSpec update workflow. Installation, upgrade, migration, and both direct/orchestrated apply preserve canonical skill paths and bytes.
