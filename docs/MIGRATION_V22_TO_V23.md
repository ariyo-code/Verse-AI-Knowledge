# Migration V22 → V23

V23 is intentionally incremental. It keeps V22 trust/validation semantics and adds API-coverage evidence, generation evals and generated-code provenance.

## Main changes

- `schema_version`: 22 → 23
- API generator: `tools/migrate_api_catalog_v23.py`
- coverage: `knowledge/api/coverage.json`
- verification queue: `knowledge/api/verification_queue.json`
- reviewed evidence: `knowledge/api/verification_records.jsonl`
- candidate harvests: `knowledge/api/candidates/`
- generation evals: `evals/generation/`
- visible + hidden provenance: `docs/GENERATED_CODE_MARKER.md`

Old V22 validator/migration entry points remain as compatibility shims and delegate to V23.

No UEFN compile claim is introduced by this migration.
