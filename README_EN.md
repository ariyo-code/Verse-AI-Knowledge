# Verse AI Knowledge — English

**V24 — Claim Resolution, Evidence Graph & Continuous Verification**

Verse AI Knowledge helps AI agents work with Verse / UEFN using retrieval, provenance, evidence and anti-hallucination guards.

> **Never invent a Verse API.**

## Start here

Repository-aware agents start with:

```text
AI_BOOTSTRAP.md
```

Recommended flow:

```text
ROUTING → targeted retrieval → API claim resolution → Evidence Pack → Claim Ledger → implementation → provenance → validation
```

## V24

V24 adds:

- field-level API claim resolution;
- API evidence graph;
- conservative Verse claim linting;
- API-version revalidation;
- coverage snapshots/diffs;
- redirect-safe Epic documentation fetching;
- visible + hidden V24 provenance;
- optional end-to-end LLM evaluation harness;
- public-release path/secret checks.

## CLI

```bash
python -m pip install -e .
verse-ai api GetFortCharacter
verse-ai claim GetFortCharacter --field signature
verse-ai lint path/to/code.verse
verse-ai coverage
verse-ai doctor
verse-ai validate
```

Unsupported exact claims must remain:

```text
TODO(API VERIFY)
```

Static validation does not prove UEFN compilation.

Original project content is governed by `LICENSE.md`; third-party material keeps its original licenses and provenance.
