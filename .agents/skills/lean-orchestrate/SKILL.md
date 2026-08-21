---
name: lean-orchestrate
description: Explicitly request lean Codex CLI orchestration for a material task. Use only when the user intentionally wants independent subagent coordination; do not use for normal automatic routing or simple work.
---

# Lean Orchestrate

Use KISS. This skill is an explicit override, not the default path.

1. Decide the smallest useful topology.
2. Skip `scout` when scope is already clear.
3. Normal route: one coherent `implementer`, then one fresh `verifier`.
4. Add a scout only for material discovery uncertainty.
5. Add parallel read-only workers only for genuinely independent questions.
6. Keep one active writer unless scopes are demonstrably disjoint.
7. Use one automatic rework cycle for a concrete material defect, then stop and surface the blocker.
8. Keep the primary thread as control plane while orchestration is active.

For OpenSpec work, preserve canonical `.agents/skills/openspec-*` unchanged. The implementation worker should use canonical `$openspec-apply-change`; the verifier should use canonical `$openspec-verify-change` when installed. Do not recreate OpenSpec planning or verification inside this skill.

Model starting points:
- scout: GPT-5.6 Terra, low;
- implementer: GPT-5.6 Sol, medium;
- verifier: GPT-5.6 Terra, high;
- high-risk verifier: GPT-5.6 Sol, high.

Return the final result after verification without narrating internal orchestration history unless it affects the user's decision.
