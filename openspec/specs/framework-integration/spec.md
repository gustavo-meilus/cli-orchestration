# Framework Integration Specification

## Purpose

Defines how the pure orchestrator composes with canonical development frameworks without taking ownership of their artifacts, lifecycle, or methodology.

## Requirements

### Requirement: Preserve framework authority
The orchestration layer SHALL preserve this authority precedence: latest explicit user requirement, applicable governing repository instructions, approved framework change artifacts, canonical framework or system specifications, approved design and task artifacts, validated current implementation, authoritative external sources, and historical or speculative material. It SHALL limit itself to selecting and coordinating execution contexts around the governing workflow and SHALL block affected work when material sources at the same unresolved authority level conflict.

#### Scenario: Canonical workflow is already specified
- **WHEN** approved framework artifacts already provide sufficient requirements, design, tasks, and validation guidance
- **THEN** the orchestrator passes authoritative references to the selected route without rebuilding equivalent planning or copying detailed artifact bodies through the primary context

#### Scenario: Explicit authority overrides a framework artifact
- **WHEN** a latest explicit user requirement or governing repository instruction conflicts with an older framework artifact
- **THEN** the higher-precedence requirement governs and the framework artifact is reconciled through its canonical update workflow before affected implementation continues

#### Scenario: Authority conflict remains unresolved
- **WHEN** material governing sources conflict and the precedence order does not resolve them
- **THEN** affected work is blocked for clarification rather than allowing implementation to choose a source of truth

#### Scenario: Framework is not installed
- **WHEN** a repository does not provide an optional integrated framework
- **THEN** the portable orchestration protocol remains usable for direct tasks and repository-native processes

### Requirement: Keep OpenSpec canonical
The package SHALL treat OpenSpec as the owner of proposal, specification, design, tasks, apply, verification, sync, and archive operations and SHALL NOT edit, copy, replace, or package canonical `.agents/skills/openspec-*` resources.

#### Scenario: OpenSpec-managed skills are present
- **WHEN** installation, migration, or upgrade encounters canonical `openspec-*` skills
- **THEN** their paths and bytes remain unchanged

#### Scenario: OpenSpec change is clear and low-risk
- **WHEN** an approved OpenSpec change qualifies for direct execution
- **THEN** the route SHALL be permitted to invoke canonical OpenSpec apply directly and use the change's appropriate native checks

#### Scenario: OpenSpec change is materially risky
- **WHEN** an approved OpenSpec change requires orchestration
- **THEN** the Implementer uses the canonical apply workflow and a fresh Verifier uses canonical OpenSpec verification as conformance evidence when available and materially useful

### Requirement: Separate framework conformance from orchestration acceptance
Canonical framework verification SHALL remain owned by the integrated framework and SHALL produce conformance evidence; the selected execution route SHALL own the independent decision that the implemented result meets its acceptance gate. Framework task progress or conformance evidence SHALL NOT by itself substitute for a required fresh Verifier PASS.

#### Scenario: Direct framework work is accepted
- **WHEN** a direct low-risk route completes the framework operation and appropriate native checks satisfy the governing acceptance criteria
- **THEN** the direct route SHALL be permitted to accept the result without manufacturing a separate orchestration gate

#### Scenario: Orchestrated framework work is accepted
- **WHEN** canonical framework verification passes for work assigned to an orchestrated route
- **THEN** the fresh Verifier evaluates that evidence together with authoritative artifacts and actual repository state before returning PASS

#### Scenario: Framework verification fails
- **WHEN** canonical framework verification reports a material conformance failure
- **THEN** the fresh Verifier cannot return PASS until the failure is resolved or classified as an explicit blocker

### Requirement: Avoid duplicate process ownership
The orchestrator SHALL identify one source of truth for requirements and acceptance criteria, and one route-owned acceptance decision, and SHALL NOT stack semantically overlapping framework verification, Reviewer, Validator, and Final Auditor stages unless each added gate covers a documented distinct risk.

#### Scenario: Framework provides sufficient acceptance checks
- **WHEN** native framework verification plus the selected route covers the stated acceptance criteria
- **THEN** no equivalent generic validation stage is required

#### Scenario: Extra gate covers a separate risk
- **WHEN** an additional gate is introduced for a distinct risk domain
- **THEN** the route records that risk and the unique acceptance evidence expected from the gate

### Requirement: Compose with TDD and external development frameworks
The orchestration layer SHALL accept test-driven development, task systems, and other development frameworks as process inputs without redefining their semantics, and SHALL assign their work through the same adaptive routing and ownership rules.

#### Scenario: Repository mandates test-driven development
- **WHEN** repository instructions require tests before implementation
- **THEN** the selected worker follows that order while orchestration continues to govern only context assignment, dependencies, and acceptance

#### Scenario: External task system defines dependencies
- **WHEN** a task system supplies authoritative readiness or dependency data
- **THEN** the orchestrator consumes that data rather than creating a competing dependency graph

### Requirement: Framework integrations remain optional
The package SHALL keep framework-specific bridges isolated from the portable core so that adding, removing, or upgrading an integration does not change the core role and packet contracts.

#### Scenario: Framework adapter is upgraded
- **WHEN** an integration changes its commands or artifact schema
- **THEN** only the integration boundary and its compatibility evidence need change unless the portable behavior contract itself changed
