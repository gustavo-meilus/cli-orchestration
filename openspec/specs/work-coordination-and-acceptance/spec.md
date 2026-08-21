# Work Coordination and Acceptance Specification

## Purpose

Defines conflict-safe ownership, dependency-aware dispatch, route-specific acceptance, bounded rework, and optional recovery for coordinated development work.

## Requirements

### Requirement: Maintain one active writer per ownership boundary
The orchestrator SHALL assign a single active writer to any overlapping file or subsystem ownership boundary and SHALL permit parallel work only when ownership is disjoint or the work is read-only.

#### Scenario: Write scopes overlap
- **WHEN** two ready tasks would modify the same file or coupled ownership boundary
- **THEN** the orchestrator serializes them or assigns them to one coherent Implementer batch

#### Scenario: Work is independent and read-only
- **WHEN** multiple tasks only inspect disjoint or shared material without modifying it
- **THEN** they SHALL be permitted to execute concurrently

### Requirement: Respect dependencies before dispatch
The orchestrator SHALL dispatch a work unit only after its required inputs are available and SHALL pass explicit ownership, dependencies, acceptance criteria, and validation expectations to the responsible worker.

#### Scenario: Dependency is incomplete
- **WHEN** a task depends on an unfinished artifact or implementation result
- **THEN** it remains undispatched until that dependency is satisfied or the plan is explicitly revised

#### Scenario: Work becomes ready
- **WHEN** required inputs are complete and ownership does not conflict
- **THEN** the control plane SHALL be permitted to dispatch the work with a compact, self-contained packet

### Requirement: Apply route-specific acceptance
Direct low-risk work SHALL be accepted using appropriate repository-native or framework-native validation, ordinary orchestrated work SHALL require a PASS from a fresh Verifier, and extra gates SHALL be limited to documented high-risk concerns.

#### Scenario: Direct task completes
- **WHEN** a direct low-risk task satisfies its acceptance criteria and appropriate native checks pass
- **THEN** it SHALL be permitted to complete without manufacturing an independent review stage

#### Scenario: Orchestrated implementation completes
- **WHEN** an Implementer reports a completed material batch
- **THEN** a fresh Verifier independently checks artifact conformance, material regressions, and appropriate validation before acceptance

#### Scenario: High-risk route defines an additional gate
- **WHEN** route selection records a distinct high-risk concern not covered by the normal fresh Verifier
- **THEN** acceptance requires both fresh Verifier PASS and the recorded concern-specific evidence or specialist gate

#### Scenario: Verification mutates tracked output
- **WHEN** a purported validation step changes tracked source or generated deliverables
- **THEN** the mutation is treated as implementation and the affected output is independently reverified

### Requirement: Define fresh independent verification
A fresh Verifier SHALL run in a new agent context that did not implement, edit, or own the batch being judged, SHALL inspect authoritative artifacts and actual resulting state directly, and SHALL NOT rely on the Implementer's narrative as proof. Freshness SHALL NOT require a different model or vendor.

#### Scenario: Verifier has implementation involvement
- **WHEN** a proposed Verifier implemented, edited, or owned any part of the batch under review
- **THEN** that context is ineligible to provide the acceptance PASS

#### Scenario: New context uses the same model
- **WHEN** a new non-implementer context uses the same model family as the Implementer
- **THEN** it remains eligible as a fresh Verifier if every independence condition is satisfied

### Requirement: Bound rework and diagnose repeated failure
After a Verifier reports a concrete defect, the orchestrator SHALL route the defect to the same Implementer when that context remains available and ownership-compatible and SHALL otherwise use one recorded replacement Implementer; it SHALL use a fresh Verifier for the reworked output and, after one failed rework cycle, SHALL stop automatic looping and diagnose the cause.

#### Scenario: First verification finds a defect
- **WHEN** a fresh Verifier returns a reproducible, in-scope defect
- **THEN** the same Implementer receives the defect and evidence for one focused rework cycle

#### Scenario: Original Implementer cannot safely perform rework
- **WHEN** the original Implementer context is unavailable, has crossed an independence boundary, or no longer owns the affected scope
- **THEN** the control plane records the reason and assigns one replacement Implementer a self-contained correction packet without adding another automatic rework cycle

#### Scenario: Rework is submitted
- **WHEN** the Implementer completes the focused correction
- **THEN** a different fresh Verifier evaluates the updated result

#### Scenario: Reverification fails
- **WHEN** the fresh reverification still fails
- **THEN** the control plane classifies whether the cause is specification ambiguity, architecture, task boundary, environment or tooling, or implementation misunderstanding and surfaces the blocker instead of spawning an unbounded loop

### Requirement: Keep resumability proportional
The framework SHALL support compact durable coordination state when a workflow explicitly spans sessions or multiple dependent batches, but SHALL NOT require a state ledger for direct or single-batch work.

#### Scenario: Workflow is short-lived
- **WHEN** a task completes within one direct or coherent worker session
- **THEN** no durable orchestration ledger is required

#### Scenario: Workflow must resume
- **WHEN** execution crosses sessions or contains multiple dependent dispatched batches
- **THEN** persisted state records only the route, work identities, ownership, dependencies, statuses, evidence pointers, and next gate needed to resume safely

#### Scenario: Legacy state is encountered
- **WHEN** resumption encounters a valid ledger from the superseded six-role state schema
- **THEN** the framework preserves the original, converts only unambiguous claims into the current compact schema, and requires fresh reconciliation before dispatch

#### Scenario: Legacy state cannot be converted safely
- **WHEN** a legacy ledger is invalid or contains claims that cannot be mapped without guessing
- **THEN** resumption is blocked with an actionable recovery path and the original state remains recoverable

### Requirement: Fail closed when required orchestration is unavailable
When a selected route requires an independent worker that the active CLI cannot create or isolate, the framework SHALL return an actionable BLOCKED result and SHALL NOT silently execute the work directly or self-verify in the primary context.

#### Scenario: Required generic agent cannot be created
- **WHEN** the active CLI cannot create the Implementer, Scout, Verifier, or required specialist context selected by the route
- **THEN** the route stops before the missing responsibility is performed and reports the unavailable capability

### Requirement: Preserve evidence without context fan-out
Workers SHALL return compact result packets containing decisions, changed scope, validation evidence, remaining risks, and actionable defects, while detailed logs remain outside the primary control-plane context unless needed for a decision.

#### Scenario: Worker completes a batch
- **WHEN** a Scout, Implementer, or Verifier reports to the control plane
- **THEN** the report is sufficient to route the next action without replaying the worker's full context
