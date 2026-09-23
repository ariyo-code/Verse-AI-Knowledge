# Verse AI Knowledge — English

**V22 — Knowledge Integrity & Agent Reliability**

> **Never invent a Verse API.**

Verse AI Knowledge is a knowledge repository and toolset for source-grounded Verse / UEFN assistance.

## Start here

Repository-aware agents should read `AI_BOOTSTRAP.md`, then `knowledge/ROUTING.md`, and retrieve only relevant evidence.

V22 separates:

- `source_trust`: authority/currentness of a source;
- `validation`: what was actually validated locally.

If an exact API cannot be verified, use `TODO(API VERIFY)`.

## Validation

`draft` → `static-checked` → `compiled` → `verified` → `multiplayer-verified`.

The last three require real corresponding UEFN evidence. Static analysis is never a UEFN compile.

## CLI

```bash
python -m pip install -e .
verse-ai doctor
verse-ai search "vehicle ownership"
verse-ai api GetFortCharacter
verse-ai validate
```

The V21 portable prompt with UI remains available for compatibility at `portable/VERSE_AI_MASTER_PROMPT_v21_WITH_UI.txt`.

See `README.md`, `AGENTS.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, and `docs/architecture/V22_KNOWLEDGE_INTEGRITY.md`.
