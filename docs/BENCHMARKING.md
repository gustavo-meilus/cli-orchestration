# Route Benchmarking

## Compared routes

A. Direct execution / framework-native process only  
B. Implementer → fresh Verifier  
C. Scout → Implementer → fresh Verifier

Use representative small-local, material-well-specified, and materially-uncertain workloads with the same acceptance criteria. Do not force an unsuitable route merely to fill a table; record that mismatch.

## Record

For every run capture: final correctness; verifier-caught defects; elapsed time; observable input/output tokens and cost; model turns; tool calls; repeated file/spec reads; test executions; rework cycles; final diff churn; and user interventions. Record CLI/model/version and missing telemetry explicitly.

## Promotion rule

- If Verifier rarely catches material defects for a class, consider direct implementation plus native checks for that class.
- If Scout rarely changes route/scope/ownership/dependencies, remove Scout from that class.
- Strengthen a model or add a stage only when its marginal quality benefit justifies latency/cost.
- Publish inconclusive or unavailable measurements as limitations, not defaults.

## Current evidence

The matched `simple-add` field corpus is recorded in `benchmarks/results/codex-0.148.0-2026-08-20.json` and summarized in `BENCHMARK-RESULTS.md`. Route A completed. Routes B/C returned honest fail-closed `BLOCKED` results because `codex exec` could not create a collaboration thread. This measures the current runtime availability boundary but does not provide comparative completed-route quality, so model/stage tuning remains unpromoted.
