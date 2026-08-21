## Purpose

Defines minimal deterministic dependency, ownership, validation, and acceptance rules that prevent conflicting work without requiring a separate scheduling service.

## ADDED Requirements

### Requirement: Dependency-ready dispatch
A work item SHALL enter `READY` only when every declared dependency is `DONE`, and the primary orchestrator SHALL dispatch Executors only for `READY` work items.

#### Scenario: Dependency is incomplete
- **WHEN** work item B depends on work item A and A is not `DONE`
- **THEN** B remains non-ready and no Executor is dispatched for B

#### Scenario: All dependencies are accepted
- **WHEN** every dependency of a planned work item has reached `DONE`
- **THEN** the item may transition to `READY`

### Requirement: Single active writer
The portable baseline SHALL permit at most one active source-writing Executor in a repository at a time while allowing independent read-heavy roles to run concurrently.

#### Scenario: Writer is already active
- **WHEN** one Executor is modifying repository source and another write item becomes `READY`
- **THEN** the second item remains queued until the active Executor leaves the writing state

#### Scenario: Independent read-only work exists
- **WHEN** multiple inspections, plans, or reviews are independent and thread capacity is available
- **THEN** the orchestrator may dispatch those read-only roles concurrently

### Requirement: Explicit work ownership
Every planned implementation item SHALL declare owned paths and shared resources, and an Executor SHALL limit changes to that declared scope unless it reports a newly discovered dependency.

#### Scenario: Change remains inside ownership
- **WHEN** an Executor modifies only declared owned paths and resources
- **THEN** the Reviewer evaluates the change normally

#### Scenario: Change exceeds ownership
- **WHEN** an Executor modifies an undeclared path or shared resource
- **THEN** the Reviewer treats it as a scope violation unless a recorded dependency and approved replanning justify it

### Requirement: Auditable role identities
The orchestration ledger SHALL record implementation, review, validation, and final-audit thread identities needed to verify independence.

#### Scenario: Reviewer identity matches implementer
- **WHEN** a review result identifies the same thread as the Executor
- **THEN** that result cannot transition the work item to `DONE`

#### Scenario: Fresh review passes
- **WHEN** a distinct non-implementer Reviewer returns `PASS`
- **THEN** the work item may transition to `DONE`

### Requirement: Exact validation contract
Plans SHALL identify exact applicable validation commands or explicitly state why no mechanical command applies, and the Validator SHALL execute every applicable aggregate command before returning `PASS`.

#### Scenario: Required command succeeds
- **WHEN** the Validator executes a required command and it passes
- **THEN** the Validator records the command and concise evidence reference

#### Scenario: Required command cannot run
- **WHEN** an applicable validation command cannot be executed because of the environment or permissions
- **THEN** the Validator returns `BLOCKED` with the exact limitation rather than treating the check as passed

#### Scenario: Required command fails
- **WHEN** an applicable validation command fails
- **THEN** the Validator returns `FAIL` and associates the failure with affected work items when practical

### Requirement: Acceptance gates
Material implementation SHALL be accepted only after a fresh Reviewer passes every material item, aggregate validation passes, and a fresh Final Auditor passes the combined result.

#### Scenario: Executor completes implementation
- **WHEN** an Executor returns `COMPLETED`
- **THEN** the item transitions to `IMPLEMENTED` rather than directly to `DONE`

#### Scenario: Aggregate result is complete
- **WHEN** all material items are `DONE`, aggregate validation returns `PASS`, and a fresh Final Auditor returns `PASS`
- **THEN** the orchestration task may be reported complete

### Requirement: Optional resumable ledger
For work explicitly designated as cross-session, the system SHALL persist only the compact orchestration ledger and SHALL reconstruct its claims against current repository state before resuming execution.

#### Scenario: Cross-session work is started
- **WHEN** the user or governing process marks a task as resumable
- **THEN** the orchestrator maintains one repository-local state file containing work-item states, dependencies, assignments, blockers, attempt counts, and evidence references without worker transcripts

#### Scenario: Persisted work is resumed
- **WHEN** a later session loads the persisted ledger
- **THEN** an Inspector verifies its baseline and state claims against authoritative artifacts and current repository state before any item is dispatched

