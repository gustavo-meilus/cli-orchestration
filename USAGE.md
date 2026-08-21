# Usage

## Choose the route

- Direct: clear, local, low-risk, cheaply verifiable, and no orchestration trigger.
- Implementer → fresh Verifier: well-specified material behavior or regression risk, or explicit orchestration.
- Scout → Implementer → fresh Verifier: material uncertainty about route, scope, ownership, dependencies, or risk.
- Read-only orchestration: only the minimum independent analysis/review contexts; no manufactured implementation cycle.
- High assurance: strengthen the fresh Verifier or add one specialist for a recorded distinct risk.

If a required worker cannot be created, stop with `BLOCKED` and name the missing capability.

## Dispatch a material batch

Invoke the native form of `orchestrator-work-protocol`. Give each worker a compact packet containing the objective, authority references, dependencies, context-affinity boundary, ownership, criteria, checks, and risks. Keep one active writer per overlapping boundary.

The Implementer edits and runs focused checks. A fresh Verifier reads authority and actual state directly. A model change is optional; a new non-implementer context is mandatory.

## Rework

Send the first concrete defect to the same Implementer when safe. Use one recorded replacement only when the original is unavailable or no longer owns the scope. Send corrected output to a different fresh Verifier. After a second failure, classify the cause and stop automatic looping.

## OpenSpec

Direct qualifying change:

```text
$openspec-apply-change my-change
```

Material orchestrated change:

```text
$openspec-orchestrated-apply my-change
```

The Implementer still invokes canonical OpenSpec apply. The fresh Verifier may invoke canonical OpenSpec verify as evidence. Sync and archive remain canonical OpenSpec actions.

## Optional state

Do not create state for direct or coherent single-batch work. For cross-session or multiple dependent batches, use state v2:

```bash
python .agents/skills/orchestrator-work-protocol/scripts/state.py .orchestration/state.json
```

Migrated v1 claims always enter `RECONCILE`; they never inherit acceptance.
