# Brainstorm Into an OpenSpec Proposal

Convert exploration into a coherent, implementation-ready OpenSpec change:

`recover → ground → scope → resolve → diverge → falsify → contract → approve → propose → validate → review`

## Hard gates

- Do not write application code, scaffold implementation, or modify product files.
- Do not create the OpenSpec change until the user explicitly approves the change contract.
- Treat silence, earlier exploration agreement, or approval of an approach as insufficient approval of the final contract.
- End with a validated, user-reviewed OpenSpec change ready for apply—not implementation.

## Working principles

- **Reuse exploration:** Recover known facts, decisions, options, risks, and evidence from the conversation. Never make the user repeat known information.
- **Ground in reality:** Verify material claims against the repository, existing specs, tests, and OpenSpec configuration.
- **Separate certainty:** Distinguish observed facts, user decisions, assumptions, and open questions.
- **One cohesive change:** Split independent outcomes before proposing.
- **One question at a time:** Ask only questions whose answers could change scope, requirements, design, migration, or tasks.
- **Diverge before converging:** Compare genuinely different approaches and recommend one.
- **Falsify the recommendation:** Record evidence that would reverse the decision and regression behavior that must remain protected.
- **Approve before writing:** Present a concise change contract and obtain explicit approval.
- **Let OpenSpec define artifacts:** Follow the selected schema and `openspec instructions`; do not assume every schema is spec-driven.
- **Review before apply:** Strict validation is necessary but does not replace cross-artifact coherence or user review.

## 1. Recover the exploration handoff

Recover from the conversation and supplied artifacts:

- problem and affected users
- current behavior and workaround
- desired outcome and urgency
- relevant files, modules, APIs, data models, tests, and existing capabilities
- constraints, compatibility requirements, and preserved behavior
- options already considered and rejected
- user decisions
- risks, unknowns, and prior evidence

Classify consequential information internally as:

- **Observed fact** — verified in code, specs, tests, or configuration
- **User decision** — explicitly chosen
- **Assumption** — reasonable but unverified
- **Open question** — unresolved and capable of changing the proposal

Only material open questions should interrupt the flow.

## 2. Resolve the OpenSpec context

When the user names a registered store or the work belongs to one, run:

```bash
openspec store list --json
```

Resolve its store ID and preserve `--store <id>` on commands that accept it, including `new change`, `status`, `instructions`, `list`, `show`, `validate`, `archive`, `doctor`, `context`, and `view`.

Without a selected store, use the nearest initialized local OpenSpec root. Run:

```bash
openspec list --json
```

Use the returned root and planning context instead of assuming paths. Read `openspec/config.yaml` or `openspec/config.yml` at that root when present:

- Treat `context` as project facts and constraints.
- Treat `rules` as artifact-specific instructions.
- Apply both as instructions; do not copy them mechanically into artifacts.

If a relevant active change exists, run:

```bash
openspec status --change "<name>" --json
```

Read existing artifacts from `artifactPaths.<artifact>.existingOutputPaths`. Do not silently overwrite or duplicate a change. Determine from the conversation whether to refine it or create a distinct change.

Inspect extra repository files only to close factual gaps. Do not restart broad exploration by default. If no initialized project or resolvable store exists, stop and tell the user what prerequisite is missing.

## 3. Check scope before details

Represent one outcome that can be reviewed, implemented, and validated as a unit. Split the request when it contains independent:

- user outcomes
- services or products
- capabilities with separate rollout or acceptance criteria
- migrations
- behavioral features and unrelated cleanup

For an oversized request:

1. Show the natural slices and dependencies.
2. Recommend the smallest valuable first slice.
3. Ask the user to approve that slice.
4. Continue only with the approved slice.

Do not hide several projects inside one umbrella proposal.

## 4. Resolve proposal-critical questions

Maintain a working decision record covering:

