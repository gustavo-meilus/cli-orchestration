# OpenSpec Pre-Apply Grill

Stress-test a completed OpenSpec change before implementation:

`select → preflight → validate → load → map decisions → grill → confirm → reconcile → revalidate → hand off`

## Contents

1. [Hard gates](#hard-gates)
2. [Input and root selection](#input-and-root-selection)
3. [Preflight the change](#preflight-the-change)
4. [Load the complete planning context](#load-the-complete-planning-context)
5. [Build the decision tree](#build-the-decision-tree)
6. [Conduct the grilling loop](#conduct-the-grilling-loop)
7. [Confirm convergence](#confirm-convergence)
8. [Reconcile planning artifacts](#reconcile-planning-artifacts)
9. [Verify the reconciled change](#verify-the-reconciled-change)
10. [Report and hand off](#report-and-hand-off)

## Hard gates

- Do not implement application code or modify product files.
- Do not start `openspec-apply-change` or invoke apply automatically.
- Do not mark implementation tasks complete; preserve every pending `- [ ]` task.
- Ask exactly one decision question per message and wait for the answer.
- Include one clear recommended answer with every decision question.
- Investigate facts instead of asking the user to recall them.
- Leave product and design decisions to the user; do not silently choose.
- Settle parent decisions before dependent choices.
- Do not edit planning artifacts until the user confirms the shared understanding.
- Do not treat simulated, hypothetical, or missing evidence as a real approval.
- Do not commit, push, create branches, or open pull requests unless separately requested.

The goal is to expose and resolve material ambiguity, contradiction, missing coverage, and unsupported assumptions while changes are still cheap.

## Input and root selection

Accept an optional change name. If omitted:

- Infer it from the conversation only when the reference is unambiguous.
- Auto-select it when exactly one active change exists.
- Otherwise run `openspec list --json` and ask the user to choose.

Always announce:

```text
Using change: <name>
```

Also explain how the user can select another change.

Operate on one resolved OpenSpec root:

- When the user names a registered store, run `openspec store list --json`, resolve the store ID, and preserve `--store <id>` on every command that accepts it.
- Without a selected store, use `openspec list --json` to resolve the nearest initialized local root.
- When root selection is ambiguous, use both commands to identify available roots and changes; do not guess.
- Never assume planning files live under the current code repository.
- Treat CLI-returned `root`, `changeRoot`, `planningHome`, and `actionContext` as authoritative.

Stop and report the missing prerequisite when no initialized root or registered store can be resolved.

## Preflight the change

### 1. Select and announce

Select one change using the input rules. When multiple active changes exist and none is clearly referenced, ask the user to choose one. Do not review a guessed change.

### 2. Confirm planning completion

Run:

```bash
openspec status --change "<name>" --json
```

Read at least:

- `schemaName`
- `planningHome`
- `changeRoot`
- `artifactPaths`
- `artifacts`
- `applyRequires`
- `isComplete`
- `nextSteps`
- `actionContext`
- `root`

Require every planning artifact to be `done` or intentionally `skipped`. Treat a skipped artifact as complete by policy; never create its file.

If planning is incomplete:

1. Show every incomplete or blocked artifact.
2. Explain the dependency blocking it.
3. Recommend `openspec-plan-change`, `openspec-propose`, or `openspec instructions <artifact-id> --change "<name>" --json`, as appropriate.
4. Stop before the interview.

### 3. Confirm pre-apply readiness

Run:

```bash
openspec instructions apply --change "<name>" --json
```

Read:

- `state`
- `missingArtifacts`
- `contextFiles`
- `progress`
- `tasks`
- `instruction`
- optional `context`
- optional `operationGuidance`
- optional `references`
- `root`

Handle the state exactly:

- `blocked` — report the blocker and stop; route planning gaps to the relevant planning workflow.
- `all_done` — report that implementation tasks are already complete, stop the pre-apply review, and recommend `openspec-verify-change` when verification is still needed.
- `ready` — continue.

Treat the CLI state as authoritative. Project context, operation guidance, or conversational confidence cannot override a blocked state.

### 4. Run deterministic validation

Run:

```bash
openspec validate "<name>" --strict --json
```

If validation fails:

1. Summarize the exact findings and affected files.
2. Separate mechanical format defects from decisions requiring user input.
3. Recommend the appropriate planning repair path.
4. Stop before the interview because the artifacts cannot be grilled as a structurally valid package.
5. Do not silently repair files.

Begin the grilling session only from a structurally valid planning package.

## Load the complete planning context

Read every concrete path in `contextFiles`. Also read every concrete path in `artifactPaths.<artifact-id>.existingOutputPaths` so the review covers all completed artifacts, including schema artifacts not directly required by apply.

Use the schema and CLI output rather than assuming filenames such as `proposal.md`, `design.md`, or `tasks.md`.

Treat runtime inputs correctly:

- Apply optional `context` as required prompt-level project facts, conventions, and constraints.
- Consider every `operationGuidance` entry, but follow it only when applicable and compatible with the built-in workflow.
- Keep runtime inputs separate from artifact contents, task completion, readiness state, and the CLI instruction.
- Do not copy runtime context, guidance, or rules verbatim into planning artifacts unless separately requested.

Inspect implementation evidence when it can settle a factual question, including existing APIs, naming conventions, data models, dependency versions, test patterns, platform constraints, and current behavior. Resolve repository and branch before any connected-repository read, name exact supporting paths, and distinguish observed facts from inference.

## Build the decision tree

Build an internal decision tree from the actual artifacts and repository. Start with high-impact parent decisions and proceed toward dependent details.

Review only areas material to the selected change:

1. Problem, outcome, scope, and non-goals.
2. Observable requirements and acceptance scenarios.
3. Compatibility, error behavior, security, privacy, permissions, and mandatory approvals.
4. Interfaces, data ownership, migrations, rollout, and rollback.
5. Technical choices, alternatives, and trade-offs.
6. Operational risks, monitoring, performance, and failure recovery.
7. Task coverage, ordering, testing, documentation, and verification.
8. Contradictions between artifacts or between artifacts and repository evidence.

Check the core artifact invariants:

- Proposal scope matches delta requirements.
- Externally observable behavior lives in specs, not design-only prose.
- A `MODIFIED` requirement states the complete resulting contract rather than a patch fragment.
- Design explains consequential choices needed to realize the requirements.
- Every task traces to a requirement, design decision, validation need, migration, rollout, or documentation obligation.
- Every behavioral implementation task is represented by an appropriate delta unless the schema explicitly skips specs.
- Preserved behavior and regression cases are explicit.
- No unresolved product decision is hidden in tasks.

Classify each potential issue:

- **Fact** — investigate it directly.
- **Decision** — ask the user.
- **Contradiction** — identify both conflicting statements and ask which controls.
- **Missing coverage** — explain the implementation consequence and ask for intended behavior.
- **Accepted unknown** — record it only after the user explicitly accepts the risk.
- **Evidence gap** — identify whether evidence is real, simulated, or missing; never satisfy a mandatory approval with simulation.

Prioritize questions capable of changing requirements, architecture, migration strategy, safety, or task decomposition. Do not spend the session on cosmetic preferences.

## Conduct the grilling loop

Ask one question per message using:

```text
## Question <n> — <decision>

Why this matters:
<implementation or product consequence>

What the artifacts currently say:
<concise evidence with file paths or artifact ids>

Recommended answer:
<one clear recommendation and why>

Other viable option:
<alternative and main trade-off, when useful>

Question:
<one decision for the user>
```

After each answer:

1. Restate the accepted decision in one sentence.
2. Record the affected artifacts.
3. Re-evaluate remaining decision dependencies.
4. Ask the highest-dependency unresolved question next.

When an answer is vague, contradictory, or delegates the decision back to the agent, challenge it with one focused follow-up. Do not convert ambiguity into an assumption. Do not batch questions or present a checklist for the user to answer at once.

## Confirm convergence

Continue until every material branch is:

- resolved by evidence;
- explicitly decided by the user;
- explicitly accepted as a known risk; or
- proven irrelevant to the change.

Before editing, present:

```text
## Shared Understanding

### Confirmed decisions
- ...

### Facts verified from the repository
- ...

### Planning artifacts that must change
- <artifact id>: <required reconciliation>

### Explicitly accepted risks or unknowns
- ...

### Evidence and approval gaps
- ...

### Apply-readiness impact
- ...
```

Ask exactly one confirmation question:

```text
Does this capture our shared understanding, and should I reconcile the OpenSpec planning artifacts now?
```

Do not edit until the user explicitly confirms.

## Reconcile planning artifacts

After confirmation, update planning artifacts only. For every affected artifact, run:

```bash
openspec instructions "<artifact-id>" --change "<name>" --json
```

Treat the returned values as the artifact-writing contract:

- `instruction`
- `rules`
- `dependencies`
- `existingOutputPaths`
- `resolvedOutputPath`
- `template`
- `skipped`
- `warning`

Apply these reconciliation rules:

- Edit only paths belonging to the selected change and planning root.
- Respect schema-specific artifact IDs and paths.
- Reread dependencies before editing each artifact.
- Preserve every confirmed decision across all affected artifacts.
- Reconcile upstream and downstream artifacts together when one decision affects both.
- Keep observable behavior in specs and implementation choices in design-oriented artifacts.
- Make `MODIFIED` requirements complete replacements.
- Ensure tasks cover every confirmed implementation, migration, testing, documentation, monitoring, and rollout consequence.
- Keep new implementation tasks unchecked; never change `- [ ]` to `- [x]`.
- Do not create files for skipped artifacts.
- Do not copy project context, operation guidance, or artifact rules verbatim into artifacts.
- Keep changes minimal and limited to confirmed grilling findings.
- Never report a connected-repository write unless the write mechanism confirms it.

If reconciliation exposes a new material decision, stop editing and return to the one-question-at-a-time loop. Do not silently resolve it.

## Verify the reconciled change

Run all three checks again:

```bash
openspec validate "<name>" --strict --json
openspec status --change "<name>" --json
openspec instructions apply --change "<name>" --json
```

Succeed only when:

- strict validation passes;
- every planning artifact is `done` or intentionally `skipped`;
- apply state is `ready`;
- the task list contains actionable pending work;
- no new contradiction or unresolved material decision remains;
- every mandatory pre-implementation approval is represented by real attributable evidence or remains an explicit blocker.

If a check fails, report it and return to the appropriate planning or decision step. Do not start implementation.

## Report and hand off

Use:

```text
## OpenSpec Grilling Complete

Change: <name>
Schema: <schema-name>
Validation: passed
Planning artifacts: complete
Apply state: ready
Tasks: <remaining>/<total> pending

### Decisions resolved
- ...

### Artifacts reconciled
- ...

### Accepted risks
- ...

### Evidence status
- ...

The change is ready for the OpenSpec apply workflow.
```

Report exact artifacts written, evidence limitations, and residual risks. Never imply that local or generated changes reached a source repository unless that write was confirmed.

Stop after reporting readiness. Recommend `openspec-apply-change` as the next skill, but invoke it only when the user separately asks to implement.

## Routing summary

- Incomplete planning → `openspec-plan-change` or `openspec-propose`.
- Unresolved change direction → `openspec-brainstorming`.
- Implementation already complete → `openspec-verify-change`.
- Valid, reconciled, apply-ready change → `openspec-apply-change` after an explicit implementation request.
- Do not route directly to `openspec-lifecycle`; verification must follow implementation first.
