## Purpose

Defines truthful, minimal installation and verification behavior for distributing the same orchestration contract across Codex, Claude Code, and Copilot CLI.

## ADDED Requirements

### Requirement: Explicit supported-tool declaration
The package manifest SHALL list every supported CLI, and documentation SHALL distinguish supported, experimental, and unsupported adapters.

#### Scenario: Adapter is not verified
- **WHEN** a CLI adapter has not passed its required installation and discovery checks
- **THEN** the CLI is not listed as supported

#### Scenario: Adapter is verified
- **WHEN** a CLI adapter passes its required checks on a documented current CLI version
- **THEN** the manifest and documentation may list that CLI as supported with the verification date and version

### Requirement: Tool-selective installation
The installer SHALL accept exactly one target CLI per invocation, default to Codex for backward compatibility, and install only resources owned by the selected adapter.

#### Scenario: No tool is specified
- **WHEN** the installer is invoked without a target-tool option
- **THEN** it performs the Codex installation behavior

#### Scenario: Claude Code is selected
- **WHEN** the installer targets Claude Code
- **THEN** it installs a `CLAUDE.md` bridge, Claude-discoverable orchestration skill resources, and the canonical shared protocol without installing Codex or Copilot agent profiles

#### Scenario: Copilot CLI is selected
- **WHEN** the installer targets Copilot CLI
- **THEN** it installs Copilot-discoverable instructions and skill resources plus the canonical shared protocol without installing Codex or Claude agent profiles

### Requirement: Thin platform adapters
Each CLI adapter SHALL define only the generic-agent name, dispatch syntax, skill/instruction discovery locations, and unavoidable platform limitations.

#### Scenario: Adapter dispatches a role
- **WHEN** an adapter receives a canonical role contract and bounded task
- **THEN** it launches the mapped generic subagent with that contract and requires the canonical control packet as its result

#### Scenario: Platform has native custom profiles
- **WHEN** optional native hardening profiles are installed
- **THEN** the adapter may select them without changing canonical workflow states or acceptance gates

### Requirement: Normative orchestration avoids experimental schedulers
Baseline support SHALL use ordinary first-level subagents and SHALL NOT depend on Claude Code agent teams or Copilot CLI Fleet for dependency scheduling or acceptance.

#### Scenario: Claude Code executes the protocol
- **WHEN** the Claude adapter runs a material workflow
- **THEN** the primary conversation directly dispatches ordinary subagents and maintains protocol state without requiring agent teams

#### Scenario: Copilot CLI executes the protocol
- **WHEN** the Copilot adapter runs a material workflow
- **THEN** the primary agent directly dispatches the required logical roles and does not delegate normative decomposition or acceptance to Fleet

### Requirement: Tool-aware verification
The verifier SHALL validate the selected adapter's required files, parseable metadata, managed ownership, generic-agent mapping, canonical role availability, and repeated-install idempotence.

#### Scenario: Static adapter verification succeeds
- **WHEN** an installation contains all selected-tool resources with valid syntax and consistent ownership metadata
- **THEN** the verifier reports static verification success

#### Scenario: Required adapter resource is missing
- **WHEN** a selected-tool resource or canonical role contract is missing or malformed
- **THEN** the verifier reports failure with the missing or invalid resource

### Requirement: CLI discovery smoke test
Each supported adapter SHALL have a documented smoke test that starts a fresh CLI process and confirms discovery of the orchestration skill, generic-agent mapping, and role dispatch contract.

#### Scenario: Support promotion
- **WHEN** static verification passes but the fresh-process discovery smoke test has not passed
- **THEN** the adapter remains experimental rather than supported

#### Scenario: Repeated installation
- **WHEN** the same adapter is installed twice into an unchanged target
- **THEN** the second installation produces no managed-content changes and verification still passes

