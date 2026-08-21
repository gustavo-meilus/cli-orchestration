# Changelog

## 2.0.0 - 2026-08-20

- Replaced the mandatory six-role default with adaptive direct, read-only, Implementer → Verifier, and Scout → Implementer → Verifier routes.
- Preserved a pure primary control plane whenever orchestration is active.
- Added CLI-neutral Scout, Implementer, and fresh-Verifier contracts, context-affinity batching, one-writer ownership, bounded rework, and fail-closed worker availability.
- Made Planner, Validator, Final Auditor, legacy aliases, and specialists optional high-assurance resources.
- Reduced resumable state to optional compact schema v2 with conservative v1 migration and fresh reconciliation.
- Converted the OpenSpec entry into a thin bridge around canonical apply and verify; canonical OpenSpec resources remain package-excluded.
- Added selected single/multi-tool installation with Codex default, thin Codex/Claude/Copilot adapters, optional Codex hardening, attribute-safe atomic replacement, migration backups, and deterministic verification fixtures.
- Aligned package, protocol, manifest, documentation, checksum, and verifier version surfaces on `2.0.0`.
- Limited support status to `experimental|supported` and made the manifest the evidence authority.

## 1.1.0 - 2026-08-15

Superseded. Required the six-role pure-orchestrator workflow and introduced portable adapters/state v1.

## 1.0.0 - 2026-08-15

Initial Codex/OpenSpec orchestration package.
