## Context

The repository currently implements a portable pure-control-plane protocol around six generic roles, CLI adapters, installation and verification tooling, state artifacts, and an OpenSpec bridge. Its shipped README, usage, workflow, normative templates, and v1 state still describe that six-role default, while the repository's contributor `AGENTS.md` already uses the target lean policy. That current-versus-target split is migration input, not a set of simultaneously valid runtime contracts. The superseded `simplify-cross-cli-orchestration` change partially extended the old design but was archived without syncing its deltas. Separately, the inspected `codex-openspec-lean-orchestration-v2.0.0` package demonstrates a smaller Codex-first adaptive workflow and passes its reported package checks, while direct reuse from its OneDrive-expanded source exposed a repeat-install issue caused by copied read-only attributes.

This change reconciles those inputs. The behavior contracts are defined in the four delta specs; see `proposal.md` for motivation.

## Goals / Non-Goals

**Goals:**

- Keep the framework portable and CLI-neutral at its core.
- Make direct execution and pure orchestration explicit, complementary modes.
- Reduce routine orchestration to the smallest topology that preserves material quality.
- Preserve independent verification, safe ownership, framework authority, and recoverable distribution.
- Retain valuable high-assurance capabilities without making them routine stages.
- Preserve existing public skill entry names and a safe path from legacy state and installations.
- Establish evidence that can tune routing, models, and support declarations.

**Non-Goals:**

- Reimplementing OpenSpec or editing canonical OpenSpec skills.
- Making Codex-specific model identifiers part of the portable protocol.
- Promising feature parity where a target CLI lacks an equivalent native primitive.
- Requiring durable workflow state, a six-role committee, or a subagent for every task.
- Silently degrading a selected orchestrated route into direct execution when independent workers are unavailable.
- Claiming field-performance gains before representative benchmarks exist.

## Decisions

### 1. Put the pure boundary around orchestration mode, not every task

The runtime exposes two modes. Direct mode lets the active agent implement and validate clear low-risk work. Orchestration mode makes the primary a pure control plane and delegates all substantive worker work.

This preserves the project's defining pure-orchestrator property whenever orchestration exists without paying coordination cost when no independent context adds value. The alternative—requiring a control plane for every change—was rejected because it converts a safety architecture into unavoidable ceremony.

### 2. Reduce the portable normal role set to Scout, Implementer, and Verifier

The default material path is Implementer → fresh Verifier. Scout is prepended only when focused discovery can materially reduce uncertainty. Existing Planner, Validator, Final Auditor, and specialist contracts are reconciled into an optional high-assurance library rather than silently deleted.

Logical role contracts remain vendor-neutral. Adapters may map them to native general-purpose agents, configured custom agents, models, or reasoning levels. The alternative—encoding one vendor's current model catalog into the protocol—would make portability brittle.

### 3. Select topology by explicit route predicates

Project policy and the orchestration entry point use cumulative predicates. For implementation work, an explicit user or governing repository requirement, meaningful behavior/regression risk, or a high-risk boundary establishes the Implementer → fresh Verifier base. Material discovery or route-selection uncertainty prepends Scout. A named uncovered high-risk concern strengthens the Verifier or adds one distinct specialist. Read-only analysis, discovery, or review uses only the minimum independent read-only contexts and never manufactures an Implementer cycle. Direct execution is eligible only when no orchestration predicate applies and the work is clear, local, low-risk, and cheaply verifiable. Independent read-heavy branches select orchestration only when their expected correctness, uncertainty, or wall-clock benefit is material.

The primary evaluates those predicates from the request, governing instructions, already-visible control information, and explicit risk indicators. If choosing a route requires substantive repository or specification discovery, that uncertainty itself selects Scout; the primary does not inspect deeply and then retroactively declare orchestration. Predicates remain decision guidance rather than an elaborate scoring engine. This KISS approach is inspectable and portable; a numeric router would imply precision unsupported by current evidence.

### 4. Batch work by context affinity under one-writer ownership

The control plane groups tasks that share files, concepts, and validation context into coherent work packets. It permits parallel read-only or disjoint discovery branches, but only one active writer owns an overlapping boundary. Dependencies gate dispatch.

