---
name: openspec-grill-change
description: Stress-test a completed OpenSpec change through a one-question-at-a-time decision interview, reconcile confirmed findings across its planning artifacts, and revalidate apply readiness. Use after proposal or planning artifacts are complete and before openspec-apply-change; requires the OpenSpec CLI and an initialized project or registered store.
---

# OpenSpec Change Grill

Use [references/workflow.md](references/workflow.md) as the authoritative workflow.

Remain between planning and implementation. Do not implement application code, start the apply workflow, or mark implementation tasks complete. Resolve one OpenSpec change through CLI-reported roots, stores, schemas, paths, and readiness state; never assume default artifact filenames.

Ask exactly one material decision question at a time and include a recommendation. Investigate factual questions from repository and planning evidence. Do not edit planning artifacts until the user confirms the shared understanding, and never claim a write or readiness result that was not observed.

**Complete when:** confirmed decisions have been reconciled across the selected change's planning artifacts, strict validation passes, every planning artifact is done or intentionally skipped, apply state is ready, and the user receives a truthful readiness report. Stop before implementation.

## Subagent coordination

The grilling conversation and reconciliation remain in the main agent. Bounded
read-only workers may verify facts or review one artifact dimension. Do not run
several reviewers when their questions depend on the same unresolved user
decision. Subagents never edit the change.
