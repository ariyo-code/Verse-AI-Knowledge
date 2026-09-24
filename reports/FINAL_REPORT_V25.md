# V25 Final Engineering Report — stabilization candidate

## Release

```text
Release: 25.0.0
Schema: 25
Codename: Professionalization, API Expansion & Reproducible Verification
Verse API snapshot: 42.20
```

No V26 work is included. This package is a V25 stabilization candidate.

## Main correction

The GitHub V25 failures on the latest checked `main` HEAD were cascading from missing canonical portable prompt files. This candidate includes the current portable pack in the repository tree and validates it locally.

Required files present:

```text
portable/current/VERSE_AI_MASTER_PROMPT.txt
portable/current/VERSE_AI_MASTER_PROMPT_WITH_UI.txt
portable/current/TASK_TEMPLATE.txt
```

Prompt generation is deterministic in the candidate environment.

## GitHub state before candidate push

```text
HEAD: 80b8140ee718aa5aa390ac03f9cf73aae60b7973
V25 CI: FAIL
Docs: PASS
CodeQL: PASS
lint-types-package: PASS
retrieval-policy: PASS
```

The candidate GitHub CI status is **UNKNOWN until pushed**.

## Local validation actually executed

```text
V25 integrity: PASS
Repository integrity: PASS
Verification evidence: PASS
API revalidation gate: PASS
Prompt consistency/drift: PASS
Prompt generation deterministic: PASS
Internal paths: PASS
Secret scan: PASS
pytest: 13/13 PASS
Legacy RAG benchmark: 8/8 PASS
Evidence benchmark: 3/3 PASS
Anti-hallucination policy: 14/14 PASS
verse-ai doctor: PASS
verse-ai validate: PASS
Python compileall: PASS
```

GitHub's latest `lint-types-package` job independently reports:

```text
Ruff: PASS
mypy: PASS
Package build: PASS
```

## API coverage

```text
Known structured symbols: 164
Modules: 9
Exact signatures verified: 12
Known event names: 24
Verified event payloads: 0
Known members: 42
Presence-only symbols: 152
```

No API claim was fabricated to improve coverage.

## Retrieval metrics measured in this candidate

```text
Cases: 104
Recall@1: 0.0096
Recall@5: 0.8846
Recall@10: 0.9327
MRR: 0.3518
nDCG@10: 0.4956
```

## Opaque Project Recognition

The privacy-preserving opaque recognition layer is preserved. The public repository contains opaque fingerprints and generic recognition metadata, but no real project name, private project source, identity mapping, or private project registry. An opaque pattern match is not API evidence.

## Validation boundaries

```text
UEFN compile: NOT TESTED
Runtime: NOT TESTED
Multiplayer: NOT TESTED
LLM end-to-end benchmark: SKIPPED
```

## Publication readiness

```text
PUBLICATION READINESS: UNKNOWN
```

A real green V25 GitHub Actions run on the candidate commit is still required before preparing the `v25.0.0` GitHub Release.
