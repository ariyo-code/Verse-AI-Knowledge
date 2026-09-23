# AI Bootstrap — Verse AI Knowledge V24

This is the authoritative entry point for repository-aware AI agents.

Read `AGENTS.md` before substantial implementation.

## Absolute rule

**Never invent a Verse / UEFN API.**

If an exact API claim cannot be supported:

```text
TODO(API VERIFY)
```

## V24 field-level API rule

A symbol being known does not prove every field.

Before emitting an exact:

- signature;
- parameter list;
- return type;
- effect;
- event payload;
- member name;

resolve the corresponding field against stored evidence.

Use:

```bash
verse-ai claim SYMBOL --field signature
verse-ai claim SYMBOL --field effects
```

A result of:

```text
TODO(API VERIFY)
```

must not be rewritten from memory.

## Required workflow

```text
Task
↓
knowledge/ROUTING.md
↓
targeted retrieval
↓
API claim resolution
↓
Evidence Pack
↓
Claim Ledger
↓
implementation
↓
V24 generated-code provenance
↓
static/API-claim validation
↓
UEFN compile/runtime/multiplayer validation when available
↓
promotion with evidence
```

## Generated Verse

Generated Verse in Markdown must use:

1. the visible V24 provenance block before the code;
2. the hidden HTML V24 marker after the code.

Never use invisible Unicode.

See `docs/GENERATED_CODE_MARKER.md`.

## Validation

Generated code defaults to:

```text
draft
```

Only real evidence can justify:

```text
compiled
verified
multiplayer-verified
```

## Useful commands

```bash
verse-ai search "vehicle ownership"
verse-ai context "create RP phone"
verse-ai api GetFortCharacter
verse-ai claim GetFortCharacter --field signature
verse-ai lint path/to/code.verse
verse-ai coverage
verse-ai api-queue
verse-ai errors "compiler error"
verse-ai doctor
verse-ai validate
```

Read `docs/architecture/V24_CLAIM_RESOLUTION.md` for the V24 evidence model.
