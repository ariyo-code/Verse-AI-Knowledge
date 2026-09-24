# Changelog

## 25.0.0 — Professionalization, API Expansion & Reproducible Verification

### Added
- Canonical prompt compiler and current/archive portable layout.
- Python `KnowledgeBase` SDK, expanded CLI, evidence/explain/status/version commands.
- Local provider-neutral knowledge server bridge.
- V25 API candidate/versioning schemas and diff tooling.
- 100+ retrieval stress cases and metric runner.
- MkDocs site configuration, CodeQL, Dependabot, CODEOWNERS, Issue Forms and release workflow.
- Reproducible release audit generator and structured third-party manifest.

### Changed
- Public prompt is generated from canonical prompt sources.
- Generated-code provenance terminology is now “machine-readable provenance comment”.
- Python packaging/quality configuration is standardized.
- Current-vs-legacy prompts are explicitly separated.

### Validation
- Static/Python checks do not constitute UEFN compilation.
- UEFN compile/runtime/multiplayer remain NOT TESTED unless real evidence is recorded.
- LLM benchmark remains SKIPPED unless explicitly configured.


## 25.0.0 — Professionalization, API Expansion & Reproducible Verification

### Added
- Canonical prompt compiler and current/archive portable layout.
- Python `KnowledgeBase` SDK, expanded CLI, evidence/explain/status/version commands.
- Local provider-neutral knowledge server bridge.
- V25 API candidate/versioning schemas and diff tooling.
- 100+ retrieval stress cases and metric runner.
- MkDocs site configuration, CodeQL, Dependabot, CODEOWNERS, Issue Forms and release workflow.
- Reproducible release audit generator and structured third-party manifest.

### Changed
- Public prompt is generated from canonical prompt sources.
- Generated-code provenance terminology is now “machine-readable provenance comment”.
- Python packaging/quality configuration is standardized.
- Current-vs-legacy prompts are explicitly separated.

### Validation
- Static/Python checks do not constitute UEFN compilation.
- UEFN compile/runtime/multiplayer remain NOT TESTED unless real evidence is recorded.
- LLM benchmark remains SKIPPED unless explicitly configured.


## 24.0.0 — Claim Resolution, Evidence Graph & Continuous Verification

### Added

- field-level API claim resolution with `ALLOW` / `TODO(API VERIFY)`;
- generated API evidence graph linking symbol fields to supporting evidence;
- API-version revalidation state and strict stale-evidence gate;
- conservative Verse API-claim linting;
- coverage snapshots and deterministic release-to-release diffs;
- redirect-safe, hostname-strict Epic documentation fetching;
- provider-optional end-to-end LLM evaluation harness under `evals/llm/`;
- public-release checks for internal paths and likely secrets;
- V24 visible + hidden generated-code provenance;
- V24 integrity, claim-resolution, provenance, URL-security and LLM-runner tests.

### Changed

- exact claims are resolved per field instead of from symbol-level confidence alone;
- generated API data now carries `field_evidence`, `claim_state`, and `revalidation`;
- `verse-ai` exposes claim, lint, coverage-snapshot/diff and LLM-eval workflows;
- CI is upgraded to V24 and keeps UEFN truth boundaries explicit.

### Safety

- no missing API field is inferred;
- remote Epic redirects are revalidated before following;
- policy evals are not described as end-to-end LLM quality;
- LLM evals report `SKIPPED` when no responses/provider are configured;
- no invisible Unicode provenance mechanism is used;
- compile/runtime/multiplayer claims still require real evidence.

### Compatibility

V21/V22/V23 historical prompts and migration documents remain available where useful. `AI_BOOTSTRAP.md` is authoritative for repository-aware agents.

### Validation boundary

Static repository checks do not constitute a UEFN compile or runtime test.

## 23.0.0 — API Coverage, Generation Reliability & Provenance

### Added

- V23 structured API coverage fields for signature, parameters, return type, effects and events.
- deterministic `knowledge/api/coverage.json` and `verification_queue.json`.
- reviewed official evidence overlay in `verification_records.jsonl`.
- conservative Epic-page harvester that only creates unverified candidates.
- generation reliability task set and V22/V23 comparison tooling.
- visible generated-code status block plus hidden HTML provenance marker.
- V23 integrity, provenance and CLI tests.

### Safety

- harvested candidates never auto-promote to verified API knowledge;
- no invisible Unicode markers;
- compile/runtime claims still require real UEFN evidence.


## 22.0.0 — Knowledge Integrity & Agent Reliability

### Added

- `AI_BOOTSTRAP.md` as the primary AI entry point.
- Canonical `source_trust` and `validation` schemas.
- Progressive `knowledge/api/` structured symbol index.
- `verse-ai` Python CLI and `pyproject.toml` packaging.
- V22 integrity, CLI, generated-drift, and anti-hallucination checks.
- `evals/` structure for policy/retrieval/generation-oriented evaluation.
- V21 → V22 migration and architecture documentation.
- Optional MCP knowledge-server contract documentation.

### Changed

- Source authority and local validation are now separate axes.
- RAG scoring treats trust and validation separately.
- Generated-code marker uses V22 metadata and only local validation statuses.
- README is a shorter bilingual developer-facing landing page.
- GitHub validation workflows are consolidated into `ci.yml`.
- External corpus trust names are normalized to the V22 vocabulary.

### Migrated

- `benchmarks/evidence_composition.json` → `evals/retrieval/evidence_composition.json`.
- Legacy trust labels remain readable through compatibility aliases where needed.
- Existing scripts remain available while the unified CLI becomes the preferred interface.

### Compatibility

V22 intentionally preserves V21 tooling and project data where possible. Compatibility fields may remain in existing JSON while V22 canonical fields (`source_trust`, `validation`, `lifecycle_status`) are introduced progressively.

### Validation boundary

Static repository tests do not constitute a UEFN compile. No `compiled`, `verified`, or `multiplayer-verified` promotion may occur without corresponding evidence.
