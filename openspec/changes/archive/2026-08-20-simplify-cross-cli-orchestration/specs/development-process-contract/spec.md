## Purpose

Defines a small durable contract for direct tasks, TDD, and external development frameworks without creating a competing specification or orchestration system.

## ADDED Requirements

### Requirement: Optional repository process contract
The system SHALL recognize an optional repository process contract containing the objective, authority references, process mode, work items or derivation guidance, dependencies, acceptance criteria, and validation commands.

#### Scenario: Process contract exists
- **WHEN** an Inspector begins a material task and the repository contains the process contract
- **THEN** the Inspector reads it as governing project input subject to the protocol's authority precedence rules

#### Scenario: Process contract is absent
- **WHEN** no process contract exists
- **THEN** the Inspector derives the work graph from the explicit user objective, repository instructions, approved specifications, current state, and discoverable validation conventions

### Requirement: Supported process modes
The process contract SHALL support `STANDARD`, `TDD`, and `CUSTOM` modes without changing the six-role acceptance workflow.

#### Scenario: Custom framework is selected
- **WHEN** the process mode is `CUSTOM`
- **THEN** the contract identifies the external framework's authoritative artifacts, required gates, definition of done, and validation evidence while the orchestration protocol retains execution and acceptance ownership

### Requirement: TDD evidence contract
For `TDD` work, the Planner SHALL declare the behavior under test plus exact red and green validation commands, and the Executor SHALL return red and green evidence references. Reliable red evidence identifies the exact declared red command executed before implementation and its result demonstrating the intended failure. Reliable green evidence identifies the exact declared green command executed after implementation and its passing result. A command mismatch, incorrect timing, or result that does not meet these criteria is unreliable.

#### Scenario: Valid red-green cycle
- **WHEN** the pre-change command demonstrates the intended failing behavior and the post-change command passes after the smallest implementation change
- **THEN** the Executor records both evidence references and the Reviewer evaluates them against the approved behavior

#### Scenario: Red evidence is absent
- **WHEN** a TDD work item reaches review without reliable evidence of the pre-change failure
- **THEN** the Reviewer returns `REWORK` or `BLOCKED` and SHALL NOT return `PASS`

#### Scenario: Green evidence is absent
- **WHEN** a TDD work item reaches review without reliable evidence that the declared post-change command passes
- **THEN** the Reviewer returns `REWORK` or `BLOCKED` and SHALL NOT return `PASS`

### Requirement: One orchestration owner
The system SHALL permit only one active workflow to own subagent decomposition, implementation dispatch, independent review, and aggregate acceptance for a material change.

#### Scenario: OpenSpec governs intent
- **WHEN** an approved OpenSpec change exists
- **THEN** OpenSpec owns specification intent and lifecycle while this protocol alone owns implementation orchestration and acceptance

#### Scenario: Superpowers provides planning or TDD practices
- **WHEN** Superpowers artifacts or practices are used as input
- **THEN** they may inform the process contract, but Superpowers subagent-driven-development SHALL NOT run concurrently with this protocol's orchestration workflow

#### Scenario: Competing orchestrator is already active
- **WHEN** the Inspector detects another workflow actively owning material execution and review
- **THEN** affected work is reported as `BLOCKED` until the user selects one orchestration owner

### Requirement: Framework independence
The system SHALL NOT require OpenSpec, Superpowers, or any other named development framework for generic material tasks.

#### Scenario: Direct user-defined task
- **WHEN** the user supplies an objective and acceptance criteria without an external framework
- **THEN** the protocol can inspect, plan, execute, independently review, validate, and audit the task using the same role and gate contracts
