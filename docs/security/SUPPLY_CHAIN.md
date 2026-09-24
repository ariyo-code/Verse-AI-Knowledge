# Supply-chain policy

GitHub Actions and Python dependencies are reviewed as part of repository maintenance.

- Dependabot tracks `github-actions` and `pip` dependencies.
- Critical workflows should prefer immutable action SHAs once a maintainer has verified the exact upstream revision.
- A floating major tag such as `actions/checkout@v4` is easier to maintain but is not equivalent to an immutable pin.
- Release artifacts include SHA-256 checksums.
- Third-party vendored code is tracked separately in `THIRD_PARTY_MANIFEST.json`.

Do not pin an action to an unverified SHA merely to appear more secure.
