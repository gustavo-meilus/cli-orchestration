# OpenSpec Integration

OpenSpec owns proposal, specifications, design, tasks, apply, verification, sync, archive, and `.agents/skills/openspec-*`. TacticSwitch owns only route selection, context assignment, dependency/ownership coordination, and route acceptance.

## Routes

- Clear low-risk change: canonical `$openspec-apply-change` directly, then native checks.
- Material change: Implementer uses canonical apply; fresh Verifier checks artifacts and actual state, optionally using canonical `$openspec-verify-change` as conformance evidence.
- Material uncertainty: Scout first.
- Read-only request: only required read-only contexts.

OpenSpec `[x]` means task progress. OpenSpec Verify means specification-conformance evidence. Neither automatically substitutes for a required fresh-Verifier `PASS`.

## Composition

Approved OpenSpec artifacts remain requirements/design/task authority. TDD or another framework may add process order, but one orchestration owner assigns implementation. Normal routes do not stack Reviewer, Validator, Final Auditor, and OpenSpec Verify. Add a gate only for a distinct documented risk.

If implementation exposes material drift, stop the affected scope and use canonical OpenSpec update/reconciliation before continuing. Installation and migration preserve canonical skill bytes.