This replaces task-per-session decomposition, which repeatedly reconstructs the same context. It also avoids the alternative of unrestricted parallel writes, whose merge and semantic-conflict cost defeats the speed benefit.

### 5. Make acceptance proportional to the selected route

Direct work uses the repository's appropriate native checks. Ordinary orchestrated work requires a fresh Verifier PASS. A stronger verifier or distinct specialist review is added only for high-risk domains. Validation that mutates tracked output is reclassified as implementation and independently reverified.

A fresh Verifier is a newly created non-implementer context that did not edit or own the judged batch and reads authoritative state directly. It may use the same model family; independence is contextual and behavioral, not a model-diversity claim. The first verifier defect returns to the same Implementer so the warm implementation context is reused, followed by a different fresh Verifier. If that Implementer is unavailable, contaminated by a conflicting responsibility, or no longer owns the scope, one replacement receives a self-contained correction packet and the reason is recorded. A second failure ends automatic looping and triggers cause diagnosis. The alternative of spawning a new implementer routinely or an unbounded review loop increases rediscovery without resolving ambiguity.

### 6. Keep framework authority outside the orchestration layer

The core coordinates contexts but does not own development methodology. Authority follows a portable order beginning with the latest explicit user requirement and governing repository instructions, then approved framework change artifacts and canonical specifications, followed by design/tasks, validated implementation, external evidence, and historical or speculative material. Same-level material conflicts block affected work. For OpenSpec, canonical proposal/spec/design/tasks/apply/verify/sync/archive commands and `.agents/skills/openspec-*` resources remain authoritative and package-excluded. Direct OpenSpec apply remains valid for qualifying work; material work passes canonical change references through the Implementer and fresh Verifier.

Canonical OpenSpec Verify owns specification-conformance evidence; it does not by itself make the orchestration acceptance decision. In an orchestrated route, the fresh Verifier evaluates that evidence with authoritative artifacts and actual repository state. TDD and other task or development frameworks are treated the same way: their order, artifacts, and acceptance criteria enter the work packet; the orchestrator only assigns ownership, schedules dependencies, and applies the selected route's acceptance gate. This avoids competing sources of truth while separating the source of acceptance criteria from the context authorized to judge them.

### 7. Use one canonical protocol with thin CLI adapters

The portable core contains route semantics, role contracts, packets, and acceptance rules. Codex CLI, Claude Code, and Copilot CLI adapters contain only native discovery, invocation, configuration, and optional hardening details. Installation selects adapters explicitly and verification checks each selected target.

No tool-selection flag installs Codex only for compatibility with the existing Codex-first package; Claude Code and Copilot CLI require explicit selection, and multiple explicit selections remain valid. The manifest is the single support-evidence record and permits exactly `experimental` or `supported`. Static/package checks are necessary but not sufficient: a `supported` label also needs current authoritative documentation, tested CLI version, and repeatable fresh-process discovery/invocation smoke evidence. A failed or missing smoke remains `experimental` with its reason. Narrative documentation is generated or checked against that record.

If a selected CLI cannot create or isolate a required generic worker, the orchestrated route returns BLOCKED before the missing responsibility is performed. It never falls back to primary-thread implementation or self-review. The alternative would make the same route name provide materially different safety depending on the adapter.

### 8. Reconcile v2 and the current repository instead of overlaying either

Implementation begins with a file-level ownership map: retain portable features unique to this repository, import or adapt lean behavior demonstrated by v2, and retire obsolete six-role-default assets only after references and migration paths are updated. Canonical OpenSpec resources are protected with byte-preservation sentinels.

The v2 artifact is an implementation input, not a replacement tree. Its source identity and checksum are recorded in the reconciliation evidence, and its OneDrive read-only propagation finding becomes an installer regression case. Existing logical `orchestrator-work-protocol` and `openspec-orchestrated-apply` names remain stable, with each adapter preserving its native invocation syntax, while their default behavior changes. This avoids losing multi-CLI work already present here, breaking existing prompts unnecessarily, or inheriting source-packaging assumptions blindly.

### 9. Keep durable state optional and compact

