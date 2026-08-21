# Model and Stage Policy

The portable protocol specifies logical responsibilities, not model products. Each adapter may recommend a model/reasoning setting, but the recommendation remains provisional until current product documentation and representative workload evidence support it.

KISS defaults:

- direct mode: active CLI model;
- Scout: a cost-efficient model sufficient for bounded read-only discovery;
- Implementer: a model appropriate to material code changes;
- Verifier: a fresh high-attention context; use a stronger model for genuine high risk before adding routine stages.

Do not infer that a subagent is cheaper than the primary. Measure total task success, latency, tokens/cost where observable, repeated context reads, tool calls, rework, and interventions. Model identity does not determine Verifier freshness.

Current product names, availability, effort controls, and economics change independently of this package. Revalidate authoritative vendor documentation before publishing an adapter recommendation.
