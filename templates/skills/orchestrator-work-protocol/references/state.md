# Optional Resumable State

Use `.orchestration/state.json` only when orchestration explicitly crosses sessions or has multiple dependent dispatched batches. Direct and coherent single-batch work remains stateless.

Validate state with:

```bash
python .agents/skills/orchestrator-work-protocol/scripts/state.py .orchestration/state.json
```

State is a compact claim, not authority. Resume only after fresh reconciliation of route, current files, dependencies, ownership, statuses, evidence references, and next gate.

## State v2

The strict schema stores `schema_version`, `workflow_id`, `route`, `owner`, `next_gate`, and compact batches. It excludes transcripts, raw logs, specification bodies, detailed plans, and worker reasoning. At most one overlapping writer may be active; `READY` dependencies must be accepted; rework count cannot exceed the one automatic cycle.

## Legacy v1 migration

Preserve the original file before conversion. Convert only unambiguous claims from an object with schema version 1 and a valid item list whose identifiers, objectives, dependencies, ownership, evidence references, and rework counts can be read without guessing. Every converted item receives `RECONCILE`, never inherited acceptance, plus a `legacy:preserved-claim` evidence marker.

Ambiguous or invalid legacy state returns actionable `BLOCKED` and remains recoverable. After conversion, fresh reconciliation is mandatory before dispatch.

```bash
python .agents/skills/orchestrator-work-protocol/scripts/state.py legacy.json --migrate-legacy migrated.json --workflow-id my-change
```
