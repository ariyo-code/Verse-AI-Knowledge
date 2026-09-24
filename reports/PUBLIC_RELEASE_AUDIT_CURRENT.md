# Public Release Audit — V25 stabilization candidate

- Release: **25.0.0**
- Schema: **25**
- Codename: **Professionalization, API Expansion & Reproducible Verification**
- Verse API snapshot: **42.20**
- Candidate basis: public V25 package with Opaque Project Recognition preserved

## Candidate checks executed locally

- repository_integrity: **PASS**
- prompt_consistency: **PASS**
- generated_drift: **PASS**
- internal_paths: **PASS**
- secret_scan: **PASS**
- v25_integrity: **PASS**
- verification_evidence: **PASS**
- api_revalidation_gate: **PASS**
- pytest: **PASS — 13/13**
- retrieval_legacy: **PASS — 8/8**
- evidence_benchmark: **PASS — 3/3**
- hallucination_policy: **PASS — 14/14**
- verse-ai doctor: **PASS**
- verse-ai validate: **PASS**
- Python compileall (`src/verse_ai_knowledge`): **PASS**
- prompt generation deterministic: **PASS**

## GitHub status

Latest checked `main` HEAD before this candidate is pushed:

```text
80b8140ee718aa5aa390ac03f9cf73aae60b7973
```

Observed GitHub Actions state for that HEAD:

- V25 CI: **FAIL**
- Docs: **PASS**
- CodeQL: **PASS**
- lint-types-package: **PASS** (`ruff`, `mypy`, package build)
- retrieval-policy: **PASS**

The remaining failures on that HEAD are caused by `portable/current/` not being present in the Git commit. This candidate contains the required current portable artifacts.

Because this candidate has not yet been pushed and run by GitHub Actions:

```text
github_ci: UNKNOWN
```

Do not change that value to PASS until the candidate commit completes a green GitHub V25 CI run.

## Current measured API coverage

- known structured symbols: **164**
- modules represented: **9**
- exact signatures verified: **12**
- symbols with known event names: **24**
- verified event payloads: **0**
- symbols with known members: **42**
- presence-only symbols: **152**

These numbers describe symbols currently known to this repository, not Epic's total Verse API surface.

## Current retrieval metrics

Measured by `python tools/rag_metrics_v25.py` in this candidate environment:

```text
Cases:      104
Recall@1:   0.0096
Recall@5:   0.8846
Recall@10:  0.9327
MRR:        0.3518
nDCG@10:    0.4956
```

## Validation boundaries

- UEFN compile: **NOT TESTED**
- Runtime: **NOT TESTED**
- Multiplayer: **NOT TESTED**
- LLM end-to-end benchmark: **SKIPPED — no provider or saved responses configured**

## Publication

```text
PUBLICATION READINESS: UNKNOWN
```

Reason: the candidate still requires a real GitHub V25 CI run after push.
