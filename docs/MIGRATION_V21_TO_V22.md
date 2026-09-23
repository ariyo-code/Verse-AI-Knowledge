# Migrating V21 to V22

V22 is intentionally incremental. It does not replace the existing knowledge base or portable UI prompt.

## Main migrations

- `manifest.json` becomes the canonical place for release, API snapshot, trust, and validation vocabularies.
- Legacy `status` / `verification` fields are retained when removing them could break tooling, while V22 fields are added.
- `knowledge/api_catalog.json` remains supported and is used to generate `knowledge/api/symbols.jsonl`.
- `benchmark/` remains as the legacy/manual scoring suite; the separate `benchmarks/` evidence composition fixture moves to `evals/retrieval/`.
- V21 portable prompts remain compatible; repository agents should enter through `AI_BOOTSTRAP.md`.

## Legacy trust aliases

Some old labels do not map one-to-one to V22 source trust. They are preserved as `evidence_basis` where useful:

- `module-index-verified` → source is `official-current`, claim scope remains presence-oriented;
- `official-guide-presence-verified` → `official-current`, presence-oriented;
- `external-community` → `community-unverified`.

This normalization does **not** promote exact signatures.

## Local validation migration

Project/system metadata derives V22 `validation` from explicit verification booleans where available. If evidence is absent, migration is conservative and does not preserve a `compiled`/`verified` claim merely because an old label said so.

## After upgrading

Run:

```bash
python tools/validate_v22_integrity.py
python tools/check_generated_drift.py
python tools/run_hallucination_evals.py
python tools/self_test.py
```

If UEFN was not used, report:

```text
UEFN compile status: NOT TESTED
```
