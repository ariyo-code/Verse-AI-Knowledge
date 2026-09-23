# Migration V23 → V24

V24 is an incremental reliability release.

It does not remove V23 API coverage data.

## Main changes

- schema `23` → `24`;
- release `23.0.0` → `24.0.0`;
- generated provenance marker `v23` → `v24`;
- field-level API evidence;
- API evidence graph;
- claim resolver;
- static Verse API-claim lint;
- version-aware revalidation;
- coverage snapshots and diffs;
- redirect-safe Epic documentation fetch;
- provider-optional LLM eval harness;
- public-release path/secret checks.

## Generate V24 derived files

```bash
python tools/migrate_api_catalog_v24.py
```

This regenerates:

```text
knowledge/api/symbols.jsonl
knowledge/api/modules.json
knowledge/api/versions.json
knowledge/api/coverage.json
knowledge/api/verification_queue.json
knowledge/api/evidence_graph.json
knowledge/api/revalidation_state.json
```

No missing signature is inferred.

## Validate

```bash
python tools/validate_v24_integrity.py
python tools/check_generated_drift.py
python tests/test_v24_integrity.py
python tests/test_claim_resolution_v24.py
python tests/test_generated_provenance_v24.py
python tests/test_epic_url_security.py
verse-ai validate
```

## Compatibility

Historical V21/V22/V23 documents and prompts may keep their original version names when they are explicitly compatibility material.

For repository-aware agents, `AI_BOOTSTRAP.md` is authoritative.
