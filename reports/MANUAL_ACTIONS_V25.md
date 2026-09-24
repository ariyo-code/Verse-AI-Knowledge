# Manual actions remaining

These items cannot be truthfully completed by static repository tooling alone:

1. **UEFN compile/runtime/multiplayer** — connect a real Windows UEFN/VerseLab environment and record evidence.
2. **Live LLM benchmark** — configure a provider or supply saved model outputs; otherwise the harness must remain SKIPPED.
3. **GitHub Pages** — enable Pages for the repository if the workflow is not already authorized.
4. **Branch protection/ruleset** — enable required CI, block force pushes/deletion, and require PR/review policy as desired.
5. **Private vulnerability reporting** — enable repository Security settings if unavailable.
6. **GitHub topics** — apply the list in `docs/GITHUB_TOPICS.md` if repository settings are not automated.
7. **PyPI** — package metadata is prepared, but publishing is intentionally not performed.
