# Graph Report - C:\Users\gmeil\Github\cli-orchestration  (2026-08-16)

## Corpus Check
- Corpus is ~8,309 words - fits in a single context window. You may not need a graph.

## Summary
- 98 nodes · 116 edges · 19 communities (11 shown, 8 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 12 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Protocol Governance and Gates
- OpenSpec Integration
- Package Manifest and Ownership
- Installer Implementation
- Control and Work Plane Workflow
- Agent Role Templates
- Installation Verification
- Pure-Orchestrator Rationale
- Source Verification
- POSIX Installer Wrapper
- POSIX Verifier Wrapper
- Adoption Plan Overview
- Adoption Phases
- Framework Independence
- Package Ownership Model
- Bounded Rework
- Generic Material Workflow

## God Nodes (most connected - your core abstractions)
1. `Universal Codex CLI Pure-Orchestrator Work Protocol` - 11 edges
2. `owned_agent_files` - 7 edges
3. `main()` - 7 edges
4. `backup()` - 6 edges
5. `Codex CLI and OpenSpec Pure-Orchestration Standard` - 6 edges
6. `OpenSpec Integration` - 6 edges
7. `OpenSpec Orchestrated Apply Skill` - 6 edges
8. `Orchestrator Work Protocol Skill` - 6 edges
9. `write_owned_file()` - 5 edges
10. `Codex Orchestration Standard Policy Block` - 5 edges

## Surprising Connections (you probably didn't know these)
- `Material Work State Flow` --semantically_similar_to--> `Normative Material Workflow`  [INFERRED] [semantically similar]
  docs/WORKFLOW.md → templates/skills/orchestrator-work-protocol/references/protocol.md
- `OpenSpec Initialization and Update` --conceptually_related_to--> `OpenSpec Orchestrated Apply Skill`  [INFERRED]
  INSTALL.md → templates/skills/openspec-orchestrated-apply/SKILL.md
- `Version 1.1.0 Pure-Orchestrator Changes` --conceptually_related_to--> `Pure Control-Plane Orchestrator`  [INFERRED]
  CHANGELOG.md → README.md
- `Codex CLI and OpenSpec Pure-Orchestration Standard` --references--> `Installation Guide`  [EXTRACTED]
  README.md → INSTALL.md
- `Codex CLI and OpenSpec Pure-Orchestration Standard` --references--> `OpenSpec Integration`  [EXTRACTED]
  README.md → docs/OPENSPEC-INTEGRATION.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Pure-Orchestration Control and Work Planes** — readme_pure_control_plane_orchestrator, docs_architecture_control_plane, docs_architecture_work_plane, templates_skills_orchestrator_work_protocol_references_protocol_role_separation [INFERRED 0.95]
- **Independent Material and Aggregate Acceptance Gates** — templates_project_agents_block_material_acceptance_policy, docs_workflow_review_independence, templates_skills_orchestrator_work_protocol_references_protocol_acceptance_gates, templates_skills_openspec_orchestrated_apply_skill_acceptance_mapping [INFERRED 0.95]
- **OpenSpec Intent and Orchestration Execution Responsibility Model** — docs_openspec_integration_responsibility_split, templates_skills_openspec_orchestrated_apply_references_workflow_authority_set, templates_skills_openspec_orchestrated_apply_references_workflow_no_competing_planning_layer [INFERRED 0.95]

## Communities (19 total, 8 thin omitted)

### Community 0 - "Protocol Governance and Gates"
Cohesion: 0.20
Nodes (15): Governance, Normative Process Sources, Role Instructions and Runtime Permission Boundary, Troubleshooting, Codex Orchestration Standard Policy Block, Material Acceptance Policy, Compact Evidence Handoff, Control Packet Contract (+7 more)

### Community 1 - "OpenSpec Integration"
Cohesion: 0.16
Nodes (14): Package and OpenSpec Ownership Boundary, OpenSpec Progress Versus Orchestration Acceptance, OpenSpec Integration, OpenSpec and Orchestration Responsibility Split, Specification Drift Reconciliation, Installation Guide, User and Project Installation Scopes, OpenSpec Initialization and Update (+6 more)

### Community 2 - "Package Manifest and Ownership"
Cohesion: 0.15
Nodes (12): architecture, default_max_concurrent_threads_per_session, managed_agents_md_markers, name, openspec_generated_files_owned_by_package, owned_skills, verified_date, version (+4 more)

### Community 3 - "Installer Implementation"
Cohesion: 0.41
Nodes (11): backup(), copy_owned_tree(), main(), parse_args(), Namespace, Path, run_openspec_init(), stamp() (+3 more)

### Community 4 - "Control and Work Plane Workflow"
Cohesion: 0.20
Nodes (11): Architecture, Context Isolation Without Transcript Relay, Primary Thread Control Plane, Subagent Work Plane, End-to-End Workflow, Material Work State Flow, Fresh Review Independence, Codex CLI and OpenSpec Pure-Orchestration Standard (+3 more)

### Community 5 - "Agent Role Templates"
Cohesion: 0.29
Nodes (7): owned_agent_files, executor.toml, final-auditor.toml, inspector.toml, planner.toml, reviewer.toml, validator.toml

### Community 6 - "Installation Verification"
Cohesion: 0.47
Nodes (5): check_skill(), main(), parse_args(), Namespace, Path

### Community 7 - "Pure-Orchestrator Rationale"
Cohesion: 0.40
Nodes (5): Changelog, Version 1.1.0 Pure-Orchestrator Changes, Primary Control-Plane Invariant, Keep Noisy Work in Subagents, Pure Control-Plane Orchestrator

### Community 8 - "Source Verification"
Cohesion: 0.67
Nodes (3): Verified Codex Sources, Verified OpenSpec Sources, Source Verification

## Knowledge Gaps
- **34 isolated node(s):** `name`, `version`, `verified_date`, `inspector.toml`, `planner.toml` (+29 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Codex CLI and OpenSpec Pure-Orchestration Standard` connect `Control and Work Plane Workflow` to `OpenSpec Integration`, `Pure-Orchestrator Rationale`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Why does `OpenSpec Integration` connect `OpenSpec Integration` to `Protocol Governance and Gates`, `Control and Work Plane Workflow`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Why does `Universal Codex CLI Pure-Orchestrator Work Protocol` connect `Protocol Governance and Gates` to `OpenSpec Integration`, `Control and Work Plane Workflow`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **What connects `name`, `version`, `verified_date` to the rest of the system?**
  _34 weakly-connected nodes found - possible documentation gaps or missing edges._