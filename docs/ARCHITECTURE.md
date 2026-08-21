# Architecture

## Portable core

The two package-owned skills and their references define route semantics, logical roles, compact packets, acceptance, framework boundaries, and optional state. They contain no vendor model catalog or CLI invocation syntax.

## Direct plane and pure control plane

Direct mode is ordinary CLI work: the active agent may inspect, edit, and validate. Orchestration mode begins when an independent context is selected. From that point the primary is only a control plane; Scout, Implementer, Verifier, or a justified specialist owns substantive work.

This boundary preserves the project's pure-orchestrator identity without requiring orchestration when it adds no material value.

## Thin adapters

Each adapter owns only native instruction/skill discovery, invocation syntax, generic-worker mapping, fail-closed behavior, and optional hardening. Every adapter maps to the same Scout/Implementer/Verifier contracts.

The distribution has one source copy of the portable core. Installation places it in each selected CLI's required discovery root; multiple CLI selections do not create competing protocol definitions.

## Ownership and state

Context-affinity batches keep warm implementation context. One writer owns any overlapping boundary. Optional state v2 records only route, batch identity, ownership, dependencies, status, evidence pointers, rework count, and next gate. It is a resumability claim reconciled against current authority before dispatch.

## Framework boundary

Development frameworks own their artifacts, semantics, and acceptance criteria. The portable layer owns context assignment and route acceptance. OpenSpec-generated skills are outside package ownership and protected by byte-preservation fixtures.
