# AI Bootstrap — Verse AI Knowledge V22

This is the primary entry point for an AI working with this repository. It does **not** replace `AGENTS.md`.

## Absolute rule

**Never invent a Verse / UEFN API.** Never fabricate a class, function, event, module, property, effect, signature, import, or UEFN feature.

If an exact API claim cannot be supported by the repository's evidence model, use:

```text
TODO(API VERIFY)
```

A static check is not a UEFN compile. `compiled`, `verified`, and `multiplayer-verified` require real corresponding evidence.

## Required workflow

```text
Task
  ↓
AI_BOOTSTRAP
  ↓
knowledge/ROUTING.md
  ↓
Targeted retrieval
  ↓
Evidence Pack
  ↓
Claim validation
  ↓
Implementation
  ↓
UEFN validation when available
```

For non-trivial work:

1. Identify the domain and relevant project context.
2. Read `knowledge/ROUTING.md`.
3. Retrieve only the smallest useful set of sources.
4. Prefer exact, current, higher-trust evidence over similarity or model memory.
5. Build an Evidence Pack when the tooling is available.
6. Verify exact API signatures before emitting them as facts.
7. Use `TODO(API VERIFY)` for unsupported exact API claims.
8. Never claim a UEFN compile or runtime result that did not actually happen.
9. Consider lifecycle, multiplayer, cleanup, concurrency, failure contexts, and persistence when relevant.
10. Read `AGENTS.md` before substantial implementation.

## Two-axis confidence model

Every important technical claim should distinguish:

- `source_trust`: how authoritative/current the source is;
- `validation`: what has actually been validated locally.

These axes are independent. See `schemas/trust.schema.json`, `schemas/validation_status.schema.json`, and `docs/architecture/V22_KNOWLEDGE_INTEGRITY.md`.

## Fast commands

After installing the local CLI (`python -m pip install -e .`):

```bash
verse-ai search "vehicle ownership"
verse-ai context "create RP phone"
verse-ai api GetFortCharacter
verse-ai errors "compiler error text"
verse-ai doctor
verse-ai validate
```
