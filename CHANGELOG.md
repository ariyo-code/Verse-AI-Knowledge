# Changelog

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
