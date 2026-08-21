# Release 2.0 Route Benchmark

Date: 2026-08-20  
Runtime: `codex-cli 0.148.0`  
Fixture: `benchmarks/simple-add`  
Raw reproducible record: `benchmarks/results/codex-0.148.0-2026-08-20.json`

Each route began from the same isolated defect: `add(2, 3)` returned `-1`, while one unittest expected `5`. Temporary workspaces were automatically removed. Setup files and Python caches were excluded from diff churn.

| Metric | A: Direct | B: Implementer → Verifier | C: Scout → Implementer → Verifier |
|---|---:|---:|---:|
| Outcome | Completed | BLOCKED at Implementer spawn | BLOCKED at Scout spawn |
| Correctness assessment | PASS | FAIL (unchanged fixture) | FAIL (unchanged fixture) |
| Elapsed seconds | 21.481 | 26.790 | 26.413 |
| Turns | 1 | 1 | 1 |
| Observable tool calls | 4 | 1 | 1 |
| Observable test runs, including independent assessment | 2 | 1 | 1 |
| Observable repeated file reads | 0 | 0 | 0 |
| Rework cycles | 0 | 0 | 0 |
| Verifier-caught defects | 0 | 0 (Verifier never created) | 0 (Verifier never created) |
| Diff churn | 1 file | 0 files | 0 files |
| User interventions | 0 | 0 | 0 |
| Input tokens | 88,140 | 56,632 | 56,742 |
| Cached input tokens | 70,400 | 45,312 | 45,312 |
| Output tokens | 436 | 596 | 615 |
| Cost | unavailable | unavailable | unavailable |

Routes B and C obeyed fail-closed semantics. `codex exec` returned `collab spawn failed: no thread with id ...`; neither route silently implemented in the primary. These are actual field outcomes and worker-availability evidence, but they are not completed-route quality comparisons.

## Tuning decision

No additional stage, stronger model, or adapter model recommendation is promoted. Route A demonstrates direct-mode viability for this small local fixture. B/C show that this `codex exec` environment cannot currently execute the orchestrated topologies; they do not show that those topologies lack quality value. Re-run the same harness when native collaboration threads are available.
