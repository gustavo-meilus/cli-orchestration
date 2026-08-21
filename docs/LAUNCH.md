# Launch Kit and Gate

## Repository metadata

**Description:** Choose the minimum sufficient execution tactic for coding-agent work: direct by default, with focused discovery and fresh verification only when justified.

**Topics:** `ai-agents`, `coding-agents`, `cli`, `codex-cli`, `claude-code`, `copilot-cli`, `multi-agent`, `orchestration`, `openspec`, `developer-tools`

Leave homepage empty until a maintained project site exists. Export `assets/brand/social-preview.svg` to a visually inspected 1280×640 PNG, then upload it under **Settings → Social preview**; committing the source does not activate it. See [GitHub's social-preview guidance](https://docs.github.com/en/enterprise-cloud@latest/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview).

## Existing historical release

**Existing release:** `v2.0.0 — Lean control. Fresh proof.`

Tag `v2.0.0` and its GitHub release already exist under the historical pre-rebrand project identity. Preserve that tag, release, title, assets, and history unchanged.

The TacticSwitch branding-only change keeps version `2.0.0` for package and protocol compatibility, but it creates no release or tag and does not bump the version. Any future release is a separate decision and must pass final tests/checksums from its exact commit before a new tag is created. [GitHub releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases) are tag-based deployable records.

## Announcement copy

**Short post:**

> Agent workflows often use the wrong formation: one overloaded context or extra contexts, repeated reads, and review stages whether they help or not. TacticSwitch selects the minimum sufficient tactic—direct by default, fresh verification for material work, Scout only for real uncertainty. It is a portable control plane for Codex CLI, Claude Code, and Copilot CLI, with experimental adapters and honest fail-closed boundaries. I’d value feedback from maintainers on which task classes actually justify an extra context.

**Long-form opening:**

> I built TacticSwitch after seeing agent workflows optimize for either one overloaded context or a mandatory committee pipeline. Clear local work stays direct; material behavior changes use one Implementer and a fresh Verifier; a Scout appears only when discovery can prevent churn. It is deliberately a pure control plane, so OpenSpec, TDD, or another task system keeps owning the development method. The adapters are experimental, and the current real benchmark is narrow: direct mode completed one Codex fixture while orchestrated routes failed closed when collaboration threads were unavailable. I’m looking for reproducible field evidence, especially cases where fresh verification changes the outcome.

## Rebrand checklist

- [x] Add the [MIT License](../LICENSE) with SPDX-standard license text.
- [x] Publish the renamed public repository at [gustavo-meilus/tacticswitch](https://github.com/gustavo-meilus/tacticswitch) with the documented description and focused [topics](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics).
- [x] Enable private vulnerability reporting and link the private report form from `SECURITY.md`.
- [ ] Export/upload the social preview and verify a shared-link preview.
- [x] Set `main` as default; block force-pushes and deletion; require linear history and resolved review conversations; disable Wiki and Projects.
- [x] Validate the exact rebrand commit with the full test suite and `python scripts/checksums.py --verify`.
- [x] Confirm every adapter label matches `manifest.json`.

## Release checklist

- [ ] Test README installation commands in a clean temporary repository.
- [ ] For a future release, choose its version and create the matching new tag and release only after all blockers pass.

## Post-launch checklist

- [ ] Publish channel-specific posts with the real release URL and one specific evidence request.
- [ ] Watch first-user install failures, documentation gaps, and worker-availability reports.

Participate where maintainers already discuss coding-agent reliability. The [Open Source Guides](https://opensource.guide/finding-users/) recommends clarifying beneficiaries and meeting them where they gather.
