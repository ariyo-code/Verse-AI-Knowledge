# Public Release Audit — V24

## Résumé

- Release: **24.0.0**
- Schema: **24**
- Codename: **Claim Resolution, Evidence Graph & Continuous Verification**
- Verse API snapshot: **42.20**
- Package validation date: **2026-09-23**
- GitHub CI for this V24 package: **NOT RUN YET — package not pushed at audit time**
- UEFN compile status: **NOT TESTED**
- Runtime status: **NOT TESTED**
- Multiplayer status: **NOT TESTED**
- LLM end-to-end benchmark: **SKIPPED — no provider or saved responses configured**

V24 extends V23 without a structural rewrite. The focus is field-level API claim resolution, explicit evidence links, stale-evidence revalidation, generated-code provenance, conservative API linting, and measurable reliability workflows.

## Corrections et ajouts effectués

- Added field-level claim resolution so presence, signature, parameters, return type, effects, event payload and runtime behavior are not treated as equivalent evidence.
- Added `knowledge/api/evidence_graph.json` linking symbol fields to explicit evidence nodes.
- Added `knowledge/api/revalidation_state.json` and a revalidation gate so API-version changes cannot silently preserve stale exact claims.
- Added conservative Verse API claim linting and `verse-ai claim` / `verse-ai lint` workflows.
- Added deterministic API coverage snapshots and release-to-release diff tooling.
- Added V24 generated-code provenance with a visible status block and a normal HTML comment marker.
- Added explicit guards against invisible Unicode provenance mechanisms.
- Added provider-optional LLM eval infrastructure that reports `SKIPPED` when it is not configured.
- Added stricter Epic URL/redirect validation tests.
- Added internal-path and likely-secret validation.
- Preserved V21/V22/V23 historical/compatibility material where useful instead of rewriting the repository wholesale.

## API Coverage

Coverage below describes symbols currently known to this repository. It does **not** claim to represent the total Epic Verse API surface.

```text
Known structured symbols:        164
Modules represented:               9
Presence recorded:               164 / 164 (100.00%)
Exact signatures verified:        12 / 164 (7.32%)
Structured parameters:            12 / 164 (7.32%)
Structured return types:           12 / 164 (7.32%)
Structured effects:                12 / 164 (7.32%)
Symbols with known event names:    24 / 164 (14.63%)
Verified event payloads:            0 / 164 (0.00%)
Exact signature claims allowed:    12 / 164 (7.32%)
Field evidence present:           164 / 164 (100.00%)
Current revalidation state:       164 current / 0 needing attention
```

Claim state:

```text
exact-signature: 12
presence-only:   152
```

Source trust:

```text
signature-verified: 12
api-page-verified:  40
official-current:  112
```

Local validation:

```text
static-checked: 164
```

No missing signature, event payload, effect or return type is inferred from symbol names or nearby APIs.

## Validation réellement exécutée

### Static / repository tests

The following checks were executed against the packaged V24 tree and passed:

```text
python tools/validate_v24_integrity.py                 PASS
python tools/check_generated_drift.py                 PASS
python tools/self_test.py                             PASS
python tests/test_v24_integrity.py                    PASS
python tests/test_claim_resolution_v24.py             PASS
python tests/test_api_coverage_v24.py                 PASS
python tests/test_generated_provenance_v24.py         PASS
python tests/test_epic_url_security.py                PASS
python tools/check_internal_paths.py                  PASS
python tools/scan_secrets.py                          PASS
python tests/test_cli_contracts.py                    PASS
python tests/test_lab_state.py                        PASS
python tests/test_cli_v24.py                          PASS
python tools/validate_integrity.py                    PASS
python tools/check_verification.py                    PASS
python tools/validate_repo.py                         PASS
python tools/preflight.py                             PASS
python tools/validate_all.py                          PASS
```

The secret scan found no high-confidence credential pattern in the current packaged tree. This does not prove that Git history never contained a secret.

### Retrieval tests

```text
RAG benchmark: 8/8 PASS
Evidence benchmark: 3/3 PASS
```

### Policy evals

```text
Anti-hallucination policy eval: 14/14 PASS
```

These are deterministic repository guardrail tests. They do **not** prove that an LLM cannot hallucinate or that generated Verse compiles.

### LLM evals

```text
SKIPPED — no LLM provider or saved responses configured
```

No LLM-quality improvement percentage is claimed.

### UEFN

```text
Compile:     NOT TESTED
Runtime:     NOT TESTED
Multiplayer: NOT TESTED
```

No static check in this audit is treated as UEFN evidence.

## Generation provenance

V24 requires two complementary Markdown-level markers for generated Verse:

1. a visible status block carrying validation/API snapshot information;
2. a normal HTML comment marker using `verse-ai-generated:v24` for machine-readable provenance.

The marker includes validation state, API snapshot, compile/runtime/multiplayer flags, API-verification requirement and unresolved-claim count.

No zero-width, bidi-control or other invisible Unicode watermark mechanism is used.

## Reliability / claim resolution

V24 resolves exact API claims per field instead of using symbol-level confidence alone.

Conceptually:

```text
symbol presence
≠ exact signature
≠ parameter contract
≠ return type
≠ effects
≠ event payload
≠ runtime behavior
```

Unsupported exact claims must fall back to:

```text
TODO(API VERIFY)
```

The LLM benchmark harness exists, but no end-to-end model benchmark result is reported until real provider/model outputs are supplied.

## Limitations restantes

- UEFN compilation was not performed for this release package.
- Runtime behavior was not tested in UEFN.
- Multiplayer behavior was not tested in UEFN.
- End-to-end LLM evaluation is not configured in this audit.
- The structured API catalog is not a complete mirror of every API published by Epic.
- 152/164 currently known symbols remain `presence-only` for exact-signature claims.
- Verified event payload coverage is currently 0/164 symbols.
- External upstream compile claims still require local UEFN recompilation before local `compiled` promotion.
- GitHub Actions for V24 cannot be reported green until this package is actually pushed and the workflow runs on GitHub.

## Publication

The package is internally consistent and the local/static V24 validation suite passes.

```text
PACKAGE READINESS: READY
PUBLICATION READINESS: BLOCKED
```

Blocking reason:

```text
GitHub CI for the V24 commit has not run yet because this package has not been pushed.
```

After upload, `PUBLICATION READINESS` may be changed to `READY` only if the V24 GitHub CI completes successfully and no new critical issue is introduced.