- goal
- problem and current behavior
- affected users or systems
- desired observable behavior
- in scope and out of scope
- constraints and preserved behavior
- compatibility and migration
- success criteria
- important failure and edge cases
- assumptions and open questions

Ask one question per message. Prefer concrete options when the decision space is known, while allowing the user to supply another answer. Use an open question when options would conceal meaningful possibilities.

Prioritize questions about:

1. outcome
2. scope boundaries
3. observable behavior
4. authorization, privacy, safety, or compliance
5. failures and recovery
6. compatibility and migration
7. measurable success

Do not ask about details that can safely remain design decisions. When a non-critical detail follows repository conventions, adopt a conservative assumption and disclose it in the contract. Stop questioning when remaining unknowns cannot change the proposal, specs, design, or tasks.

## 5. Compare approaches

Present two or three genuinely different approaches. Include:

1. the recommended approach
2. a credible alternative
3. the smallest viable or no-build intervention when applicable

For each, summarize:

- central mechanism and fit with the current system
- observable behavior
- benefit, complexity, and operational cost
- compatibility and migration impact
- risks and reversibility
- testing implications
- deliberately omitted scope

Apply YAGNI: remove speculative extensibility, avoid unrelated refactoring, prefer existing patterns, and distinguish necessary enabling work from optional cleanup.

Ask the user to choose or approve an approach. Silence is not approval. For a very small change, keep the comparison brief but identify at least one rejected alternative or explain why the existing pattern is clearly preferable.

## 6. Falsify before convergence

Steelman the recommendation, then record:

- at least one credible, decision-relevant counterexample
- one observable falsification criterion
- the response if that criterion is met: revise, stage, defer, or reject
- at least one regression scenario protecting accepted behavior
- relevant adoption friction, maintenance burden, source-of-truth conflicts, abuse cases, or operational failure modes

Do not call supportive prose stronger evidence. An evidence gate passes only when the counterexample is plausible, the falsification criterion is observable, the response is explicit, and regression behavior is protected.

## 7. Present the change contract

Before creating files, present:

```markdown
## Proposed OpenSpec Change

**Name:** <kebab-case-name>

**Goal:** <one-sentence outcome>

**Why:** <problem and why it matters>

**In Scope**
- ...

**Out of Scope**
- ...

**Capabilities**
- New: <kebab-case capability names or none>
- Modified: <exact existing capability names or none>

**Behavior Contract**
- <observable requirement and scenario summary>

**Design Direction**
- <chosen approach and consequential decisions>

**Compatibility / Migration**
- ...

**Verification**
- ...

**Assumptions**
- ...

**Falsification and Regression Gates**
- ...

**Rejected Alternatives**
- ...

**Open Questions**
- None
```

Inspect existing `openspec/specs/` names before listing modified capabilities. Do not call an implementation detail a capability. When no spec-level behavior changes, explicitly plan `skip_specs: true`; do not invent a requirement merely to satisfy validation.

Resolve every question that could change scope, requirements, approach, migration, or task decomposition. For a straightforward change, present the contract once. For a complex or high-risk change, review it in sections before presenting the consolidated contract.

Ask for explicit approval of the complete contract. Do not create the change before approval.

## 8. Run the proposal workflow

After approval, invoke `openspec-propose` with the approved contract as its source input. Require it to:

- preserve approved scope, decisions, exclusions, assumptions, and evidence gates
- use verified repository facts
- follow the selected schema
- generate every artifact transitively required by apply
- treat each artifact's `openspec instructions` output as authoritative
- avoid reopening settled decisions unless a new critical conflict appears

If direct skill invocation is unavailable, execute the equivalent CLI workflow:

1. Create the change:

   ```bash
   openspec new change "<name>"
   ```

2. For a behavior-free change, set `skip_specs: true` in `.openspec.yaml`.
3. Read the artifact graph:

   ```bash
   openspec status --change "<name>" --json
   ```

