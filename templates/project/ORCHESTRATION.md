# Optional Orchestration Process Input

Use this file only when repository-native instructions and approved framework artifacts do not already state a required process input. Its absence is valid.

## Objective

Reference the user-visible outcome.

## Authority

List governing repository instructions, approved specifications/change artifacts, and canonical system sources. Latest explicit user requirements and repository instructions take precedence; unresolved material same-level conflicts block affected work.

## Process Mode

- `STANDARD`: follow the selected adaptive route and repository-native checks.
- `TDD`: the Implementer records the exact failing behavior/command before implementation and the passing command after implementation; the fresh Verifier checks both against actual state.
- `CUSTOM`: name the external framework and pass its process order as an input without creating a second orchestration owner.

## Dependencies and Ownership

List only dependencies and owned file/subsystem boundaries needed for safe dispatch. Related work should form context-affinity batches. One active writer owns each overlapping boundary.

## Acceptance Criteria

Reference criteria owned by the user, repository, or framework. Direct routes judge them with native checks; orchestrated routes use a fresh Verifier for the independent acceptance decision.

## Validation

List exact project- or framework-native commands when known. A validation command that mutates tracked deliverables becomes implementation and requires fresh verification.
