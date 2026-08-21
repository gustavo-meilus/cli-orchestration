# Portable Adaptive Orchestration Protocol

Release-Version: 2.0.0
Status: Normative

## 1. Modes and ordered routing

Direct mode lets the active CLI agent perform clear, local, low-risk, cheaply verifiable work. Orchestration mode creates one or more independent worker contexts and makes the primary a pure control plane. The pure boundary begins when orchestration is selected, not before route selection.

Evaluate these cumulative predicates in order; a later predicate cannot weaken an earlier one:

1. **Explicit orchestration** — a user or governing repository instruction requires orchestration or independent review. For implementation, use Implementer → fresh Verifier; add the modifiers below when applicable.
2. **High risk** — security/auth/permissions, destructive data or migration work, concurrency, production infrastructure, financial logic, or public compatibility requires Implementer → stronger fresh Verifier. Add one read-only specialist only for a distinct uncovered risk.
3. **Material uncertainty** — substantive uncertainty about scope, ownership, dependencies, risk, or route choice prepends Scout. The primary does not absorb repository discovery to decide later whether Scout was needed.
4. **Material implementation** — meaningful behavior or regression risk uses Implementer → fresh Verifier.
5. **Useful read-only parallelism** — genuinely independent read-heavy branches use only the minimum read-only contexts whose expected correctness, uncertainty, or wall-clock benefit is material.
6. **Direct execution** — select direct mode only when no earlier predicate applies and work is clear, local, low-risk, and cheaply verifiable.

Read-only analysis, discovery, or review uses only its required read-only contexts and does not manufacture an Implementer or implementation-acceptance cycle.

## 2. Pure control plane

Once an orchestrated route is selected, the primary only dispatches work, coordinates dependencies, tracks compact state, routes bounded rework, and gates completion. Worker contexts own detailed discovery, implementation, logs, diffs, and review reasoning. The primary retains compact decisions, ownership, dependencies, result packets, blockers, and evidence references.

If a required worker cannot be created or isolated, return `BLOCKED` before that responsibility is performed. The route never silently falls back to primary-thread implementation or self-review.

## 3. Normal logical roles

Role semantics are CLI-neutral. Adapters map them to native generic or custom-agent mechanisms; model names and effort levels remain adapter policy.

### Role: Scout

Read-only discovery for material uncertainty. Inspect authoritative sources and actual state; return scope, ownership, dependencies, risk, and recommended route as a compact packet. Source edits invalidate the result.

### Role: Implementer

Own one coherent context-affinity batch. Read authoritative inputs directly, preserve unrelated work, implement the smallest complete delta, run focused checks, and return changed scope, checks, risks, and evidence. Report new dependencies or specification drift instead of silently widening ownership. Never self-approve.

### Role: Verifier

Independently judge an implemented batch against authoritative requirements and actual state. A fresh Verifier is a new context that did not implement, edit, or own the batch; freshness does not require a different model or vendor. Inspect evidence directly, run appropriate checks, and return `PASS`, `REWORK`, or `BLOCKED`. Source edits invalidate the verdict and become implementation requiring another fresh verification.

## 4. Minimum topology and optional assurance

Scout, Implementer, and Verifier are the normal portable roles. Planner, Validator, Final Auditor, Inspector, Reviewer, and specialist contracts are optional high-assurance resources only. Add one when it covers a documented distinct risk or benchmark-demonstrated benefit not covered by the normal route. They never form a universal committee pipeline.

For ordinary material work:

`Implementer -> fresh Verifier`

When material discovery uncertainty exists:

`Scout -> Implementer -> fresh Verifier`

## 5. Ownership, dependencies, and batching

Group work sharing files, concepts, and validation context into one coherent context-affinity batch. Declare objective, authoritative references, dependencies, owned paths or subsystem boundary, acceptance criteria, and expected validation. Dispatch only when dependencies are satisfied.

Only one active writer may own overlapping files or a coupled subsystem boundary. Disjoint read-only work may run concurrently. Disjoint writes require explicit non-overlapping ownership and must still respect shared dependencies; the portable default is one active writer.

## 6. Acceptance and rework

**Direct acceptance:** the active agent completes the stated criteria and appropriate repository- or framework-native checks.

**Orchestrated acceptance:** a fresh Verifier returns `PASS` after checking authoritative artifacts, actual state, regressions, and appropriate validation. A distinct high-risk gate is additional only when recorded during routing.

On the first concrete `REWORK` result, return the defect to the same Implementer when safely available. Otherwise record why and use one replacement Implementer. The corrected output goes to a different fresh Verifier. A second verification failure ends automatic looping and returns a cause diagnosis: specification ambiguity, architecture, task boundary, environment/tooling, or implementation misunderstanding.

## 7. Framework authority

Authority order is:

`latest explicit user requirement > governing repository instructions > approved framework change artifacts > canonical framework/system specifications > approved design/tasks > validated current implementation > authoritative external sources > historical or speculative material`

Material same-level conflicts return `BLOCKED`. TDD, task systems, and development frameworks provide process order, dependencies, artifacts, and acceptance criteria. This protocol assigns contexts and owns only the selected route's acceptance decision.

OpenSpec owns proposal/spec/design/tasks/apply/verify/sync/archive and canonical `.agents/skills/openspec-*`. This package does not edit, copy, package, replace, or shadow those resources. Canonical OpenSpec verification is conformance evidence; an orchestrated route still requires the fresh Verifier's independent acceptance decision.

## 8. Optional resumability

Direct and single-batch work needs no ledger. Cross-session or multiple dependent batches may use `.orchestration/state.json` under `references/state.md`. Persist only identifiers, route, ownership, dependencies, statuses, evidence references, and next gate—never transcripts, specification bodies, raw logs, or worker reasoning.

## 9. Completion

A direct route completes after its criteria and native checks pass. An orchestrated implementation completes only after all dependencies are satisfied, each material batch has a fresh Verifier `PASS`, every recorded distinct risk gate passes, and blockers or field limitations are reported accurately.
