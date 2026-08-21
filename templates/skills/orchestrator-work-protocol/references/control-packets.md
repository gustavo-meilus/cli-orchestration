# Control Packet Contract

Status: Normative

Packets are compact routing records. Workers inspect authoritative files directly; packets never contain full diffs, transcripts, raw logs, copied specification bodies, private reasoning, or broad repository dumps.

## Work packet

`batch id; objective; route; authority refs; dependencies; context-affinity rationale; owned paths/subsystem; shared resources; acceptance criteria; validation expectations; process inputs; distinct risks; permission limits`

Dispatch only after dependencies are accepted and ownership does not conflict. Maintain one active writer for overlapping owned paths or a coupled subsystem boundary. Independent read-only packets may run concurrently.

## Scout result

`batch/request id; result: READY | BLOCKED; authoritative refs; baseline ref; scope; ownership; dependencies; risks; recommended route; unresolved; evidence refs`

## Implementer result

`batch id; context identity; result: COMPLETED | PARTIAL | BLOCKED; changed scope; focused checks; TDD red/green evidence when required; dependencies discovered; unresolved; risks; evidence refs`

## Verifier result

`batch id; context identity; freshness: ELIGIBLE | INELIGIBLE; verdict: PASS | REWORK | BLOCKED; requirement conformance; ownership assessment; regressions; validation assessment; distinct-risk evidence; actionable defects; evidence refs`

The Verifier reads actual state and authority; the Implementer narrative is routing input, not proof.

## Compact result packet

Every result includes only the decision, changed or inspected scope, relevant checks/evidence, remaining risks, and actionable blockers or defects. Detailed worker context remains with the worker or authoritative artifacts.

## Bounded rework packet

First defect: `batch id; original Implementer identity; verifier defect/evidence; correction scope; ownership; validation expectations; rework count: 1`.

Route it to the same Implementer when safely available. Otherwise record the replacement identity and reason. Reworked output must be judged by a different fresh Verifier. A second failed verification returns `BLOCKED` plus cause diagnosis instead of another automatic cycle.

## Optional state projection

For cross-session or multiple dependent batches, project only `workflow id; route; owner; next gate; batch ids/objectives/statuses; dependencies; owned paths; assigned contexts; evidence refs; rework counts` into state v2. Stateless direct and coherent single-batch work is valid.
