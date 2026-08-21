## Purpose

Defines how the framework selects the smallest effective execution topology while preserving a pure control plane whenever independent agent orchestration is used.

## ADDED Requirements

### Requirement: Route work by risk and uncertainty
For implementation work, the framework SHALL select an Implementer followed by fresh Verifier whenever the user or governing repository requires orchestration or the work has meaningful behavior, regression, or high-risk impact; it SHALL prepend Scout when material scope, ownership, dependency, or route-selection uncertainty exists; and it SHALL strengthen verification or add one distinct specialist when an uncovered high-risk concern requires it. These modifiers SHALL combine when more than one applies. For read-only work, orchestration SHALL use only the minimum independent discovery or review contexts needed by the request and SHALL NOT manufacture an implementation stage. Direct execution SHALL be selected only when no orchestration predicate applies and the work is clear, local, low-risk, and cheaply verifiable.

#### Scenario: Clear low-risk work stays direct
- **WHEN** a task is local, unambiguous, low-risk, cheaply verifiable, and not subject to a higher-precedence orchestration predicate
- **THEN** the documented route uses direct execution without requiring a subagent

#### Scenario: User explicitly requests orchestration
- **WHEN** the user or governing repository policy explicitly requires orchestration or independent review
- **THEN** the framework selects an orchestrated route even if the work could otherwise qualify for direct execution

#### Scenario: Material work receives independent verification
- **WHEN** a well-specified task has meaningful behavior or regression risk
- **THEN** the documented route assigns implementation to an Implementer and acceptance to a fresh Verifier

#### Scenario: Discovery uncertainty justifies a Scout
- **WHEN** material uncertainty about scope, ownership, or dependencies would likely cause implementation churn
- **THEN** the documented route adds a read-only Scout before implementation

#### Scenario: Independent read-heavy branches justify orchestration
- **WHEN** genuinely independent read-heavy branches can materially improve uncertainty reduction, correctness, or wall-clock time without write conflicts
- **THEN** the framework SHALL select orchestration and run only those useful branches concurrently

#### Scenario: Orchestrated work is read-only
- **WHEN** the selected task is analysis, discovery, or review and produces no implementation changes
- **THEN** the framework SHALL dispatch only the minimum suitable read-only contexts and SHALL NOT require an Implementer or an implementation-acceptance cycle

#### Scenario: High-risk work receives strengthened verification
- **WHEN** work crosses a security, destructive migration, concurrency, production infrastructure, financial, or public compatibility boundary
- **THEN** the framework selects Implementer followed by a stronger fresh Verifier, prepends Scout when material discovery uncertainty also exists, and adds a separate specialist only for a distinct uncovered risk

### Requirement: Select routes without absorbing worker context
The primary SHALL choose a route from the user request, governing instructions, already-available control information, and explicit risk indicators; when route selection itself requires substantive repository or specification discovery, it SHALL select a read-only Scout rather than performing that discovery in the primary context.

#### Scenario: Visible information is sufficient
- **WHEN** the request and governing instructions establish the applicable route predicates
- **THEN** the primary selects the route without an exploratory worker

#### Scenario: Selection needs substantive discovery
- **WHEN** resolving materiality, ownership, dependencies, or risk would require repository or specification analysis
- **THEN** the primary activates orchestration and delegates that analysis to Scout

### Requirement: Preserve pure orchestration boundaries
When an orchestrated route is selected, the primary agent SHALL act only as a control plane that dispatches work, coordinates dependencies, tracks compact state, routes rework, and gates completion; it SHALL NOT perform worker implementation or substitute its own review for the assigned fresh Verifier.

#### Scenario: Orchestration mode is active
- **WHEN** the route uses one or more worker agents
- **THEN** detailed discovery, implementation, validation logs, diffs, and review reasoning remain in the responsible worker contexts while the primary retains only coordination state

#### Scenario: Direct mode is active
- **WHEN** the route selects direct execution
- **THEN** the primary agent SHALL be permitted to perform the task and its native validation without pretending to be a separate control plane

### Requirement: Use the minimum sufficient topology
The framework SHALL treat Scout, Implementer, and Verifier as the normal portable roles and SHALL add Planner, Validator, Final Auditor, or specialist reviewers only for a distinct risk or demonstrated benefit that is not already covered by the selected route.

#### Scenario: Routine material change
- **WHEN** a material change is adequately specified and has no exceptional risk domain
- **THEN** the route does not add Planner, Validator, Final Auditor, or specialist stages by default

#### Scenario: Distinct high-risk concern
- **WHEN** a security, destructive migration, concurrency, production infrastructure, financial, or public compatibility concern needs separate expertise
- **THEN** the route SHALL use a stronger Verifier or add a targeted read-only specialist only for the uncovered concern and SHALL record the reason

### Requirement: Batch by context affinity
The framework SHALL group related work that shares files, concepts, or validation context into coherent worker batches instead of mapping every task-list checkbox to a fresh agent session.

#### Scenario: Related tasks share implementation context
- **WHEN** several ready tasks touch the same subsystem and can be owned safely by one writer
- **THEN** they are eligible for one coherent Implementer batch with focused validation

#### Scenario: Independent read-heavy branches exist
- **WHEN** multiple discovery or review branches have no write conflicts or unmet dependencies
- **THEN** the control plane SHALL be permitted to run them concurrently and merge only their compact findings

### Requirement: Keep model and stage choices evidence-driven
The framework SHALL express logical roles independently of vendor model names and SHALL require representative benchmark evidence before a model assignment or additional stage is promoted to a portable default.

#### Scenario: Adapter supplies native agent settings
- **WHEN** a CLI adapter maps a logical role to a model or reasoning setting
- **THEN** that mapping remains adapter configuration rather than a canonical protocol requirement

#### Scenario: Proposed default adds orchestration cost
- **WHEN** a new stage or stronger model is proposed as a default
- **THEN** its measured effect on correctness, latency, token or cost use, and rework is documented before promotion
