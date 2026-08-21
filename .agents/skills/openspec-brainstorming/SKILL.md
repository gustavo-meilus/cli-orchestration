---
name: openspec-brainstorming
description: Refine OpenSpec exploration or an uncertain project idea into one focused, explicitly approved change, then generate, strictly validate, and review every planning artifact required for implementation. Use after openspec-explore or when the user wants to converge on an OpenSpec proposal without starting implementation; requires the OpenSpec CLI and an initialized project or registered store.
---

# OpenSpec Brainstorming

Use [references/workflow.md](references/workflow.md) as the authoritative workflow.

Remain in planning throughout the workflow. Do not write application code, scaffold implementation, or modify product files. Do not create an OpenSpec change until the user explicitly approves the change contract.

Before acting, resolve the OpenSpec project or registered store with the CLI. Ground claims in repository, specification, test, and configuration evidence; label assumptions instead of presenting them as facts. Never claim an artifact or repository write unless it was actually completed.

**Complete when:** one cohesive OpenSpec change has all artifacts transitively required for apply, passes strict validation and a cross-artifact coherence review, and has been presented for user review. The next action is user approval followed by the apply workflow, not implementation in this skill.

## Subagent coordination

The main agent owns the change contract and all planning writes. Use
`openspec-subagents` only for bounded read-only repository research or independent
artifact review. Do not let workers create or edit proposal, specs, design, or
tasks. When the required handoff would contain most of the planning context, keep
the review direct.
