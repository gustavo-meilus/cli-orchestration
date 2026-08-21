# Launch Kit and Gate

## Repository metadata

**Description:** Portable lean control plane for coding-agent CLIs. Direct by default; focused discovery and fresh verification only when the work justifies it.

**Topics:** `ai-agents`, `coding-agents`, `cli`, `codex-cli`, `claude-code`, `copilot-cli`, `multi-agent`, `orchestration`, `openspec`, `developer-tools`

Leave homepage empty until a maintained project site exists. Export `assets/brand/social-preview.svg` to a visually inspected 1280×640 PNG, then upload it under **Settings → Social preview**; committing the source does not activate it. See [GitHub's social-preview guidance](https://docs.github.com/en/enterprise-cloud@latest/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview).

## Release copy

**Title:** `CLI Orchestration 2.0.0 — Lean control. Fresh proof.`

> CLI Orchestration 2.0.0 is a portable, lean control plane for coding-agent CLIs. Clear local work stays direct; material work can route through an Implementer and fresh Verifier; uncertain work can add a focused Scout. The core preserves OpenSpec and methodology ownership and fails closed when a required independent worker is unavailable. Codex, Claude Code, and Copilot CLI adapters are experimental. The current benchmark is one narrow Codex fixture, not a general performance or route-quality result.

Do not create a release until final tests/checksums pass from the exact commit and repository settings are applied. [GitHub releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases) are tag-based deployable records.

## Announcement copy

**Short post:**

> Agent workflows often pay an orchestration tax: extra contexts, repeated reads, and review stages whether they help or not. CLI Orchestration uses the minimum sufficient topology—direct by default, fresh verification for material work, Scout only for real uncertainty. It is a portable control plane for Codex CLI, Claude Code, and Copilot CLI, with experimental adapters and honest fail-closed boundaries. I’d value feedback from maintainers on which task classes actually justify an extra context.

**Long-form opening:**

> I built CLI Orchestration after seeing agent workflows optimize for either one overloaded context or a mandatory committee pipeline. Clear local work stays direct; material behavior changes use one Implementer and a fresh Verifier; a Scout appears only when discovery can prevent churn. It is deliberately a pure control plane, so OpenSpec, TDD, or another task system keeps owning the development method. The adapters are experimental, and the current real benchmark is narrow: direct mode completed one Codex fixture while orchestrated routes failed closed when collaboration threads were unavailable. I’m looking for reproducible field evidence, especially cases where fresh verification changes the outcome.

## Manual publication checklist

- [x] Add the [MIT License](../LICENSE) with SPDX-standard license text.
- [ ] Confirm the public owner/name and remote; apply the description and focused [topics](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics).
- [ ] Confirm private vulnerability reporting is enabled and the direct link in `SECURITY.md` opens the private report form.
- [ ] Export/upload the social preview and verify a shared-link preview.
- [ ] Confirm `main`, intentional branch protection/rules, and only maintainable repository features.
- [ ] Run full tests and `python scripts/checksums.py --verify` from the exact release commit.
- [ ] Test README installation commands in a clean temporary repository.
- [ ] Confirm every adapter label matches `manifest.json`.
- [ ] Tag `v2.0.0` and create the release only after all blockers pass.
- [ ] Publish channel-specific posts with the real release URL and one specific evidence request.
- [ ] Watch first-user install failures, documentation gaps, and worker-availability reports.

Participate where maintainers already discuss coding-agent reliability. The [Open Source Guides](https://opensource.guide/finding-users/) recommends clarifying beneficiaries and meeting them where they gather.
