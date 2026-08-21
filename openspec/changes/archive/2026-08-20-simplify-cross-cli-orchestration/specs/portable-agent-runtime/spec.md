## Purpose

Defines a portable subagent execution contract that preserves independent orchestration roles while minimizing platform-specific agent configuration.

## ADDED Requirements

### Requirement: Portable generic-agent mapping
The system SHALL define one built-in generic subagent mapping for every supported CLI and SHALL use that mapping as the baseline runtime for all logical orchestration roles.

#### Scenario: Codex selects its generic agent
- **WHEN** the orchestration protocol dispatches a role through Codex
- **THEN** it selects the built-in `default` subagent type unless an enabled native hardening profile is explicitly selected

#### Scenario: Claude Code selects its generic agent
- **WHEN** the orchestration protocol dispatches a role through Claude Code
- **THEN** it selects the built-in `general-purpose` subagent type

#### Scenario: Copilot CLI selects its generic agent
- **WHEN** the orchestration protocol dispatches a role through Copilot CLI
- **THEN** it selects the built-in `general-purpose` subagent type

### Requirement: Logical role preservation
The system SHALL preserve Inspector, Planner, Executor, Reviewer, Validator, and Final Auditor as distinct logical contracts regardless of the generic subagent type that executes them.

#### Scenario: Generic agent receives one bounded role
- **WHEN** the primary orchestrator dispatches a generic subagent
- **THEN** the dispatch identifies exactly one logical role, includes that role's bounded responsibilities and required output packet, and excludes responsibilities owned by other roles

### Requirement: Canonical role definitions
The system SHALL maintain one canonical definition for each logical role and SHALL keep CLI adapters limited to platform invocation syntax and capability mappings.

#### Scenario: Adapter selects a role
- **WHEN** a CLI adapter dispatches a Reviewer
- **THEN** it references the canonical Reviewer contract rather than maintaining a divergent platform-specific Reviewer definition

### Requirement: Fresh-thread independence
The system SHALL run each Reviewer and Final Auditor in a fresh thread that did not implement the state it judges.

#### Scenario: Work item enters review
- **WHEN** an Executor reports a material work item as implemented
- **THEN** the orchestrator dispatches a new generic-agent thread as Reviewer and records a thread identity different from the Executor identity

#### Scenario: Aggregate work enters final audit
- **WHEN** aggregate validation passes
- **THEN** the orchestrator dispatches a new generic-agent thread as Final Auditor whose identity differs from every implementation thread

### Requirement: Optional native hardening
The system MAY provide CLI-native custom-agent profiles for permission restrictions, model selection, or reasoning tuning, but those profiles SHALL implement the same canonical role contracts and SHALL NOT be required for baseline portability.

#### Scenario: Native profile is absent
- **WHEN** a supported CLI has no installed custom profile for a logical role
- **THEN** the role remains executable through that CLI's generic-agent mapping

#### Scenario: Native profile is enabled
- **WHEN** a user enables a native custom profile
- **THEN** the profile preserves the role's canonical responsibilities, output packet, independence rules, and acceptance semantics

### Requirement: Full-capability generic-agent safety
The system SHALL treat no-edit and bounded-write rules as semantic requirements even when a generic agent technically has broader tools.

#### Scenario: Read-only logical role has editing tools
- **WHEN** an Inspector, Planner, Reviewer, or Final Auditor is executed by a full-capability generic agent
- **THEN** its role contract prohibits source edits and any observed source edit prevents acceptance of that role result

