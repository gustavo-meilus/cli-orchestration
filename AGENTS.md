<!-- BEGIN LEAN-CODEX-ORCHESTRATION -->
## Lean Codex execution policy

KISS: default to direct execution. Subagents are an optimization, not a required ceremony.

Use direct execution when the task is clear, local, low-risk, and cheaply verifiable. Do not spawn agents merely because agents are available.

Enter orchestration mode only when at least one applies:
- independent review materially reduces risk for a behavior-changing task;
- scope, ownership, or dependencies are unclear enough that focused discovery will save implementation churn;
- the work contains genuinely independent read-heavy branches that can run in parallel;
- the change is high-risk: security/auth/permissions, destructive or migration data work, concurrency, production infrastructure, financial logic, or public compatibility boundaries;
- the user explicitly requests orchestration or independent review.

When orchestration mode is active, the primary Codex thread is a control plane only: dispatch, coordinate, track minimal state, and gate completion. Keep detailed exploration, implementation, logs, diffs, and review reasoning inside worker threads.

Use the minimum sufficient topology:
- well-specified material change: `implementer -> fresh verifier`;
- uncertain scope: `scout -> implementer -> fresh verifier`;
- high-risk: use a stronger verifier; add another read-only reviewer only for a distinct risk domain that justifies the extra cost.

Do not create Planner, Validator, or Final-Auditor stages by default. Do not cycle agents per tiny task. Batch work by context affinity so one implementer can keep the relevant code/spec context warm. Default to one active writer.

Model policy when spawning custom agents:
- `scout`: `gpt-5.6-terra`, low reasoning;
- `implementer`: `gpt-5.6`, medium reasoning for material implementation;
- `verifier`: `gpt-5.6-terra`, high reasoning;
- for high-risk verification, use `gpt-5.6`, high reasoning instead of adding routine extra stages.

Rework: route one concrete verifier defect back to the same implementer thread when practical; then use a fresh verifier. After one failed rework cycle, stop looping and surface the blocker/specification issue unless the user explicitly requests deeper iteration.

OpenSpec: `.agents/skills/openspec-*` is OpenSpec-owned. Never edit or replace canonical OpenSpec skills. For direct OpenSpec implementation, use canonical `$openspec-apply-change`. In orchestration mode, the implementer uses canonical `$openspec-apply-change`; the verifier uses canonical `$openspec-verify-change` when installed. Do not recreate OpenSpec proposal/spec/design/tasks planning in this layer.
<!-- END LEAN-CODEX-ORCHESTRATION -->
