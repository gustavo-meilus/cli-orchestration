# End-to-End Workflow

## Route selection

```text
request + governing policy
  -> explicit orchestration or high risk? -> Implementer -> fresh Verifier
  -> material discovery uncertainty?      -> Scout -> Implementer -> fresh Verifier
  -> material implementation risk?        -> Implementer -> fresh Verifier
  -> useful read-only parallelism?         -> minimum read-only contexts
  -> clear/local/low-risk/cheap checks?    -> direct execution
  -> otherwise                             -> clarify or Scout
```

Predicates are cumulative: high risk may strengthen verification, and uncertainty may prepend Scout. Read-only work never receives a synthetic Implementer cycle.

## Orchestration boundary

After an orchestrated route is selected, the primary becomes a pure control plane. It dispatches compact packets, sequences dependencies, enforces ownership, routes one rework cycle, and gates acceptance. Workers retain detailed reads, edits, logs, diffs, and reasoning.

Tasks sharing files, concepts, or validation context form one context-affinity batch. One active writer owns overlapping files/subsystems. Independent read-only work may run concurrently.

## Acceptance

- Direct: criteria plus appropriate native checks.
- Ordinary orchestration: fresh Verifier `PASS`.
- High risk: fresh Verifier `PASS` plus only the recorded distinct-risk evidence.
- Worker unavailable: `BLOCKED`, with no silent direct fallback.

Fresh means a new context that did not implement, edit, or own the batch. The model may be the same.

## Rework sequence

```text
Implementer A -> Verifier B: REWORK
             -> same Implementer A (or one recorded replacement)
             -> fresh Verifier C
             -> PASS or cause diagnosis + BLOCKED
```

## OpenSpec

OpenSpec provides the approved artifacts and lifecycle. The route passes the change reference to canonical apply/verify skills rather than rebuilding planning. Native OpenSpec verification is conformance evidence; the fresh Verifier owns orchestration acceptance.
