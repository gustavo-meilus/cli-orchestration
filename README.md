# CLI Orchestration 2.0

Portable, CLI-neutral orchestration for Codex CLI, Claude Code, and GitHub Copilot CLI. Release 2.0 keeps the primary thread a pure control plane whenever orchestration is active, while using direct execution for work that does not benefit from independent contexts.

## KISS routing

Apply cumulative predicates in this order:

1. explicit user/repository orchestration requirement;
2. high-risk boundary;
3. material discovery or route uncertainty;
4. material implementation/regression risk;
5. useful independent read-only parallelism;
6. otherwise direct execution for clear, local, low-risk, cheaply verifiable work.

The normal material topology is `Implementer -> fresh Verifier`. Add Scout only when focused discovery can prevent churn. Read-only work uses only useful read-only contexts. Planner, Validator, Final Auditor, and specialists are optional high-assurance resources for a documented distinct risk—not a default committee.

A fresh Verifier is a new context that did not implement, edit, or own the batch; it may use the same model. Related tasks stay together as context-affinity batches. One active writer owns every overlapping file/subsystem boundary. The first concrete defect returns to the same Implementer when safe, then a different fresh Verifier checks it; a second failure ends automatic looping with cause diagnosis.

## Pure portable core

The canonical package core defines logical roles, routing, packets, acceptance, framework boundaries, and optional resumability without vendor model names or invocation syntax. Thin adapters map those contracts to native discovery and generic-agent mechanisms.

When a selected route needs an independent worker that the CLI cannot create or isolate, it returns actionable `BLOCKED`; it never silently falls back to primary implementation or self-review.

## Frameworks and OpenSpec

The orchestrator coordinates contexts; it does not replace development methodology. TDD, task systems, and external frameworks supply authoritative process inputs and acceptance criteria.

OpenSpec owns proposal/spec/design/tasks/apply/verify/sync/archive and `.agents/skills/openspec-*`. This package never installs or edits canonical OpenSpec skills. Clear low-risk OpenSpec work may use `$openspec-apply-change` directly. Material orchestration uses an Implementer with canonical apply and a fresh Verifier that may use canonical `$openspec-verify-change` as conformance evidence. That evidence does not automatically grant orchestration `PASS`.

## Support matrix

`manifest.json` is authoritative. Static package checks and native fresh-process evidence are separate.

| CLI | Generic worker mapping | Status | Recorded field evidence gap |
|---|---|---|---|
| Codex CLI | `default` | `experimental` | Fresh process discovered the skill but native Scout creation failed because the session had no collaboration thread; the route returned `BLOCKED` |
| Claude Code | `general-purpose` | `experimental` | Fresh process stopped before discovery because organization subscription access was disabled |
| Copilot CLI | `general-purpose` | `experimental` | CLI unavailable in the validation environment; native smoke unrun |

Only `experimental|supported` are valid states. See [source verification](docs/SOURCE-VERIFICATION.md).

## Install

Project, Codex compatibility default:

```bash
python scripts/install.py --scope project --project /path/to/repository
python scripts/verify_install.py --scope project --project /path/to/repository
```

Explicit multi-CLI project install:

```bash
python scripts/install.py --scope project --project /path/to/repository \
  --tool codex --tool claude --tool copilot
python scripts/verify_install.py --scope project --project /path/to/repository \
  --tool codex --tool claude --tool copilot
```

Use `--native-hardening` only with a selection containing Codex to install optional Scout/Implementer/Verifier profiles. User installs use `--scope user`. See [INSTALL.md](INSTALL.md) and [migration](docs/MIGRATION.md).

## Public entries

- `orchestrator-work-protocol`: adaptive routing and portable orchestration.
- `openspec-orchestrated-apply`: thin route-aware bridge preserving canonical OpenSpec ownership.

Logical names remain stable; native invocation punctuation differs by CLI.

## Documentation

- [Usage](USAGE.md)
- [Workflow](docs/WORKFLOW.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Governance](docs/GOVERNANCE.md)
- [OpenSpec integration](docs/OPENSPEC-INTEGRATION.md)
- [Model policy](docs/MODEL-POLICY.md)
- [Benchmarking](docs/BENCHMARKING.md)
- [Benchmark results and field limitation](docs/BENCHMARK-RESULTS.md)
- [Reconciliation map](docs/RECONCILIATION.md)

Package and protocol release version: `2.0.0`.
