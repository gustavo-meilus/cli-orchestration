# Source Verification

The manifest is the machine-readable authority for adapter support evidence. This document explains the primary sources and unresolved field gaps used for release 2.0. All URLs below were fetched successfully from their authoritative domains on 2026-08-20.

## Codex CLI

Primary OpenAI documentation:

- <https://developers.openai.com/codex/subagents/> — subagent creation and role configuration.
- <https://developers.openai.com/codex/guides/agents-md/> — repository instruction discovery.
- <https://developers.openai.com/codex/skills/> — skill discovery and invocation.
- <https://developers.openai.com/codex/config-reference/> — current configuration schema.

The portable mapping uses a built-in generic `default` worker and treats custom `.codex/agents/*.toml` files as optional hardening. Local CLI observed during implementation: `codex-cli 0.148.0`. A 2026-08-20 fresh project process discovered `orchestrator-work-protocol`, but built-in Scout creation failed because the process had no collaboration thread. It returned `CODEX_SMOKE_BLOCKED` without direct fallback, so the adapter remains `experimental`.

## Claude Code

Primary Anthropic documentation:

- <https://code.claude.com/docs/en/sub-agents> — custom and general-purpose subagents.
- <https://code.claude.com/docs/en/claude-directory> — `.claude` project/user discovery roots.
- <https://code.claude.com/docs/en/skills> — skill structure and invocation.

The adapter maps the portable roles to Claude Code's `general-purpose` subagent and installs a minimal `CLAUDE.md` bridge where required. Local CLI observed during implementation: `2.1.237 (Claude Code)`. A 2026-08-20 fresh project process stopped before skill discovery because organization subscription access was disabled. Generic-worker creation and fail-closed routing remain unverified, so the adapter remains `experimental`.

## GitHub Copilot CLI

Primary GitHub documentation:

- <https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/invoke-custom-agents> — CLI agent invocation.
- <https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills> — CLI skill discovery.
- <https://docs.github.com/en/copilot/concepts/agents/copilot-cli/fleet> — parallel task execution and its distinct `/fleet` behavior.

The portable adapter uses the documented general-purpose/custom-agent prompt path. It does not use `/fleet` as the orchestration owner because fleet independently plans and assigns work. Copilot CLI was not installed in the implementation environment on 2026-08-20, so native discovery, invocation, and unavailable-worker smoke evidence remains unresolved and the adapter remains `experimental`.

## OpenSpec

Primary project sources:

- <https://github.com/Fission-AI/OpenSpec> — installation, supported tools, and canonical artifact workflow.
- <https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md> — current CLI commands and change lifecycle.

Local CLI observed during implementation: OpenSpec `1.9.0`. OpenSpec owns proposal, specs, design, tasks, apply, verify, sync, archive, and generated `.agents/skills/openspec-*`. This package calls or references those resources; it never packages or mutates them.

## Support-promotion rule

An adapter has exactly one status: `experimental` or `supported`. Promotion requires all of:

1. current authoritative source URLs and verification date;
2. a recorded tested CLI version;
3. repeatable fresh-process discovery and explicit-invocation evidence;
4. required generic-worker creation evidence;
5. an unavailable-worker test that fails closed rather than silently executing or self-reviewing.

Missing or failed evidence leaves the adapter `experimental` with a reason. Static installation, parsing, or file-copy success alone is never reported as native support.
