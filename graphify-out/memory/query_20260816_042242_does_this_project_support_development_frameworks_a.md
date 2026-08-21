---
type: "query"
date: "2026-08-16T04:22:42.496132+00:00"
question: "Does this project support development frameworks and TDD, parallel dependency-aware task execution and verification, and Claude Code CLI or Copilot CLI?"
contributor: "graphify"
outcome: "useful"
source_nodes: ["Framework Independence", "Universal Codex CLI Pure-Orchestrator Work Protocol", "OpenSpec Integration", "Review Validation and Audit Acceptance Gates"]
---

# Q: Does this project support development frameworks and TDD, parallel dependency-aware task execution and verification, and Claude Code CLI or Copilot CLI?

## Answer

Expanded via graph vocab: [framework, process, tasks, planning, openspec, workflow, concurrent, work, validation, review, acceptance, subagents]. The project is framework-independent and can wrap OpenSpec, TDD, another framework, or direct user-defined tasks, but only OpenSpec has a dedicated bridge. TDD is supported as an underlying authority/acceptance process but is not mechanically enforced. Superpowers can supply TDD or planning, but its subagent-driven-development orchestrator conflicts with this project in handoff, rework, and review ownership unless adapted. Parallel execution is protocol-level: Inspector creates a dependency graph; the primary sequences dependencies, parallelizes independent work, defaults to one writer for coupled repositories, and accepts parallel writers only for disjoint scopes. Verification uses fresh per-item Reviewers, aggregate Validator, and fresh Final Auditor. There is no persistent scheduler, lock manager, or automatic worktree system. Claude Code CLI is not directly supported: it needs CLAUDE.md, .claude/skills, and Markdown/YAML agents; a port could use subagents or experimental agent teams. Copilot CLI has partial discovery compatibility because it reads AGENTS.md and .agents/skills, but package custom-agent TOMLs and Codex-specific tool/invocation semantics are incompatible; a real port should provide .github/agents profiles and adapt orchestration to task/fleet tools.

## Outcome

- Signal: useful

## Source Nodes

- Framework Independence
- Universal Codex CLI Pure-Orchestrator Work Protocol
- OpenSpec Integration
- Review Validation and Audit Acceptance Gates