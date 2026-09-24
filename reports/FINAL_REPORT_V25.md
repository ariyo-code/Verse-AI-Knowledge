# V25 Final Engineering Report

## Release

- Release: **25.0.0**
- Schema: **25**
- Codename: **Professionalization, API Expansion & Reproducible Verification**
- Verse API snapshot: **42.20**
- Source baseline: V24 commit `1928e298a52414f27464aaa388456dd56e264cb4`
- V25 GitHub CI: **UNKNOWN until this package is pushed**

## What changed

V25 keeps the V24 evidence model and professionalizes the repository around reproducibility, current-vs-legacy separation, packaging, prompt generation, SDK/CLI/MCP access, security, release automation, documentation, and measurable retrieval quality.

Compared with the V24 source package used for this build:

- source files: **597**
- V25 package files: **701**
- files created: **104**
- files modified: **69**
- files removed: **0**

No compatibility file was silently deleted.

## Major implementation areas

### Prompt architecture

- Canonical `prompt_sources/` introduced.
- `tools/build_prompts.py` deterministically generates the public/current portable prompts.
- `portable/current/` is the current pack; historical material is retained under `portable/archive/`.
- Prompt consistency and prompt-injection boundary tests were added.

### Python product surface

- `KnowledgeBase` SDK façade.
- Expanded `verse-ai` CLI: version, explain, status, evidence, provenance, API diff, snapshot and JSON-oriented workflows.
- Optional official MCP Python SDK server in `mcp/server.py`, with read-only evidence-aware tools.
- Package metadata and optional dependency groups for dev/docs/MCP use.

### API knowledge

- Existing field-level evidence model retained.
- Candidate/review/versioning scaffolding added.
- API snapshots and diff tooling added.
- Event-payload, enum/inheritance and versioning work are explicitly separated from verified knowledge.
- Automated harvesting remains candidate-only; it does not auto-promote exact claims.

### RAG / evaluation

- Retrieval benchmark expanded to **104 cases**.
- Current measured retrieval metrics:
  - Recall@1: **0.1346**
  - Recall@5: **1.0000**
  - Recall@10: **1.0000**
  - MRR: **0.4905**
  - nDCG@10: **0.6194**
- Hard-negative coverage is included.
- RAG indexing excludes tests, eval corpora, generated reports, caches, build artifacts and other self-retrieval leakage paths.

### GitHub / release engineering

- V25 CI workflow.
- CodeQL workflow.
- Dependabot for GitHub Actions and pip.
- CODEOWNERS.
- Issue Forms + issue configuration.
- Recommended branch ruleset template.
- GitHub Pages documentation workflow.
- Tag-driven release workflow with validation, package build, clean-wheel smoke test, coverage snapshot, release audit, portable artifact and SHA-256 checksums.

### Documentation / governance

- Professional README and roadmap.
- MkDocs Material site configuration.
- Current/legacy documentation separation.
- Improved Security, Contributing and Code of Conduct files.
- Structured third-party manifest.
- Supply-chain guidance.

## API coverage

Measured against symbols currently known to this repository — **not** against the unknown total size of Epic's entire API surface:

- structured symbols: **164**
- modules represented: **9**
- symbol presence: **164 / 164**
- signature verified: **12 / 164**
- structured parameters: **12 / 164**
- structured return types: **12 / 164**
- structured effects: **12 / 164**
- event names known: **24 / 164**
- event payloads verified: **0 / 164**
- members known: **42 / 164**
- exact signature claims allowed: **12 / 164**
- presence-only symbols: **152**

V25 deliberately does not fabricate missing API data to increase these numbers.

## Validation actually executed in the build environment

### PASS

- Python syntax/compileall for `src`, `tools`, `tests`, `mcp`.
- V25 integrity validator.
- generated-file drift and current prompt drift.
- repository integrity.
- verification evidence checks.
- internal-path validation.
- current-tree high-confidence secret scan.
- API revalidation gate (`42.20`, no stale verified evidence detected).
- API coverage report.
- retrieval benchmark: **8/8** legacy cases.
- retrieval metrics suite: **104 cases**.
- evidence benchmark: **3/3**.
- deterministic anti-hallucination policy eval: **14/14**.
- preflight.
- pytest: **13/13 passed**.
- Python coverage was measured during validation: **41%** over `src/verse_ai_knowledge/` in this environment.
- full `tools/validate_all.py` suite.
- editable package installation smoke test.
- wheel build with `pip wheel --no-build-isolation`: **PASS**.

### NOT RUN in this local build environment

- Ruff: dependency not available in the execution environment.
- mypy: dependency not available in the execution environment.
- MkDocs strict build: documentation dependencies not available in the execution environment.
- official MCP SDK runtime/Inspector test: optional MCP dependency not installed locally.

The V25 GitHub workflows install these dependencies and are configured to run the corresponding checks after push. They are **not** marked PASS here.

## External / unavailable validation

- UEFN compile: **NOT TESTED**
- Runtime: **NOT TESTED**
- Multiplayer: **NOT TESTED**
- End-to-end live LLM benchmark: **SKIPPED — no provider configured**
- GitHub V25 CI: **UNKNOWN — package not yet pushed**
- GitHub Pages activation/settings: **MANUAL ACTION REQUIRED** if not already enabled
- Branch protection/ruleset application: **MANUAL ACTION REQUIRED**
- Private Vulnerability Reporting setting: **MANUAL ACTION REQUIRED** if unavailable
- PyPI publication: **NOT PERFORMED** by design

## Security notes

The current working tree passed the repository high-confidence secret scanner. This does **not** prove historical Git commits never contained secrets. A historical scan with a tool such as gitleaks is recommended in a Git-enabled environment.

Remote documentation and retrieved material remain **data, not instructions**. Exact Verse claims still require evidence, and unverified exact claims must remain `TODO(API VERIFY)`.

## Publication state

The package itself passed the static/repository tests available in this environment. Final GitHub publication readiness remains:

```text
PUBLICATION READINESS: UNKNOWN
```

until the V25 package is pushed and the actual V25 GitHub CI run succeeds.

## Recommended next milestone

Do not perform another broad structural rewrite. The highest-value next work is evidence acquisition:

1. expand verified API signatures/parameters/returns/effects;
2. verify event payloads;
3. add real UEFN compile/runtime/multiplayer evidence through VerseLab/self-hosted Windows infrastructure;
4. run the provider-neutral LLM benchmark with real model outputs;
5. improve Recall@1 while preserving hard-negative rejection and evidence authority.