The current compact schema is used only for workflows that genuinely cross sessions or dependent batches. Direct and single-batch routes do not create a mandatory ledger. When used, state tracks identifiers, route, ownership, dependencies, statuses, evidence pointers, and the next gate—not worker transcripts.

A valid legacy six-role ledger is preserved, converted only where claims map unambiguously, and then reconciled by fresh discovery before dispatch. Invalid or ambiguous legacy state remains recoverable and blocks with an actionable migration path; the implementation never guesses that old review or audit identities satisfy the new fresh-Verifier gate.

### 10. Benchmark marginal value, not just primary-context size

Representative workloads compare direct execution, Implementer → Verifier, and Scout → Implementer → Verifier. Measurements include task success, regressions found, elapsed time, total tokens/cost where observable, model turns, tool calls, repeated reads, test executions, rework, diff churn, and user interventions.

Benchmarks guide route and model defaults but do not block static/package correctness work. Field claims and promotion decisions remain explicitly pending until measurements are collected.

### 11. Use one aligned public release version

Breaking release `2.0.0` uses one version across `VERSION`, manifest, protocol header, README, changelog, checksum metadata, and verifier output. The portable protocol can still evolve conceptually, but it does not expose an independently numbered compatibility surface in this package. This removes the current unexplained package `1.1.0` versus protocol `2.0.0` split.

## Risks / Trade-offs

- [Route guidance is applied inconsistently] → Provide concrete scenarios, adapter examples, and tests for route selection; keep predicates small enough to audit.
- [Removing routine stages misses defects] → Preserve fresh verification for material work, retain optional specialists, and compare defect escape rates in representative benchmarks.
- [Legacy six-role assets confuse users] → Migrate references atomically, label optional high-assurance assets clearly, and verify no default path still requires them.
- [Adapters drift as CLIs evolve] → Isolate native assumptions, record source dates, run fresh-process smoke checks, and downgrade unsupported claims promptly.
- [Package reconciliation overwrites user or OpenSpec files] → Use managed-file manifests, explicit ownership, backups for replacements, dry-run migration, and OpenSpec byte sentinels.
- [Optional state creates two code paths] → Keep the state contract minimal and test both stateless and resumable routes rather than maintaining separate orchestration semantics.
- [Legacy state loses accepted work or invents new acceptance] → Preserve the original, map only unambiguous claims, and require fresh reconciliation before dispatch.
- [A CLI advertises orchestration but cannot create an independent worker] → Fail closed with an actionable BLOCKED result and keep the adapter experimental until fresh-process evidence passes.
- [Current and target documentation remain mixed] → Treat the file-level reconciliation map as the migration checklist and make verification reject any default six-role claim after the new release surface is published.
- [Benchmarks are noisy or unavailable] → Publish fixtures and raw measurements, separate static correctness from field evidence, and avoid unsupported optimization claims.

## Migration Plan

1. Capture the current repository, archived change, and v2 artifact identity/checksum as separate baselines; classify current documents as shipped-current, contributor-policy, or target-planning inputs and add failing contract tests for the new default route and preservation boundaries.
2. Introduce the adaptive portable protocol and three-role contracts while retaining legacy assets for compatibility.
3. Update OpenSpec integration and CLI adapters to consume the new core; verify canonical OpenSpec resources remain byte-identical.
4. Update installer, verifier, manifest, and migration logic for the Codex compatibility default, explicit selected-tool deployment, public entry-point preservation, legacy state/install reconciliation, idempotence, restrictive source attributes, aligned version surfaces, and fail-closed adapter behavior.
5. Move six-role-default material to clearly optional high-assurance resources or remove package-owned obsolete copies after all references migrate.
6. Run repository, clean-install, repeat-install, legacy-state, migration, version-consistency, and fresh-process adapter checks; reconcile narrative claims to the manifest and record support status honestly.
7. Run representative route benchmarks and tune only defaults supported by the results.

Rollback restores the pre-change package-owned files from migration backups or the prior release artifact and leaves unrelated files and canonical OpenSpec-managed skills untouched. A failed install or migration must stop before publishing a successful manifest.

## Open Questions

- Which representative repository workloads should become the long-lived benchmark corpus?
- Which current CLI environments can provide reliable token and cost telemetry in addition to wall-clock and correctness measures?
