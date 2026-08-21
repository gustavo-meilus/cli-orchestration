# Multi-CLI Distribution Specification

## Purpose

Defines a portable distribution that exposes the same logical orchestration behavior through thin, verifiable adapters for Codex CLI, Claude Code, and GitHub Copilot CLI.

## Requirements

### Requirement: Maintain a CLI-neutral portable core
The package SHALL define roles, routing, coordination packets, acceptance semantics, and framework boundaries independently of any one CLI's configuration syntax, model catalog, or invocation mechanism.

#### Scenario: Different CLIs invoke workers differently
- **WHEN** Codex CLI, Claude Code, and Copilot CLI use different native agent or instruction mechanisms
- **THEN** each adapter maps those mechanisms to the same portable logical behavior without forking the core protocol

### Requirement: Provide thin selected-tool adapters
The distribution SHALL provide isolated adapters for Codex CLI, Claude Code, and Copilot CLI and SHALL install only the adapters selected by the user. When no tool selection is supplied, the installer SHALL select Codex as the backward-compatible default.

#### Scenario: User selects one CLI
- **WHEN** installation specifies a supported CLI target
- **THEN** the installer deploys the portable core and only that target's adapter resources

#### Scenario: User selects multiple CLIs
- **WHEN** installation specifies more than one CLI target
- **THEN** each selected adapter is installed without overwriting another adapter or duplicating the portable core

#### Scenario: User omits tool selection
- **WHEN** installation receives no CLI target selection
- **THEN** it installs the portable core and Codex adapter only and reports that compatibility default

### Requirement: Verify native discoverability and invocation
For each selected CLI, the verifier SHALL check resource placement, parseable native configuration, logical-role mapping, and explicit orchestration entry points; a CLI SHALL NOT be declared supported based only on file-copy success.

#### Scenario: Static installation succeeds but native loading fails
- **WHEN** files exist at the expected destination but a fresh CLI process cannot discover or invoke the adapter
- **THEN** verification fails the support smoke check, retains the adapter status as `experimental`, and records the actionable failure

#### Scenario: Fresh-process smoke passes
- **WHEN** a clean installed fixture is discovered and its orchestration entry point can exercise the expected native mapping
- **THEN** the verifier records the evidence needed for support-status evaluation

### Requirement: Use evidence-based support status
Each CLI integration SHALL declare exactly `experimental` or `supported`. The package manifest SHALL be the support-evidence source of truth and SHALL record the authoritative source references and verification date, tested CLI version, and fresh-process smoke result. Promotion to `supported` SHALL require current authoritative documentation plus repeatable fresh-process smoke evidence for the claimed behavior.

#### Scenario: Documentation or CLI behavior changes
- **WHEN** a previously relied-on command, schema, agent mechanism, or discovery path is no longer current
- **THEN** compatibility claims are revalidated and the status is downgraded if the evidence no longer holds

#### Scenario: Documentation and manifest disagree
- **WHEN** narrative documentation claims a support or smoke result that differs from the manifest evidence record
- **THEN** verification fails until the narrative is reconciled to the manifest

#### Scenario: Model mapping is provisional
- **WHEN** an adapter recommends a model or reasoning setting
- **THEN** the recommendation is labeled as adapter policy and remains subject to benchmark and current-product revalidation

### Requirement: Install and migrate safely
Installation, repeat installation, upgrade, verification, and legacy migration SHALL be deterministic, preserve unrelated user files, protect canonical OpenSpec-owned resources, and provide a recoverable path for replaced package-owned files.

#### Scenario: Existing installation is upgraded
- **WHEN** package-owned resources from a prior orchestration version are present
- **THEN** migration reconciles or retires them without altering unrelated files or canonical `openspec-*` skills

#### Scenario: Existing public entry points are upgraded
- **WHEN** an installation already invokes the logical `orchestrator-work-protocol` or `openspec-orchestrated-apply` entry through an adapter's native syntax
- **THEN** those logical names and native adapter invocations remain available while their default execution behavior adopts the adaptive topology

#### Scenario: Installation is repeated
- **WHEN** the same selected-tool package is installed again
- **THEN** the resulting managed files and manifest are equivalent and verification succeeds

#### Scenario: Source files carry restrictive attributes
- **WHEN** a copied package source is read-only or inherits restrictive filesystem attributes
- **THEN** replacement of package-owned destination files remains safe and repeatable or fails with an actionable message without partial corruption

### Requirement: Align public version surfaces
Breaking release `2.0.0` SHALL appear as the one package release version across `VERSION`, manifest, protocol header, README, changelog, generated checksums, and verification output so users do not need to infer compatibility between independently numbered public surfaces.

#### Scenario: Version surfaces disagree
- **WHEN** verification observes different package release versions across managed public surfaces
- **THEN** package verification fails with the disagreeing locations

### Requirement: Keep native hardening optional
CLI-specific safety hooks or native hardening profiles SHALL remain optional extensions and SHALL NOT be prerequisites for the portable orchestration protocol.

#### Scenario: Native hardening is unavailable
- **WHEN** a target CLI lacks an equivalent hook or policy mechanism
- **THEN** the portable core and its support status are evaluated independently from that optional hardening feature