4. Compute the required closure from `applyRequires` by recursively following each artifact's `requires` edges. Do not rely on status alone; status is output-existence based.
5. For each missing artifact in dependency order, run:

   ```bash
   openspec instructions <artifact-id> --change "<name>" --json
   ```

6. Treat the response as authoritative:
   - apply `context` and `rules` without copying them
   - reread dependency files from disk
   - use `template` and `instruction`
   - honor `skipped` and `warning`
   - invoke delegated skills or commands when instructed
   - write to concrete paths, never to a literal glob
   - verify output existence
7. Rerun status after every artifact.
8. Stop when every artifact in the required closure is done, explicitly skipped, or omitted because its own instruction makes it conditional.

Skip specs only through `skip_specs`. Omit a conditional design only when its instruction permits it.

## 9. Validate and self-review

Run:

```bash
openspec validate "<name>" --strict
```

Review artifacts in this order: proposal, delta specs, design when present, then tasks.

### Proposal

- represents one coherent outcome
- matches approved scope and exclusions
- uses correct capability names
- contains no speculative or unrelated work
- identifies breaking changes

### Specs

- state observable behavior rather than implementation
- use normative SHALL or MUST requirements
- include at least one `#### Scenario` per requirement
- cover relevant success, failure, validation, authorization, recovery, and compatibility cases
- give new capabilities a meaningful Purpose
- include complete requirement blocks under MODIFIED
- use ADDED, MODIFIED, REMOVED, and RENAMED correctly

### Design

- implements the approved behavior
- explains consequential decisions and alternatives
- follows repository patterns or justifies deviations
- addresses relevant security, performance, migration, rollout, and rollback concerns
- contains no question that could change requirements, approach, or tasks

### Tasks

- every task uses `- [ ]`
- tasks are ordered and independently verifiable
- requirements have implementation and test coverage
- no task adds out-of-scope work
- no task depends on an unresolved decision

### Cross-artifact coherence

- proposal capabilities match spec directories
- specs match the approved behavior contract
- design satisfies the specs
- tasks implement the specs through the design
- names, constraints, APIs, evidence gates, and migration steps agree
- no TBD, TODO, placeholder, contradiction, or material ambiguity remains

Fix issues in the OpenSpec artifacts and rerun:

```bash
openspec validate "<name>" --strict
openspec status --change "<name>"
```

Do not proceed while strict validation fails.

## 10. Request user review and hand off

Summarize:

- change name and resolved location
- selected schema
- artifacts created
- conditional artifact omitted and why, if any
- assumptions and evidence gates retained
- strict-validation result

Ask the user to review the written artifacts. When changes are requested:

1. update the relevant artifact
2. propagate the decision through dependent artifacts
3. repeat the coherence review
4. rerun strict validation
5. ask for review again

Do not start implementation until the user approves the artifacts. After approval, state that all planning artifacts required for implementation are ready and point to the apply surface installed for the current tool. Use the invocation shown by OpenSpec or generated for that tool; do not assume all tools spell it the same way.

## Guardrails

- Use after exploration or when the user explicitly wants structured convergence into an OpenSpec proposal.
- Do not make this workflow mandatory for every creative task.
- Do not implement application code.
- Do not ask the user to repeat known findings.
- Ask one material question at a time.
- Decompose oversized work before proposing.
- Present alternatives and recommend one.
- Require a credible falsification gate and protected regression behavior.
- Obtain explicit contract approval before creating artifacts.
- Keep the change focused and reject unrelated refactoring.
- Follow the selected schema and `openspec instructions`.
- Reread dependencies from disk before generating downstream artifacts.
- Use CLI-resolved roots, stores, paths, and action context.
- Never write to a glob as if it were a file.
- Use `skip_specs: true` only when behavior does not change.
- Strictly validate and repair inconsistencies before review.
- Do not commit, push, create branches, or open pull requests unless separately requested.
- Hand off only to the OpenSpec apply workflow after user approval.
