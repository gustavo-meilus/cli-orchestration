---
type: "query"
date: "2026-08-16T04:55:49.710465+00:00"
question: "Those will use the general-purpose? There's similar tool like general-purpose available on all three tools? This would make it simpler or more complex?"
contributor: "graphify"
outcome: "useful"
source_nodes: ["Six-Role Separation", "Role Instructions and Runtime Permission Boundary", "Control Packet Contract", "Review Validation and Audit Acceptance Gates"]
---

# Q: Those will use the general-purpose? There's similar tool like general-purpose available on all three tools? This would make it simpler or more complex?

## Answer

Expanded from original query via vocab: [agent, default, generic, role, six, separation, control, permission, write, validation]. Functionally all three CLIs provide a generic full-capability subagent: Codex names it default, Claude Code and Copilot CLI name it general-purpose. KISS recommendation: use these built-ins as the portable runtime substrate, but preserve Inspector, Planner, Executor, Reviewer, Validator, and Final Auditor as logical prompt contracts and separate threads. Centralize role prompts in one canonical roles reference and keep only a tiny per-CLI spawn-name/syntax mapping. This simplifies installation and avoids eighteen platform-specific agent profiles. Tradeoff: generic agents have broad tools and weaker permission isolation, so one-writer enforcement, fresh reviewer/auditor thread IDs, exact output packets, and no-edit instructions remain mandatory. Native custom profiles can remain an optional hardened tier for sandboxing and model tuning.

## Outcome

- Signal: useful

## Source Nodes

- Six-Role Separation
- Role Instructions and Runtime Permission Boundary
- Control Packet Contract
- Review Validation and Audit Acceptance Gates