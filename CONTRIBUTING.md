# Contributing

Thanks for helping make TacticSwitch smaller, more portable, and better evidenced.

## Before opening a change

- Use an issue for behavior changes, adapter promotion, public compatibility claims, or protocol changes.
- Keep external frameworks authoritative; do not copy or modify canonical `.agents/skills/openspec-*` resources.
- Treat `manifest.json` as the adapter-evidence authority and keep limitations adjacent to claims.
- Prefer the smallest topology or implementation that satisfies the verified need.

## Development

Requires Python 3.10+. Create a branch from `main`, make a focused change, and run:

```bash
python -m unittest discover -s tests -v
python scripts/checksums.py --verify
```

If release assets changed, regenerate hashes with `python scripts/checksums.py --write`. Installer changes need a fresh temporary project, repeated install, and affected tool selections. Adapter claims need CLI version, exact fresh-process procedure, discovery/invocation result, generic-worker evidence, and fail-closed behavior; static parsing alone cannot promote an adapter.

## Pull requests

Keep one coherent responsibility per pull request. Explain the user problem, authority/specification, risks, validation, and field evidence still missing. Exclude generated caches, bytecode, and secrets.

By participating, follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Report vulnerabilities through [SECURITY.md](SECURITY.md), not a public issue.

Contributions are accepted under the repository's [MIT License](LICENSE).
