# How an AI should use this repository — V24

Repository-aware agents start with:

```text
AI_BOOTSTRAP.md
```

## Recommended flow

```text
User task
↓
AI_BOOTSTRAP
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
generated-code provenance
↓
static validation / API claim lint
↓
UEFN compile
↓
runtime test
↓
multiplayer test when relevant
↓
promotion with evidence
```

## Useful CLI

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

## Exact API rule

A symbol name being present does not prove:

- its signature;
- its parameters;
- its return type;
- its effects;
- an event payload.

Use the V24 claim resolver or inspect `field_evidence`.

If evidence is insufficient:

```text
TODO(API VERIFY)
```

## Generated code

Generated Verse in Markdown uses:

- a visible V24 status block;
- a hidden HTML comment after the Verse block.

See `docs/GENERATED_CODE_MARKER.md`.

## UEFN

Repository checks are not a compiler.

Never claim `compiled`, `verified`, or `multiplayer-verified` without the corresponding evidence.
