## Context

See `proposal.md` for motivation. The package currently installs a Codex-specific `AGENTS.md` block, two skills, six TOML custom-agent profiles, and one Codex concurrency setting through a single Python installer. The six role contracts and acceptance gates already exist in the normative protocol, while platform syntax and role semantics are partially duplicated in custom-agent files. Runtime permission inheritance means those files provide defense in depth but are not absolute isolation boundaries.

The four delta specifications define the portable runtime, optional process contract, deterministic coordination rules, and truthful multi-CLI distribution behavior. The design must retain existing safe file ownership, backup, dry-run, user/project scope, and idempotent installation properties.

## Goals / Non-Goals

**Goals:**

- Make the canonical protocol executable through one built-in generic subagent mapping per CLI.
- Keep logical role separation, fresh review, and acceptance gates independent from native agent-file formats.
- Make coordination and evidence rules explicit enough to validate from compact control packets and ledger state.
- Share protocol content across adapters and confine platform-specific knowledge to small declarative mappings and entrypoint text.
- Preserve safe upgrades by backing up modified managed files and never deleting legacy custom-agent files automatically.
- Add cross-platform static tests without requiring paid or interactive model calls in normal automated validation.

**Non-Goals:**

- Building a scheduler, daemon, task database, distributed lock, merge queue, or automatic worktree lifecycle.
- Supporting concurrent source-writing Executors in the portable baseline.
- Depending on Claude Code agent teams, Copilot Fleet, or recursive subagent spawning.
- Replacing OpenSpec or another framework's product-intent lifecycle.
- Making prompt-level read-only rules equivalent to an operating-system or sandbox security boundary.
- Generating many platform-specific role files from a meta-schema.

## Decisions

### 1. Separate runtime agent type from logical role

The canonical protocol remains the source of truth for Inspector, Planner, Executor, Reviewer, Validator, and Final Auditor responsibilities and packets. A dispatch combines one canonical role contract with a bounded task and sends it to the selected CLI's generic subagent:

| Tool | Baseline generic agent |
|---|---|
| Codex | `default` |
| Claude Code | `general-purpose` |
| Copilot CLI | `general-purpose` |

The primary thread records the returned thread identity and role. Reviewer and Final Auditor dispatches always request new threads.

Alternative considered: maintain six native role definitions for every CLI. Rejected because eighteen independently editable role files create drift, installation surface, and review burden without guaranteeing stronger runtime isolation.

### 2. Keep native profiles as an optional hardening layer

The existing Codex TOML profiles remain package assets but move behind an explicit native-hardening installer option. Default dispatch uses `default` even when native profiles are not installed. Upgrades do not delete existing profiles; they report them as retained legacy/native resources and modify them only when hardening is explicitly requested.

Alternative considered: remove the profiles from the repository and installer. Rejected because they remain useful for model tuning, role discovery, and defense-in-depth sandbox defaults, and automatic deletion would be unsafe.

### 3. Use one canonical skill tree plus thin adapter resources

The shared orchestration and OpenSpec skills remain canonical under `templates/skills/`. Their normative language becomes CLI-neutral. A small adapter resource for each tool contains only:

- generic-agent name and dispatch syntax;
- instruction and skill discovery paths for user and project scope;
- platform-specific invocation spelling;
- known capability limitations;
- optional native-hardening availability.

The installer copies the canonical skill tree into the selected CLI's supported discovery location and includes only that CLI's adapter resource. Claude additionally receives a minimal `CLAUDE.md` bridge to the managed `AGENTS.md` content. Copilot reuses `AGENTS.md` and its supported shared-skill location. Exact destination roots live in one installer adapter table rather than conditional logic scattered through file-copy functions.

Alternative considered: create a generator for complete tool-specific skill and agent sets. Rejected as unnecessary for three small adapters and harder to audit than explicit template resources.

### 4. Preserve existing CLI shape and add explicit tool selection

`scripts/install.py` and `scripts/verify_install.py` gain `--tool codex|claude|copilot`, defaulting to `codex`. `--scope user|project` remains. One invocation targets one tool; there is no `--tool all`. An optional `--native-hardening` flag installs supported native profiles and fails clearly when the selected adapter has none.

The manifest replaces Codex-only ownership assumptions with a per-tool adapter map containing status, generic-agent name, owned resources, supported scopes, verification date/version, and native-profile availability. A tool is marked `supported` only after its documented fresh-process discovery smoke test passes; otherwise it remains `experimental` even if static tests pass.

