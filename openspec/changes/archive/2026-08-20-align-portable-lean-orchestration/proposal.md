## Why

The current portable pure-orchestrator design protects context and review independence, but its mandatory six-role pipeline creates repeated reads, serial gates, and agent overhead that are disproportionate for many tasks. The project needs to preserve portable pure orchestration while adopting a KISS, evidence-driven policy that uses direct execution or the smallest useful orchestration topology.

## What Changes

- Define two execution modes: direct execution for clear, local, low-risk work and pure orchestration when independent contexts materially improve correctness, uncertainty reduction, verification, or parallel throughput, or when the user or governing repository policy explicitly requires orchestration.
- Preserve the pure control-plane invariant whenever orchestration mode is active.
- **BREAKING**: Replace the universal Inspector → Planner → Executor → Reviewer → Validator → Final Auditor pipeline with an adaptive material-implementation default of Implementer → fresh Verifier, adding Scout only for material discovery uncertainty and using only the minimum suitable read-only contexts for analysis or review work.
- Define a fresh Verifier as a new non-implementer context that independently inspects authoritative state; freshness does not require a different model.
- Retain Planner, Validator, Final Auditor, and specialist review contracts only as optional high-assurance extensions justified by distinct risks or measured value.
- Batch related OpenSpec tasks by context affinity instead of creating one worker cycle per checkbox.
- Keep one active writer, allow independent read-heavy parallelism, and route the first concrete verifier defect back to the same Implementer before using a fresh Verifier.
- Make acceptance route-specific: native validation for direct low-risk work, fresh Verifier PASS for ordinary orchestrated work, and selective extra gates only for genuine high risk.
- Preserve OpenSpec as the owner of proposal/spec/design/tasks/apply/verification/sync/archive; the orchestration layer selects execution topology without editing, copying, or competing with canonical `openspec-*` skills.
- Distinguish canonical framework verification evidence from the orchestration layer's independent acceptance decision, and preserve explicit user and repository authority over integrated framework artifacts.
- Preserve portable Codex, Claude Code, and Copilot CLI adapters, tool-aware installation and verification, and exactly two evidence-based support declarations: `experimental|supported`.
- Keep Codex as the backward-compatible adapter default when no tool is selected; Claude Code and Copilot CLI remain explicit selections.
- Preserve the public logical entry names `orchestrator-work-protocol` and `openspec-orchestrated-apply` while each adapter retains its native invocation syntax, and safely migrate or reject legacy resumable state with an actionable recovery path.
- Block an orchestrated route when its required independent worker cannot be created; never silently collapse that route into direct execution.
- Align package, protocol, documentation, manifest, and changelog version surfaces on breaking release `2.0.0` and make the manifest the support-evidence source of truth.
- Use the inspected v2.0.0 package as a design and implementation input while reconciling it with this repository rather than blindly overlaying either source tree.
- Add representative route benchmarks so additional roles, model choices, and validation layers must demonstrate marginal value.

## Capabilities

### New Capabilities

- `adaptive-orchestration-runtime`: Defines exhaustive route precedence, direct routing, pure orchestration mode, minimum sufficient topologies, portable logical roles, context-affinity batching, and selective high-assurance expansion.
- `framework-integration`: Defines authority precedence and the composition boundary for canonical OpenSpec, direct tasks, TDD, external development frameworks, conformance evidence, and orchestration acceptance.
- `work-coordination-and-acceptance`: Defines one-writer coordination, dependency and ownership rules, fresh-verifier identity, route-specific acceptance, bounded rework, failure behavior, and optional resumability.
- `multi-cli-distribution`: Defines thin adapters, the Codex compatibility default, selected-tool installation and verification, public-entry compatibility, safe legacy migration, aligned version surfaces, and evidence-based support status for Codex, Claude Code, and Copilot CLI.

### Modified Capabilities

None. The superseded change was archived without syncing its delta specifications, so this change introduces the reconciled capabilities as new contracts.

## Impact

- Canonical portable protocol, role contracts, project policy templates, and optional high-assurance extensions.
- Codex, Claude Code, and Copilot CLI adapter resources and native hardening profiles.
- Installer, verifier, migration, manifest, wrappers, temporary-install fixtures, and compatibility tests.
- Existing public skill invocations, legacy v1 state claims, package/protocol version fields, and adapter evidence records.
- README, workflow, architecture, governance, OpenSpec integration, migration, model-policy, benchmarking, and source-verification documentation.
- Superseded six-role-default assets and partially implemented cross-CLI behavior, which require explicit reconciliation or retirement.
- Canonical `.agents/skills/openspec-*` remain outside package ownership and must remain unchanged.