Alternative considered: infer the active CLI from environment variables or installed binaries. Rejected because implicit detection can write to the wrong configuration tree and makes dry-run output less predictable.

### 5. Harden the existing protocol rather than add a scheduler

The control packets and ledger gain the minimum data necessary for deterministic routing:

- Planner: `PROCESS`, `OWNED PATHS`, `SHARED RESOURCES`, exact `VALIDATION COMMANDS`, and TDD red/green commands when applicable.
- Executor: role/thread identity, actual changed paths, TDD evidence when applicable, and newly discovered dependencies.
- Reviewer: role/thread identity and explicit ownership/TDD/validation assessments.
- Validator and Final Auditor: role/thread identity plus concise command/evidence references.
- Ledger: implementer, reviewer, validator, and auditor identities alongside existing dependency and state fields.

The primary applies two simple invariants: all dependencies must be `DONE` before `READY`, and only one source-writing Executor may be active. No lock or scheduling process is introduced.

### 6. Add one optional durable process input and one optional state output

`ORCHESTRATION.md` is the optional human-authored process contract. A supplied template uses fixed headings for objective, authority, process mode, work derivation, dependencies, acceptance, and validation. Absence is valid and preserves current discovery behavior.

`.orchestration/state.json` is created only for work explicitly designated cross-session. It stores the compact ledger and schema version, not prompts, transcripts, raw logs, or specification bodies. On resume, Inspector treats it as a claim to reconcile against current authoritative state, never as authority by itself. Only one active orchestration owner may update it.

Alternative considered: use one combined human/machine YAML file. Rejected because generated state churn and human intent have different ownership and review needs.

### 7. Keep OpenSpec and external frameworks as authority inputs

The OpenSpec-specific skill continues to map proposal/spec/design/task artifacts into the canonical protocol. `ORCHESTRATION.md` may map other frameworks' artifacts and gates, but it cannot replace a higher-priority approved specification. Compatibility documentation establishes that only one workflow owns orchestration; Superpowers brainstorming, planning, or TDD practices may contribute inputs, but its subagent-driven implementation workflow cannot run concurrently.

### 8. Test adapters statically and promote support with manual discovery evidence

Automated tests use Python's standard library and temporary directories to cover argument validation, destination resolution, managed-block updates, adapter-specific resources, metadata parsing, backup behavior, dry-run behavior, idempotence, and verifier failures. Tests do not invoke a model.

Each adapter also has a documented manual smoke command that launches a fresh CLI process in a temporary project and checks instruction discovery, skill discovery, generic-agent dispatch, and a harmless role packet. The manifest records the successful CLI version and date. Unsupported local availability leaves the adapter experimental rather than failing the entire implementation.

## Risks / Trade-offs

- [Generic agents possess broader tools than read-only roles need] → Keep no-edit behavior normative, enforce one writer, record changed paths, and offer optional native hardening without claiming it is an absolute boundary.
- [Moving Codex profiles out of the default path changes existing installation expectations] → Preserve existing files, default `--tool` to Codex, document the migration, and require explicit opt-in before refreshing native profiles.
- [CLI discovery paths or built-in agent names change upstream] → Keep them in small adapter resources, record verified versions/dates, and fail verification with an actionable unsupported-version message.
- [Shared canonical skill text may still contain platform-specific wording] → Add static checks for forbidden foreign invocation syntax in canonical files and keep unavoidable syntax in adapter resources.
- [Persisted state becomes stale or is mistaken for authority] → Version the state schema and require Inspector reconciliation before dispatching resumed work.
- [Single-writer execution reduces throughput] → Continue parallel read-heavy work; accept lower write throughput as the portable safety baseline.
- [A tool passes static checks but cannot actually dispatch roles] → Keep it experimental until a fresh-process discovery smoke test passes.

## Migration Plan

1. Add canonical protocol and packet changes while retaining current Codex behavior.
2. Add the adapter table, manifest schema, process/state schemas, and tests.
3. Refactor installer and verifier behind the explicit `--tool` option, preserving Codex as the default.
4. Change default Codex dispatch to the built-in `default` agent and gate existing custom profiles behind `--native-hardening`; retain pre-existing files without deletion.
5. Add Claude and Copilot adapter resources and static verification.
6. Run fresh-process smoke tests on installed current CLI versions and promote only passing adapters to `supported`.
7. Update documentation and release notes with the breaking default-profile change and rollback instructions.

Rollback consists of invoking the prior installer release or reinstalling the retained Codex native profiles, restoring any backed-up managed instruction/config files, and leaving user-authored `ORCHESTRATION.md` or optional state files untouched.
